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
        self.knowledge_cache = {}  
        self.failed_queries = set()  
        self.batch_feedback_updates = {}  

    def generate_new_query(self):
        """Generate a query based on past failures and knowledge gaps."""
        if self.failed_queries:
            query = self.failed_queries.pop()  
            self.failed_queries.add(query)  # Keep it in the queue until successfully learned
            logging.info(f"🔄 Retrying failed query: {query}")
            return query  

        past_gaps = self.load_past_gaps()
        if past_gaps:
            return max(past_gaps, key=past_gaps.get)  

        logging.info("📌 Default Query Used: What are the latest advancements in AI?")
        return "What are the latest advancements in AI?"


    def extract_expected_keywords(self, query):
        """
        Extracts key topics from the query.
        """
        retrieved_info = self.knowledge_retriever.search_wikipedia(query)
        
        if not retrieved_info or retrieved_info == "No Wikipedia results found.":
            logging.warning(f"⚠️ No useful Wikipedia data for: {query}")
    
            # Fix: Use past failed queries for better keyword generation
            if self.failed_queries:
                alternative_query = random.choice(list(self.failed_queries))
                logging.info(f"🔄 Trying alternative query: {alternative_query}")
                retrieved_info = self.knowledge_retriever.search_wikipedia(alternative_query)
    
            if not retrieved_info or retrieved_info == "No Wikipedia results found.":
                logging.warning("⚠️ No useful data found even after alternative query.")
                return ["Artificial Intelligence", "Machine Learning", "Deep Learning", "AI Trends"]
    
        extracted_keywords = self.extract_keywords_from_text(retrieved_info)
        
        if not extracted_keywords:
            logging.warning("⚠️ No keywords extracted. Using default AI-related topics.")
            return ["Artificial Intelligence", "Machine Learning", "Deep Learning", "AI Trends"]
        
        return extracted_keywords
    
    

    def extract_keywords_from_text(self, text):
        """
        Extracts keywords from the given text using KeyBERT.
        Handles cases where text is empty or invalid.
        """
        if not isinstance(text, str) or not text.strip():
            logging.warning("⚠️ Empty or invalid text received for keyword extraction.")
            return []  # Return an empty list to prevent errors

        try:
            keywords = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
            return [kw[0] for kw in keywords]  # Extract just the keywords
        except Exception as e:
            logging.error(f"❌ Error extracting keywords: {e}")
            return []  # Return an empty list on failure
  

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
        if query in self.knowledge_cache:
            logging.info(f"⚡ Using cached knowledge for: {query}")
            return self.knowledge_cache[query]

        logging.info(f"📌 Searching for: {query}")  
        retrieved_info = self.knowledge_retriever.retrieve_knowledge(query)
        retrieved_keywords = self.extract_keywords_from_text(retrieved_info)

        missing_keywords = [kw for kw in expected_keywords if kw not in retrieved_keywords]

        if len(missing_keywords) > 2:
            refined_query = f"Comprehensive guide on {' '.join(missing_keywords)}"
            logging.warning(f"⚠️ Weak retrieval. Refining query to: {refined_query}")

            # Fix: Try refinement once more if the first one fails
            refined_info = self.knowledge_retriever.retrieve_knowledge(refined_query)
            refined_keywords = self.extract_keywords_from_text(refined_info)

            if len([kw for kw in expected_keywords if kw not in refined_keywords]) > 2:
                refined_query = f"Detailed explanation of {' '.join(missing_keywords)}"
                logging.warning(f"⚠️ Second refinement needed: {refined_query}")
                refined_info = self.knowledge_retriever.retrieve_knowledge(refined_query)

            self.knowledge_cache[query] = refined_info
            return refined_info

        self.knowledge_cache[query] = retrieved_info
        return retrieved_info


    def store_feedback(self, query, was_successful):
        """Store feedback on whether a query was effective."""
        self.batch_feedback_updates[query] = was_successful  

        if len(self.batch_feedback_updates) >= self.batch_update_interval:
            with open("feedback_log.json", "w") as file:
                json.dump(self.batch_feedback_updates, file, indent=4)
            logging.info("✅ Batch feedback saved.")
            self.batch_feedback_updates.clear()  

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

            gap_result = self.knowledge_gap_identifier.detect_combined_gap(query, retrieved_info, expected_keywords)

            missing_keywords = gap_result["missing_keywords"]
            semantic_gap = gap_result["semantic_gap"]

            if missing_keywords:
                logging.warning(f"⚠️ Knowledge Gaps Detected: {missing_keywords}")

                for keyword in missing_keywords:
                    self.missing_keywords_tracker[keyword] += 1  

                prioritized_keywords = sorted(
                    missing_keywords, key=lambda kw: self.missing_keywords_tracker[kw], reverse=True
                )
                new_knowledge = self.knowledge_retriever.retrieve_knowledge(" ".join(prioritized_keywords))
                
                logging.info(f"📚 Learning new concepts: {new_knowledge}")
                self.store_new_knowledge(new_knowledge)  
                self.store_feedback(query, False)  
                self.failed_queries.add(query)  
            
            elif semantic_gap:
                logging.warning("🔄 Semantic Gap Detected: AI needs better contextual understanding.")
                additional_knowledge = self.knowledge_retriever.retrieve_knowledge("Deep explanation of " + query)
                logging.info(f"📘 Learning advanced context: {additional_knowledge}")
                self.store_new_knowledge(additional_knowledge)
                self.store_feedback(query, False)  
            
            else:
                logging.info("✅ No gaps detected. AI knowledge is up-to-date.")
                self.store_feedback(query, True)  

            iteration += 1

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
            logging.warning("⚠️ past_gaps.txt not found. Starting fresh.")
            return {}
