# Test script to see what context is being retrieved
import sys
import os
sys.path.insert(0, 'src')

from retrieval import Retriever

try:
    print("Initializing retriever...")
    retriever = Retriever(k=5)  # Get more documents
    
    question = "What is the expense ratio of HDFC Flexi Cap Fund?"
    print(f"\nQuestion: {question}\n")
    
    context, sources = retriever.retrieve_and_format(question)
    
    print(f"Retrieved {len(sources)} sources\n")
    print("=" * 80)
    print("CONTEXT BEING SENT TO LLM:")
    print("=" * 80)
    print(context[:2000])  # First 2000 chars
    print("\n... (truncated for display)\n")
    
    print("=" * 80)
    print("SOURCES:")
    print("=" * 80)
    for i, src in enumerate(sources, 1):
        print(f"\n[{i}] {src['scheme']}")
        print(f"    URL: {src['url'][:70]}...")
        print(f"    Relevance: {src['relevance_score']:.4f}")
    
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
