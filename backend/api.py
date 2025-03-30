from flask import Flask, request, jsonify
from adaptive_learning import google_search, wikipedia_search
import config

app = Flask(__name__)

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

    # Combine and return results
    combined_results = {"google_results": google_results, "wikipedia_results": wikipedia_results}

    return jsonify({"query": query, "results": combined_results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=True)
