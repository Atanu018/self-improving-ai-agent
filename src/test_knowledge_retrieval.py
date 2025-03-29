from knowledge_retrieval import KnowledgeRetriever

retriever = KnowledgeRetriever()

# Example missing keywords
missing_keywords = ["Reinforcement Learning", "Neural Networks"]

# Retrieve knowledge
retrieved_info = retriever.retrieve_knowledge(missing_keywords)

# Print results
for keyword, info in retrieved_info.items():
    print(f"\n🔍 Knowledge Retrieved for {keyword}:\n{info[:500]}...")  # Limit output
