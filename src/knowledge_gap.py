import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class KnowledgeGapDetector:
    def __init__(self):
        nltk.download("punkt")
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))

    def preprocess_text(self, text):
        if isinstance(text, dict):
            text = " ".join(str(value) for value in text.values())
        elif not isinstance(text, str):
            text = str(text)

        text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
        tokens = word_tokenize(text)
        return [word for word in tokens if word not in self.stop_words]

    def detect_gap(self, query, response, expected_keywords):
        response_keywords = self.preprocess_text(response)
        return [kw for kw in expected_keywords if kw not in response_keywords]
