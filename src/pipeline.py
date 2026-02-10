import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader
from src.vector_store import VectorStore

def main():
    print("Starting RAG Pipeline...")
    
    # 1. Clear existing DB (optional, for clean build)
    vector_store = VectorStore()
    vector_store.clear()
    
    # 2. Load and Process Data
    loader = DataLoader()
    print("Loading data from URLs...")
    documents = loader.load_and_process_all()
    
    if not documents:
        print("No documents were processed. Exiting.")
        return

    # 3. Store in Vector DB
    print(f"Storing {len(documents)} document chunks in Vector DB...")
    vector_store.add_documents(documents)
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
