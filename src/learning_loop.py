import random
import time
import json
import logging
from combined_gap import CombinedGapDetector
from knowledge_retrieval import KnowledgeRetriever
from keybert import KeyBERT

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LearningLoop:
    def __init__(self, cycle_interval=30):
        self.knowledge_gap_identifier = CombinedGapDetector()
        self.knowledge_retriever = KnowledgeRetriever()
        self.kw_model = KeyBERT()
        self.cycle_interval = cycle_interval  

    def generate_new_query(self):
        """Dynamically generate a new topic to learn based on past knowledge gaps."""
        past_gaps = self.load_past_gaps()
        return random.choice(past_gaps) if past_gaps else "What are the latest advancements in AI?"

    def extract_expected_keywords(self, query):
        """Retrieve knowledge and extract keywords dynamically."""
        retrieved_info = self.knowledge_retriever.retrieve_knowledge(query)
        return self.extract_keywords_from_text(retrieved_info)

    def extract_keywords_from_text(self, text):
        """Extract keywords from text using KeyBERT."""
        keywords = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
        return [kw[0] for kw in keywords[:5]]  

    def run(self):
        """Run the self-improving AI loop with a cycle interval."""
        while True:
            logging.info("🔍 Identifying knowledge gaps...")

            query = self.generate_new_query()
            retrieved_info = self.knowledge_retriever.retrieve_knowledge(query)
            expected_keywords = self.extract_expected_keywords(query)

            gap_result = self.knowledge_gap_identifier.detect_combined_gap(query, retrieved_info, expected_keywords)

            missing_keywords = gap_result.get("missing_keywords", [])  
            semantic_gap = gap_result.get("semantic_gap", False)  

            if missing_keywords:
                logging.warning(f"⚠️ Knowledge Gaps Detected: {missing_keywords}")
                new_knowledge = self.knowledge_retriever.retrieve_knowledge(missing_keywords)
                logging.info(f"📚 Learning new concepts: {new_knowledge}")
                self.store_new_knowledge(new_knowledge)
            
            if semantic_gap:
                logging.warning("🔄 Semantic Gap Detected: AI needs better contextual understanding.")
                additional_knowledge = self.knowledge_retriever.retrieve_knowledge([query])
                logging.info(f"📘 Learning advanced context: {additional_knowledge}")
                self.store_new_knowledge(additional_knowledge)

            if not missing_keywords and not semantic_gap:
                logging.info("✅ No gaps detected. AI knowledge is up-to-date.")

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
                return file.read().splitlines()
        except FileNotFoundError:
            return []
