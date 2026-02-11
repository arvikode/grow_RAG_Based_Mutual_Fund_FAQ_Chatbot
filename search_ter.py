# Search for expense ratio in all documents
import sys
import os
sys.path.insert(0, 'src')

from vector_store import VectorStore

try:
    print("Searching for expense ratio data in vector store...")
    vs = VectorStore()
    
    # Try different search queries
    queries = [
        "expense ratio 1.05",
        "TER percentage HDFC Flexi Cap",
        "management fee HDFC Flexi Cap",
        "annual charges HDFC Flexi Cap",
        "0.5% 1% 1.5% 2% expense"
    ]
    
    for query in queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print('='*80)
        results = vs.query(query, k=3)
        
        if results:
            for i, (doc, score) in enumerate(results, 1):
                print(f"\n[{i}] Score: {score:.4f}")
                print(f"Scheme: {doc.metadata.get('scheme', 'Unknown')}")
                print(f"Content preview: {doc.page_content[:300]}...")
        else:
            print("No results found")
            
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
