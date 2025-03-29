from knowledge_storage import KnowledgeStorage

storage = KnowledgeStorage()

# Sample test data
new_knowledge = {
    "Reinforcement Learning": "A machine learning paradigm focused on training agents through rewards and punishments.",
    "Generative AI": "AI models that create new data samples, such as images, text, or music, based on patterns learned from training data.",
    "Explainable AI": "A field of AI that focuses on making AI decision-making processes more transparent and interpretable.",
    "Transfer Learning": "A technique where a pre-trained model is adapted to a new but related task, reducing training time and data requirements."
}

storage.update_knowledge(new_knowledge)

# Retrieve and print knowledge to verify
print(storage.get_knowledge("Reinforcement Learning"))
print(storage.get_knowledge("Generative AI"))
print(storage.get_knowledge("Explainable AI"))
print(storage.get_knowledge("Transfer Learning"))