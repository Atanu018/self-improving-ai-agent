import random
import time
import json
import logging
from collections import defaultdict
from combined_gap import CombinedGapDetector  
from knowledge_retrieval import KnowledgeRetriever
from keybert import KeyBERT  

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LearningLoop:
    def __init__(self, cycle_interval=30, batch_update_interval=5):
        self.knowledge_gap_identifier = CombinedGapDetector()  
        self.knowledge_retriever = KnowledgeRetriever()
        self.kw_model = KeyBERT()  
        self.cycle_interval = cycle_interval  
        self.batch_update_interval = batch_update_interval  

        self.missing_keywords_tracker = defaultdict(int)  
        self.feedback_log = self.load_feedback_log()  
        self.knowledge_cache = {}  # ✅ Cache for retrieved knowledge
        self.failed_queries = set()  # ✅ Track failed queries to avoid retrying immediately
        self.batch_feedback_updates = {}  # ✅ Store feedback in memory for batch writing

    def generate_new_query(self):
        """Generate a query based on past failures and knowledge gaps."""
        # ✅ Prioritize past failures first
        if self.failed_queries:
            query = self.failed_queries.pop()  # Remove it from failed queries
            return query  

        past_gaps = self.load_past_gaps()
        if past_gaps:
            return max(past_gaps, key=past_gaps.get)  # Most frequent gap

        return "What are the latest advancements in AI?"  # Default query

    def extract_expected_keywords(self, query):
        """Retrieve knowledge and extract keywords dynamically."""
        retrieved_info = self.knowledge_retriever.retrieve_knowledge(query)
        keywords = self.extract_keywords_from_text(retrieved_info)
        return keywords

    def extract_keywords_from_text(self, text):
        """Extract keywords from text using KeyBERT."""
        keywords = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
        return [kw[0] for kw in keywords[:5]]  

    def refine_query(self, query):
        """Modify the query dynamically if initial retrieval is weak."""
        logging.info(f"🔄 Refining Query: {query}")
        refined_queries = [
            f"Comprehensive guide on {query}",
            f"Detailed explanation of {query}",
            f"Latest research on {query}",
            f"Beginner-friendly introduction to {query}"
        ]
        return random.choice(refined_queries)  

    def retrieve_and_refine_knowledge(self, query, expected_keywords):
        """Retrieve knowledge with caching and refine query if needed."""
        # ✅ Check cache first
        if query in self.knowledge_cache:
            logging.info(f"⚡ Using cached knowledge for: {query}")
            return self.knowledge_cache[query]

        retrieved_info = self.knowledge_retriever.retrieve_knowledge(query)
        retrieved_keywords = self.extract_keywords_from_text(retrieved_info)

        missing_keywords = [kw for kw in expected_keywords if kw not in retrieved_keywords]

        if len(missing_keywords) > 2:
            refined_query = self.refine_query(query)
            logging.warning(f"⚠️ Weak retrieval. Refining query to: {refined_query}")
            retrieved_info = self.knowledge_retriever.retrieve_knowledge(refined_query)

        # ✅ Store in cache
        self.knowledge_cache[query] = retrieved_info
        return retrieved_info

    def store_feedback(self, query, was_successful):
        """Store feedback on whether a query was effective."""
        self.batch_feedback_updates[query] = was_successful  # ✅ Store feedback in memory

        # ✅ Batch write feedback to reduce file I/O
        if len(self.batch_feedback_updates) >= self.batch_update_interval:
            with open("feedback_log.json", "w") as file:
                json.dump(self.batch_feedback_updates, file, indent=4)
            logging.info("✅ Batch feedback saved.")
            self.batch_feedback_updates.clear()  # ✅ Clear after writing

    def load_feedback_log(self):
        """Load feedback data from a file."""
        try:
            with open("feedback_log.json", "r") as file:
                return json.load(file)  
        except FileNotFoundError:
            return {}

    def run(self):
        """Run the self-improving AI loop with adaptive learning."""
        iteration = 0  
        while True:
            logging.info("🔍 Identifying knowledge gaps...")

            query = self.generate_new_query()  
            expected_keywords = self.extract_expected_keywords(query)  

            retrieved_info = self.retrieve_and_refine_knowledge(query, expected_keywords)

            # Identify gaps using the combined approach
            gap_result = self.knowledge_gap_identifier.detect_combined_gap(query, retrieved_info, expected_keywords)

            missing_keywords = gap_result["missing_keywords"]
            semantic_gap = gap_result["semantic_gap"]

            if missing_keywords:
                logging.warning(f"⚠️ Knowledge Gaps Detected: {missing_keywords}")

                # Update frequency of missing keywords
                for keyword in missing_keywords:
                    self.missing_keywords_tracker[keyword] += 1  

                prioritized_keywords = sorted(
                    missing_keywords, key=lambda kw: self.missing_keywords_tracker[kw], reverse=True
                )
                new_knowledge = self.knowledge_retriever.retrieve_knowledge(" ".join(prioritized_keywords))
                
                logging.info(f"📚 Learning new concepts: {new_knowledge}")
                self.store_new_knowledge(new_knowledge)  
                self.store_feedback(query, False)  # Mark query as unsuccessful
                self.failed_queries.add(query)  # ✅ Add to failed queries for retrying later
            
            elif semantic_gap:
                logging.warning("🔄 Semantic Gap Detected: AI needs better contextual understanding.")
                additional_knowledge = self.knowledge_retriever.retrieve_knowledge("Deep explanation of " + query)
                logging.info(f"📘 Learning advanced context: {additional_knowledge}")
                self.store_new_knowledge(additional_knowledge)
                self.store_feedback(query, False)  # Mark query as unsuccessful
            
            else:
                logging.info("✅ No gaps detected. AI knowledge is up-to-date.")
                self.store_feedback(query, True)  # Mark query as successful

            iteration += 1

            # ✅ Save feedback every batch interval
            if iteration % self.batch_update_interval == 0:
                with open("feedback_log.json", "w") as file:
                    json.dump(self.feedback_log, file, indent=4)

            logging.info(f"⏳ Waiting {self.cycle_interval} seconds before next learning cycle...\n")
            time.sleep(self.cycle_interval)

    def store_new_knowledge(self, knowledge):
        """Save newly learned knowledge for future reference."""
        with open("learned_knowledge.txt", "a") as file:
            file.write(json.dumps(knowledge, indent=4) + "\n")  

    def load_past_gaps(self):
        """Load past knowledge gaps from a file."""
        try:
            with open("past_gaps.txt", "r") as file:
                gaps = file.read().splitlines()
                return {gap: gaps.count(gap) for gap in gaps}  
        except FileNotFoundError:
            return {}
