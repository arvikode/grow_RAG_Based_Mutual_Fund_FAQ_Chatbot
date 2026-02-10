from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_embedding_function():
    """Return the singleton embedding function."""
    # Using a lightweight, high-performance model suitable for CPU usage
    # all-MiniLM-L6-v2 is a standard choice for tasks like this
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings
