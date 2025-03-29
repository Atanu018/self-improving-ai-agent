from knowledge_gap import KnowledgeGapDetector

detector = KnowledgeGapDetector()

# Example query and expected response
query = "What is Reinforcement Learning?"
response = "It is a machine learning technique."
expected_keywords = ["reward", "policy", "agent", "environment"]

# Check for knowledge gaps
gap = detector.detect_gap(query, response, expected_keywords)

# Print the results
print("Detected Knowledge Gaps:", gap)
