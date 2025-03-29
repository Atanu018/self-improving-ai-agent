from knowledge_gap import KnowledgeGapDetector

detector = KnowledgeGapDetector()

query = "What is machine learning?"
response = "Machine learning is a subset of AI."
expected_keywords = ["algorithm", "data", "training", "model", "supervised", "unsupervised"]

missing_keywords = detector.detect_gap(query, response, expected_keywords)
print("Missing Keywords:", missing_keywords)
