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
        If the topic is too specific, it tries searching for broader terms.
        """
        page = self.wiki_api.page(topic)
    
        if page.exists():
            logging.info(f"✅ Wikipedia result found for: {topic}")
            return page.summary[:1000]  # Limit to 1000 characters
    
        logging.warning(f"⚠️ No Wikipedia results for: {topic}. Trying refined search...")
    
        # Try refining the search: Break query into meaningful words
        refined_topics = topic.split()  # Break query into individual words
        for term in refined_topics:
            if len(term) > 3:  # Ignore small words
                refined_page = self.wiki_api.page(term)
                if refined_page.exists():
                    logging.info(f"✅ Wikipedia result found for refined term: {term}")
                    return refined_page.summary[:1000]
    
        logging.warning(f"⚠️ No Wikipedia results found for any refined terms.")
        return "No Wikipedia results found."
    

    def retrieve_knowledge(self, missing_keywords) -> dict:
        """
        Searches for missing knowledge on Wikipedia.
        If `missing_keywords` is a string, it will be treated as a single query.
        If it's a list, it will search for each keyword separately.
        Returns a dictionary with keywords and their retrieved information.
        """
        knowledge_data = {}

        # Ensure missing_keywords is treated as a full query string if needed
        if isinstance(missing_keywords, list):
            if len(missing_keywords) == 1:
                missing_keywords = missing_keywords[0]  # Convert single-item list to string
            else:
                missing_keywords = " ".join(missing_keywords)  # Convert list into a full query string

        if isinstance(missing_keywords, str):
            logging.info(f"🔍 Searching for: {missing_keywords}")
            knowledge_data[missing_keywords] = self.search_wikipedia(missing_keywords)
        else:
            logging.error("❌ Invalid query format. Expected string or list of strings.")

        return knowledge_data
