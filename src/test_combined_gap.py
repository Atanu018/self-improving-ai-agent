from combined_gap import CombinedGapDetector

# Initialize the Combined Gap Detector
detector = CombinedGapDetector()

# Test Cases
test_cases = [
    {
        "query": "What is cloud computing?",
        "response": "Cloud computing provides on-demand computing services over the internet.",
        "expected_keywords": ["cloud", "computing", "internet", "services"],
        "expected_gap": False  # Relevant response
    },
    {
        "query": "Explain data science.",
        "response": "Painting is a form of artistic expression.",
        "expected_keywords": ["data", "science", "analysis", "statistics"],
        "expected_gap": True  # Unrelated response
    },
    {
        "query": "What are the benefits of AI?",
        "response": "",
        "expected_keywords": ["AI", "benefits", "automation"],
        "expected_gap": True  # No response → gap detected
    }
]

# Run tests
for i, test in enumerate(test_cases, 1):
    result = detector.detect_combined_gap(test["query"], test["response"], test["expected_keywords"])
    print(f"Test {i}: {result}")
    assert result["final_gap_detected"] == test["expected_gap"], f"Test {i} failed!"
    
print("✅ All tests passed!")
