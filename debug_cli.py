# Debug script to inspect retrieved context with safe printing
import sys
import os
import io

# Set stdout to handle utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'src')

from retrieval import Retriever
from answer_generator import get_answer_generator

def debug_query():
    try:
        print("Initializing components...")
        retriever = Retriever(k=5)
        generator = get_answer_generator(k=5)
        
        question = "What is the exit load of HDFC Flexi Cap Fund?"
        print(f"\nQuestion: {question}\n")
        
        # 1. Check Retrieval
        context, sources = retriever.retrieve_and_format(question)
        
        print(f"Retrieved {len(sources)} sources")
        print("=" * 80)
        print("CONTEXT:")
        print("=" * 80)
        print(context) 
        print("=" * 80)
        
        # 2. Check Generation
        print("\nGeneratig answer...")
        result = generator.generate_answer(question)
        print("\n=== FULL ANSWER ===")
        print(result['answer'])
        
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_query()
