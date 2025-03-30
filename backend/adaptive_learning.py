import sys
import os

# Ensure root directory is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import config

def google_search(query):
    """Fetches search results from Google (using API)."""
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={config.GOOGLE_API_KEY}&cx={config.SEARCH_ENGINE_ID}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        data = response.json()
        return [item["link"] for item in data.get("items", [])]
    
    return []

def wikipedia_search(query):
    """Fetches Wikipedia results for a given query."""
    wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={query}&prop=extracts&exintro"
    response = requests.get(wiki_url)

    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        return [page.get("extract", "") for page in pages.values() if "extract" in page]
    
    return []
