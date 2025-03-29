import logging
from knowledge_storage import KnowledgeStorage

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SelfImprovement:
    """
    Handles the agent's ability to improve its knowledge by integrating new information.
    """

    def __init__(self):
        self.knowledge_storage = KnowledgeStorage()

    def improve_knowledge(self, new_knowledge):
        """
        Compare new knowledge with existing knowledge and update if necessary.
        - new_knowledge: Dictionary of missing keywords and retrieved information.
        """
        updated = False
        for keyword, new_info in new_knowledge.items():
            stored_info = self.knowledge_storage.get_knowledge(keyword)
            
            if stored_info == "Knowledge not found." or stored_info != new_info:
                logging.info(f"Updating knowledge for: {keyword}")
                self.knowledge_storage.update_knowledge({keyword: new_info})
                updated = True
            else:
                logging.info(f"Knowledge for '{keyword}' is already up-to-date.")
        
        if updated:
            logging.info("Self-improvement completed successfully.")
        else:
            logging.info("No improvements were needed.")

