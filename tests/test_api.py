import pytest
import json
from backend.api import app

@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_search_api(client):
    """Tests the search API endpoint."""
    response = client.post("/search", json={"query": "Artificial Intelligence"})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "results" in data
    assert len(data["results"]) > 0
