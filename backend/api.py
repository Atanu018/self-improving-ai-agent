from flask import Flask, request, jsonify
from search_engine import google_search, wikipedia_search
from adaptive_learning import AdaptiveLearning
import config

app = Flask(__name__)
adaptive_model = AdaptiveLearning()

@app.route("/search", methods=["POST"])
def search():
    """Handles user queries and retrieves search results."""
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Perform Google & Wikipedia search
    google_results = google_search(query)
    wikipedia_results = wikipedia_search(query)

    # Improve with adaptive learning
    refined_results = adaptive_model.enhance_results(query, google_results + wikipedia_results)

    return jsonify({"query": query, "results": refined_results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=True)
