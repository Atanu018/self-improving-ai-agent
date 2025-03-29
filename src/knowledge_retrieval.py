import wikipediaapi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class KnowledgeRetriever:
    """
    Retrieves missing knowledge from external sources.
    """

    def __init__(self):
        # Set a proper user-agent
        self.wiki_api = wikipediaapi.Wikipedia(
            language="en",
            user_agent="Self-Improving-AI-Agent/1.0 (https://github.com/Atanu018/self-improving-ai-agent)"
        )

    def search_wikipedia(self, topic: str) -> str:
        """
        Retrieves a Wikipedia summary for the given topic.
        """
        page = self.wiki_api.page(topic)
        if page.exists():
            logging.info(f"Wikipedia result found for {topic}")
            return page.summary[:1000]  # Limit to 1000 characters
        else:
            logging.warning(f"No Wikipedia results for {topic}")
            return "No Wikipedia results found."

    def retrieve_knowledge(self, missing_keywords: list) -> dict:
        """
        Searches for missing knowledge on Wikipedia for each keyword.
        Returns a dictionary with keywords and their retrieved information.
        """
        knowledge_data = {}
        for keyword in missing_keywords:
            logging.info(f"Searching for: {keyword}")
            knowledge_data[keyword] = self.search_wikipedia(keyword)
        return knowledge_data
