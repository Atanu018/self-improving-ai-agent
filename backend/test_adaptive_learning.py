import sys
import os

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
                
from adaptive_learning import AdaptiveLearning

def test_adaptive_learning():
    learner = AdaptiveLearning()
    query = "Latest advancements in AI"

    print("🔍 Running adaptive learning test...")
    result = learner.process_query(query)

    print("\n✅ Learning Process Complete!")
    print("🔹 Identified Gaps:", result.get("identified_gaps", "No gaps found"))

    if 'google_results' in result and result['google_results']:
        print("✅ Google Search API is integrated successfully!")
        for idx, res in enumerate(result['google_results'], start=1):
            print(f"{idx}. {res['title']} - {res['link']}")
    else:
        print("⚠️ No Google Search results. Check API key or query.")

if __name__ == "__main__":
    test_adaptive_learning()
