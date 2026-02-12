import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from vector_store import VectorStore
from langchain_core.documents import Document

def ingest_data():
    print("Starting data ingestion...")
    
    # Initialize loader
    loader = DataLoader("official-urls.csv")
    
    # Load and process documents
    print("Loading documents from URLs...")
    raw_docs = loader.load_and_process_all()
    
    if not raw_docs:
        print("No documents loaded!")
        return

    print(f"Loaded {len(raw_docs)} document chunks.")
    
    # Convert to LangChain Documents
    documents = []
    for doc in raw_docs:
        # Check if it's already a Document object or needs conversion
        if isinstance(doc, Document):
            documents.append(doc)
        else:
            # Assuming raw_docs has page_content and metadata if not Document objects
            # Adjust based on actual return type of loader.load_and_process_all()
            # Inspecting data_loader.py, it likely returns Document objects directly
            # due to text_splitter.create_documents
            documents.append(doc)

    # Initialize vector store
    print("Initializing vector store...")
    vector_store = VectorStore()
    
    # Add to vector store
    print("Adding documents to vector store...")
    count = vector_store.add_documents(documents)
    
    print(f"Successfully added {count} documents to vector store.")
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_data()
