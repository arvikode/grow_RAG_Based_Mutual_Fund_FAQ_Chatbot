"""
Comprehensive test script for the Mutual Fund FAQ Chatbot.
Tests 30 different prompts to validate greeting handling, guardrails, and RAG responses.
"""
import sys
import os
import warnings

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Suppress warnings
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.guardrails import get_guardrails
from src.answer_generator import get_answer_generator


# Test prompts organized by category
TEST_PROMPTS = {
    "Greetings & Casual (Should respond directly)": [
        "hi",
        "hello there",
        "good morning",
        "how are you?",
        "what can you do?",
        "who are you?",
        "help me",
        "thanks!",
    ],
    
    "Factual Questions (Should use RAG)": [
        "What is the expense ratio of HDFC Flexi Cap Fund?",
        "What is the exit load for HDFC Large Cap Fund?",
        "What is the minimum SIP amount for HDFC ELSS?",
        "What is the lock-in period for ELSS?",
        "What is the riskometer level of HDFC Small Cap Fund?",
        "What is the benchmark index for HDFC Balanced Advantage Fund?",
        "How do I download my mutual fund statement?",
    ],
    
    "Advice-Seeking (Should be blocked)": [
        "Should I invest in HDFC Flexi Cap Fund?",
        "Which fund is better: HDFC Large Cap or Small Cap?",
        "Can you recommend a fund for me?",
        "How much should I invest?",
        "Is HDFC ELSS a good investment?",
        "When should I invest in mutual funds?",
    ],
    
    "Edge Cases & Tricky Questions": [
        "",  # Empty
        "What?",  # Single word
        "Tell me everything about HDFC funds",  # Too broad
        "What is the NAV?",  # Missing fund name
        "expense ratio",  # Incomplete question
        "HDFC Flexi Cap vs HDFC Large Cap",  # Comparison (should block)
        "What is the recommended minimum SIP?",  # Has "recommend" but factual
        "Compare HDFC ELSS and HDFC Small Cap",  # Comparison (should block)
        "What are the tax benefits of ELSS?",  # May not be in docs
    ],
}


def print_separator(char="=", length=80):
    """Print separator line."""
    print(char * length)


def test_chatbot():
    """Run comprehensive chatbot tests."""
    print("\n" + "="*80)
    print("COMPREHENSIVE CHATBOT TEST - 30 PROMPTS")
    print("="*80)
    
    # Initialize
    print("\n🔧 Initializing chatbot...")
    try:
        guardrails = get_guardrails()
        answer_generator = get_answer_generator(k=3)
        print("✅ Chatbot initialized successfully!\n")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Track results
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    results = []
    
    # Run tests
    for category, prompts in TEST_PROMPTS.items():
        print_separator("-")
        print(f"\n📋 CATEGORY: {category}")
        print_separator("-")
        
        for i, question in enumerate(prompts, 1):
            total_tests += 1
            
            # Skip empty questions
            if not question:
                print(f"\n[{total_tests}] SKIPPED: Empty question")
                continue
            
            print(f"\n[{total_tests}] TESTING: \"{question}\"")
            
            try:
                # Determine expected behavior
                is_greeting = guardrails.is_greeting(question)
                is_advice = guardrails.is_advice_seeking(question)
                
                # Process question
                if is_greeting:
                    response = guardrails.get_greeting_response(question)
                    route = "GREETING"
                elif is_advice:
                    _, response = guardrails.check_and_respond(question)
                    route = "ADVICE_BLOCKED"
                else:
                    response = answer_generator.generate_answer(question)
                    route = "RAG_PIPELINE"
                
                # Check response
                has_answer = bool(response.get('answer'))
                answer_preview = response['answer'][:100] + "..." if len(response['answer']) > 100 else response['answer']
                
                # Validate
                status = "✅ PASS"
                
                # Category-specific validation
                if "Greetings" in category and route != "GREETING":
                    status = "❌ FAIL"
                    failed_tests += 1
                elif "Factual" in category and route != "RAG_PIPELINE":
                    status = "❌ FAIL"
                    failed_tests += 1
                elif "Advice" in category and route != "ADVICE_BLOCKED":
                    status = "❌ FAIL"
                    failed_tests += 1
                else:
                    passed_tests += 1
                
                # Print result
                print(f"   Route: {route}")
                print(f"   Answer: {answer_preview}")
                print(f"   Sources: {len(response.get('sources', []))}")
                print(f"   Status: {status}")
                
                # Store result
                results.append({
                    'question': question,
                    'route': route,
                    'status': status,
                    'category': category
                })
                
            except Exception as e:
                print(f"   ❌ ERROR: {str(e)}")
                failed_tests += 1
                results.append({
                    'question': question,
                    'route': 'ERROR',
                    'status': '❌ FAIL',
                    'category': category,
                    'error': str(e)
                })
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"\nTotal Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Failed tests detail
    if failed_tests > 0:
        print("\n" + "="*80)
        print("FAILED TESTS")
        print("="*80)
        for result in results:
            if result['status'] == '❌ FAIL':
                print(f"\n❌ {result['question']}")
                print(f"   Category: {result['category']}")
                print(f"   Route: {result['route']}")
                if 'error' in result:
                    print(f"   Error: {result['error']}")
    
    # Route distribution
    print("\n" + "="*80)
    print("ROUTE DISTRIBUTION")
    print("="*80)
    route_counts = {}
    for result in results:
        route = result['route']
        route_counts[route] = route_counts.get(route, 0) + 1
    
    for route, count in sorted(route_counts.items()):
        print(f"{route}: {count}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_chatbot()
