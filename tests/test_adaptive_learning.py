import sys
import os

# Ensure the backend folder is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from backend.adaptive_learning import google_search, wikipedia_search
import backend.config

def test_google_search():
    """Test the Google Search function."""
    query = "Latest AI advancements"
    results = google_search(query)
    
    if results:
        print(f"✅ Google Search returned {len(results)} results.")
        for i, res in enumerate(results[:3], 1):  # Show only first 3 results
            print(f"{i}. {res}")
    else:
        print("❌ Google Search returned no results. Check API key or quota.")

def test_wikipedia_search():
    """Test the Wikipedia Search function."""
    query = "Artificial Intelligence"
    results = wikipedia_search(query)

    if results:
        print(f"✅ Wikipedia Search returned {len(results)} results.")
        for i, res in enumerate(results[:1], 1):  # Show only first result
            print(f"{i}. {res[:200]}...")  # Truncate for readability
    else:
        print("❌ Wikipedia Search returned no results.")

if __name__ == "__main__":
    test_google_search()
    test_wikipedia_search()
