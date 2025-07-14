from langchain_huggingface import HuggingFaceEmbeddings

# Initialize the embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text = "The capital of India is New Delhi."
embedding_vector = embedding.embed_query(text)
print(embedding_vector)