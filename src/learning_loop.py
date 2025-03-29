import random
import time
import json
from knowledge_gap import KnowledgeGapDetector
from knowledge_retrieval import KnowledgeRetriever
from keybert import KeyBERT  # Import KeyBERT for keyword extraction

class LearningLoop:
    def __init__(self, cycle_interval=30):  # Add cycle_interval as an optional parameter
        self.knowledge_gap_identifier = KnowledgeGapDetector()
        self.knowledge_retriever = KnowledgeRetriever()
        self.kw_model = KeyBERT()  # Initialize KeyBERT
        self.cycle_interval = cycle_interval  # Store cycle interval for repeated learning

    def generate_new_query(self):
        """Dynamically generate a new topic to learn based on past knowledge gaps."""
        past_gaps = self.load_past_gaps()  # Load past knowledge gaps from a file or database
        if past_gaps:
            return random.choice(past_gaps)  # Pick a random knowledge gap to explore
        return "What are the latest advancements in AI?"  # Default topic if no gaps found

    def extract_expected_keywords(self, query):
        """Retrieve knowledge and extract keywords dynamically."""
        retrieved_info = self.knowledge_retriever.retrieve_knowledge(query)
        keywords = self.extract_keywords_from_text(retrieved_info)
        return keywords

    def extract_keywords_from_text(self, text):
        """Extract keywords from a given text using KeyBERT."""
        keywords = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
        return [kw[0] for kw in keywords[:5]]  # Return top 5 keywords

    def run(self):
        """Run the self-improving AI loop with a cycle interval."""
        while True:
            print("🔍 Identifying knowledge gaps...")
            query = self.generate_new_query()  # Step 1: Generate a new query dynamically
            retrieved_info = self.knowledge_retriever.retrieve_knowledge(query)  # Step 2: Retrieve knowledge
            expected_keywords = self.extract_expected_keywords(query)  # Step 3: Extract keywords dynamically

            # Step 4: Identify knowledge gaps
            missing_keywords = self.knowledge_gap_identifier.detect_gap(query, retrieved_info, expected_keywords)

            # Step 5: If there are gaps, refine learning
            if missing_keywords:
                print(f"⚠️ Knowledge Gaps Detected: {missing_keywords}")
                new_knowledge = self.knowledge_retriever.retrieve_knowledge(" ".join(missing_keywords))
                print(f"📚 Learning new concepts: {new_knowledge}")
                self.store_new_knowledge(new_knowledge)  # Store new knowledge for future use
            else:
                print("✅ No gaps detected. AI knowledge is up-to-date.")

            print(f"⏳ Waiting {self.cycle_interval} seconds before next learning cycle...\n")
            time.sleep(self.cycle_interval)  # Wait before the next cycle

    def store_new_knowledge(self, knowledge):
        """Save newly learned knowledge for future reference."""
        with open("learned_knowledge.txt", "a") as file:
            file.write(json.dumps(knowledge, indent=4) + "\n")  # Convert dict to JSON string

    def load_past_gaps(self):
        """Load past knowledge gaps from a file."""
        try:
            with open("past_gaps.txt", "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []
