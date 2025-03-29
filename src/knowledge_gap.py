import logging
from typing import Dict, List

# Set up logging to track AI's knowledge gaps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class KnowledgeGapDetector:
    """
    Detects knowledge gaps in the AI's responses and categorizes them.
    """

    def __init__(self):
        self.gaps = []  # Stores detected knowledge gaps

    def detect_gap(self, query: str, response: str, expected_keywords: List[str]) -> Dict:
        """
        Analyzes AI's response and detects missing information.
        """
        missing_keywords = [kw for kw in expected_keywords if kw.lower() not in response.lower()]

        if missing_keywords:
            gap_info = {
                "query": query,
                "response": response,
                "missing_keywords": missing_keywords,
                "status": "knowledge gap detected"
            }
            self.gaps.append(gap_info)
            logging.warning(f"Knowledge gap detected: {gap_info}")
            return gap_info
        else:
            logging.info("No knowledge gap detected.")
            return {"status": "no gap"}

    def get_gaps(self) -> List[Dict]:
        """
        Returns all detected knowledge gaps.
        """
        return self.gaps
