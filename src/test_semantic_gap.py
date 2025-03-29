from semantic_gap import SemanticGapDetector

# Initialize Semantic Gap Detector
detector = SemanticGapDetector()

# Test Cases
test_cases = [
    {
        "query": "What is deep learning?",
        "retrieved_knowledge": "Deep learning is a subset of machine learning based on artificial neural networks.",
        "expected_gap": False  # This should not be a gap as it's relevant.
    },
    {
        "query": "Explain quantum mechanics",
        "retrieved_knowledge": "The Mona Lisa is a famous painting by Leonardo da Vinci.",
        "expected_gap": True  # This is unrelated, so it should be a gap.
    },
    {
        "query": "What are the applications of AI?",
        "retrieved_knowledge": "",
        "expected_gap": True  # No knowledge retrieved, so it's a gap.
    }
]

# Run tests
for i, test in enumerate(test_cases, 1):
    result = detector.detect_gap(test["query"], test["retrieved_knowledge"])
    print(f"Test {i}: {result}")
    assert result["gap_detected"] == test["expected_gap"], f"Test {i} failed!"
    
print("✅ All tests passed!")
