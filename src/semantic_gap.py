import torch
from sentence_transformers import SentenceTransformer, util
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SemanticGapDetector:
    def __init__(self, model_name="all-MiniLM-L6-v2", threshold=0.7):
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold

    def detect_gap(self, query, retrieved_knowledge):
        # Ensure retrieved_knowledge is a valid string
        if not retrieved_knowledge or not isinstance(retrieved_knowledge, str):
            logging.warning("⚠️ No valid knowledge retrieved! Assuming a gap exists.")
            return {"gap_detected": True, "similarity_score": 0.0, "reason": "No knowledge retrieved"}

        # Convert query and knowledge to embeddings
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        try:
            knowledge_embedding = self.model.encode(retrieved_knowledge, convert_to_tensor=True)
        except Exception as e:
            logging.error(f"❌ Error encoding retrieved knowledge: {e}")
            return {"gap_detected": True, "similarity_score": 0.0, "reason": "Failed to process knowledge"}

        # Compute similarity
        similarity_score = util.pytorch_cos_sim(query_embedding, knowledge_embedding).item()
        gap_detected = similarity_score < self.threshold

        result = {
            "gap_detected": gap_detected,
            "similarity_score": similarity_score,
            "reason": "Low similarity score" if gap_detected else "Knowledge is relevant"
        }

        logging.info(f"Query: {query} | Similarity Score: {similarity_score:.4f} | Gap Detected: {gap_detected}")
        return result
