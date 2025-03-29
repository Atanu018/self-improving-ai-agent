import logging
from knowledge_gap import KnowledgeGapDetector
from semantic_gap import SemanticGapDetector

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CombinedGapDetector:
    def __init__(self, semantic_threshold=0.7, lexical_threshold=3, weight_semantic=0.6, weight_lexical=0.4):
        self.semantic_detector = SemanticGapDetector(threshold=semantic_threshold)
        self.lexical_detector = KnowledgeGapDetector()
        self.weight_semantic = weight_semantic
        self.weight_lexical = weight_lexical
        self.lexical_threshold = lexical_threshold

    def detect_combined_gap(self, query, response, expected_keywords):
        lexical_result = self.lexical_detector.detect_gap(query, response, expected_keywords)
        semantic_result = self.semantic_detector.detect_gap(query, response)

        missing_keywords = lexical_result if isinstance(lexical_result, list) else []
        lexical_gap = len(missing_keywords) >= self.lexical_threshold  
        semantic_gap = semantic_result.get("gap_detected", False)  

        final_gap_score = (self.weight_lexical * lexical_gap) + (self.weight_semantic * semantic_gap)
        final_gap_detected = final_gap_score > 0.5  

        result = {
            "final_gap_detected": final_gap_detected,
            "lexical_gap": lexical_gap,
            "semantic_gap": semantic_gap,
            "semantic_score": semantic_result.get("similarity_score", 0.0),
            "missing_keywords": missing_keywords,
            "reason": "Combined lexical & semantic gap detection",
        }

        logging.info(f"Query: {query}")
        logging.info(f"Final Gap Detected: {final_gap_detected} | Lexical Gap: {lexical_gap} | Semantic Gap: {semantic_gap}")
        logging.info(f"Missing Keywords: {missing_keywords} | Similarity Score: {result['semantic_score']:.4f}")
        
        return result
