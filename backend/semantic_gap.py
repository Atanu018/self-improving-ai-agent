from sentence_transformers import SentenceTransformer

class SemanticGap:
    """Converts text queries into embeddings to find the best match."""
    
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight NLP model
    
    def get_embedding(self, text):
        """Returns numerical vector representation of a given text."""
        return self.model.encode(text)
