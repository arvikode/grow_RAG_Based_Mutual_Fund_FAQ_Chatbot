"""
Command-line interface for testing the Mutual Fund FAQ Chatbot.
Allows interactive Q&A in the terminal.
"""
import sys
import os
import warnings
import time
import threading
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.guardrails import get_guardrails
from src.answer_generator import get_answer_generator


class Spinner:
    """Simple loading spinner."""
    
    def __init__(self, message="Loading"):
        self.message = message
        self.running = False
        self.thread = None
    
    def spin(self):
        """Spin animation."""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while self.running:
            sys.stdout.write(f'\r{chars[i % len(chars)]} {self.message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def start(self):
        """Start spinner."""
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
    
    def stop(self):
        """Stop spinner."""
        self.running = False
        if self.thread:
            self.thread.join()


def print_header():
    """Print minimal header."""
    print("\n" + "="*60)
    print("💰 MUTUAL FUND FAQ CHATBOT")
    print("="*60)
    print("\nCovered Schemes: HDFC Flexi Cap, Large Cap, ELSS, Small Cap, Balanced Advantage")
    print("\nCommands: 'examples' | 'quit' | 'exit'")
    print("="*60 + "\n")


def print_examples(guardrails):
    """Print example questions."""
    print("\n✅ EXAMPLE QUESTIONS:")
    examples = guardrails.get_example_factual_questions()
    for i, question in enumerate(examples[:5], 1):
        print(f"  {i}. {question}")
    print()


def format_response(response):
    """Format response for terminal."""
    lines = []
    
    # Answer
    if response.get('is_advice_refusal'):
        lines.append("\n🚫 ADVICE REFUSAL:")
        lines.append("I cannot provide investment advice. Please consult a SEBI-registered advisor.")
        lines.append("\nFor factual info, ask about: expense ratio, exit load, min SIP, lock-in, etc.")
    else:
        lines.append(f"\n💡 ANSWER:")
        lines.append(response['answer'])
        
        # Sources (compact)
        if response.get('sources') and len(response['sources']) > 0:
            lines.append(f"\n📚 SOURCES ({len(response['sources'])}):")
            for i, source in enumerate(response['sources'], 1):
                scheme = source.get('scheme', 'Unknown')
                lines.append(f"  [{i}] {scheme}")
    
    return "\n".join(lines)


def main():
    """Main CLI function."""
    print_header()
    
    # Initialize with spinner
    spinner = Spinner("Initializing chatbot")
    spinner.start()
    
    try:
        guardrails = get_guardrails()
        answer_generator = get_answer_generator(k=3)
        spinner.stop()
        print("✅ Ready!\n")
    except Exception as e:
        spinner.stop()
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Run 'python src/pipeline.py' to load documents")
        print("  2. Set valid GEMINI_API_KEY in .env")
        return
    
    # Main loop
    while True:
        try:
            # Get input
            question = input("💬 Ask: ").strip()
            
            # Handle commands
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if question.lower() == 'examples':
                print_examples(guardrails)
                continue
            
            if not question:
                continue
            
            # Process with spinner
            spinner = Spinner("Thinking")
            spinner.start()
            
            # Check for greetings first
            if guardrails.is_greeting(question):
                response = guardrails.get_greeting_response(question)
                spinner.stop()
                print(format_response(response))
                print()
                continue
            
            # Check guardrails for advice
            is_advice, refusal_response = guardrails.check_and_respond(question)
            
            if is_advice:
                response = refusal_response
            else:
                try:
                    response = answer_generator.generate_answer(question)
                except Exception as e:
                    response = {
                        "question": question,
                        "answer": f"Error: {str(e)}",
                        "sources": [],
                        "timestamp": datetime.now().isoformat()
                    }
            
            spinner.stop()
            print(format_response(response))
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


if __name__ == "__main__":
    main()

