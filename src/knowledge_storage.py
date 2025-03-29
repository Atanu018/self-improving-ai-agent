import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class KnowledgeStorage:
    """
    Manages the storage and retrieval of knowledge.
    """

    def __init__(self, storage_file="knowledge_base.json"):
        self.storage_file = storage_file
        self.knowledge_data = self._load_knowledge()

    def _load_knowledge(self):
        """Load existing knowledge from file or initialize empty storage."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                logging.warning("Corrupted knowledge file. Reinitializing.")
                return {}
        return {}

    def save_knowledge(self):
        """Save updated knowledge to file."""
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump(self.knowledge_data, file, indent=4)
        logging.info("Knowledge storage updated.")

    def update_knowledge(self, new_data):
        """
        Updates the knowledge base with new data.
        - new_data: Dictionary of missing keywords and retrieved information.
        """
        updated = False
        for keyword, info in new_data.items():
            if keyword not in self.knowledge_data or self.knowledge_data[keyword] != info:
                self.knowledge_data[keyword] = info
                updated = True
                logging.info(f"Knowledge updated for: {keyword}")
        
        if updated:
            self.save_knowledge()
        else:
            logging.info("No new knowledge updates were necessary.")

    def get_knowledge(self, keyword):
        """Retrieve stored knowledge for a specific keyword."""
        return self.knowledge_data.get(keyword, "Knowledge not found.")

