import pytest
from backend.adaptive_learning import AdaptiveLearning

def test_adaptive_learning():
    """Tests adaptive learning system."""
    model = AdaptiveLearning()
    
    query = "Machine Learning"
    initial_results = ["https://example.com/ml"]

    model.enhance_results(query, initial_results)
    
    updated_results = model.enhance_results(query, ["https://newsource.com"])
    assert "https://example.com/ml" in updated_results
    assert "https://newsource.com" in updated_results
