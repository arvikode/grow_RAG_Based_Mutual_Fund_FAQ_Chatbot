import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure stdout for UTF-8 to handle Unicode characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from src.vector_store import VectorStore

def test_retrieval():
    print("Testing RAG Retrieval...")
    
    vector_store = VectorStore()
    
    test_queries = [
        "What is the expense ratio of HDFC Flexi Cap Fund?",
        "What is the exit load for HDFC Large Cap Fund?",
        "Minimum SIP amount for HDFC Small Cap?",
        "Does HDFC ELSS Tax Saver have a lock-in period?",
        "What is the risk level of HDFC Balanced Advantage Fund?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = vector_store.query(query, k=1)
        
        if results:
            doc, score = results[0]
            print(f"Top Result (Score: {score:.4f}):")
            print(f"Content: {doc.page_content[:200]}...")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        else:
            print("No results found.")

if __name__ == "__main__":
    test_retrieval()
