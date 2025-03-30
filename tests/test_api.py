import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if your server is running elsewhere

def test_api():
    query = "Latest advancements in AI"
    response = requests.post(f"{BASE_URL}/query", json={"query": query})

    if response.status_code == 200:
        result = response.json()
        print("✅ API is working!")
        print("🔹 Response:", result)

        if 'google_results' in result and result['google_results']:
            print("✅ Google Search API is integrated successfully!")
            for idx, res in enumerate(result['google_results'], start=1):
                print(f"{idx}. {res['title']} - {res['link']}")
        else:
            print("⚠️ No Google Search results. Check API key or query.")
    else:
        print(f"❌ API test failed! Status Code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    test_api()
