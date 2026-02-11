# Enhanced test script to see full LLM response
import sys
import os
sys.path.insert(0, 'src')

from answer_generator import get_answer_generator

try:
    print("Initializing answer generator...")
    generator = get_answer_generator(k=3)
    
    print("\nTesting question...")
    question = "What is the expense ratio of HDFC Flexi Cap Fund?"
    result = generator.generate_answer(question)
    
    print("\n=== FULL RESULT ===")
    print(f"Question: {result['question']}")
    print(f"\nAnswer (length={len(result['answer'])}):")
    print(result['answer'])
    print(f"\n\nSources ({len(result.get('sources', []))}):")
    for i, src in enumerate(result.get('sources', []), 1):
        print(f"  [{i}] {src.get('scheme', 'Unknown')}")
        print(f"      URL: {src.get('url', 'N/A')[:80]}...")
        print(f"      Relevance: {src.get('relevance_score', 0):.4f}")
    
    if result.get('error'):
        print(f"\nERROR: {result['error']}")
    
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
