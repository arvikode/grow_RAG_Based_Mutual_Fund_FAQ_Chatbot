"""
Guardrails module for detecting and handling advice-seeking questions.
Ensures the chatbot only provides factual information, not investment advice.
"""
import re
from typing import Dict, Tuple
from datetime import datetime


class Guardrails:
    """
    Detects advice-seeking questions and provides appropriate refusals.
    Allows factual questions to proceed to the RAG pipeline.
    """
    
    # Keywords that indicate advice-seeking intent
    ADVICE_KEYWORDS = [
        "should i invest",
        "should i buy",
        "should i",
        "recommend",
        "suggest",
        "advice",
        "best fund",
        "better fund",
        "which fund",
        "how much to invest",
        "how much should i",
        "is it good",
        "is it worth",
        "is this good",
        "portfolio",
        "allocation",
        "diversify",
        "when to invest",
        "when should i",
        "good time to invest",
        "right time",
        "predict",
        "future returns",
        "will it grow",
        "will give",
        "guaranteed returns",
        "good investment",
        "good returns",
        "compare"
    ]
    
    # Patterns for advice-seeking questions
    ADVICE_PATTERNS = [
        r"^should i\b",
        r"^can i\b.*invest",
        r"^will\b.*\b(give|provide|return)",
        r"\bvs\b",  # Comparison questions
        r"\bversus\b",
        r"\bcompare\b",
        r"\bbetter than\b",
        r"\bworth investing\b",
        r"\bgood investment\b",
        r"^which\b.*\b(fund|better|best)"
    ]
    
    def __init__(self):
        """Initialize guardrails."""
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.ADVICE_PATTERNS]
        
        # Casual greetings and small talk
        self.greetings = [
            "hi", "hello", "hey", "greetings", "good morning", "good afternoon", 
            "good evening", "howdy", "hiya", "sup", "what's up", "whats up", "hello there"
        ]
        
        self.casual_questions = [
            "how are you", "how r u", "what can you do", "what do you do",
            "who are you", "help", "thanks", "thank you", "bye", "goodbye"
        ]
    
    def is_greeting(self, question: str) -> bool:
        """
        Check if the question is a casual greeting or small talk.
        
        Args:
            question: User's question
            
        Returns:
            True if greeting/casual, False otherwise
        """
        question_lower = question.lower().strip()
        
        # Check exact greetings
        if question_lower in self.greetings:
            return True
        
        # Check casual questions
        for casual in self.casual_questions:
            if casual in question_lower:
                return True
        
        return False
    
    def get_greeting_response(self, question: str) -> Dict:
        """
        Generate a response for greetings and casual questions.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with greeting response
        """
        question_lower = question.lower().strip()
        
        # Determine response based on question type
        if any(greeting in question_lower for greeting in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
            answer = "Hello! I'm a mutual fund FAQ chatbot. I can answer factual questions about HDFC mutual fund schemes. What would you like to know?"
        elif "how are you" in question_lower:
            answer = "I'm functioning well, thank you! I'm here to help you with factual information about HDFC mutual fund schemes. What would you like to know?"
        elif "what can you do" in question_lower or "what do you do" in question_lower:
            answer = """I can answer factual questions about 5 HDFC mutual fund schemes:
- HDFC Flexi Cap Fund
- HDFC Large Cap Fund
- HDFC ELSS Tax Saver
- HDFC Small Cap Fund
- HDFC Balanced Advantage Fund

You can ask about: expense ratio, exit load, minimum SIP amount, lock-in period, riskometer level, benchmark index, etc.

Type 'examples' to see sample questions!"""
        elif "who are you" in question_lower:
            answer = "I'm a mutual fund FAQ chatbot that provides factual information about HDFC mutual fund schemes. I don't provide investment advice, only facts from official sources."
        elif "help" in question_lower:
            answer = "I can help you with factual information about HDFC mutual funds. Try asking: 'What is the expense ratio of HDFC Flexi Cap Fund?' or type 'examples' for more sample questions."
        elif any(thanks in question_lower for thanks in ["thanks", "thank you"]):
            answer = "You're welcome! Feel free to ask more questions about HDFC mutual funds."
        elif any(bye in question_lower for bye in ["bye", "goodbye"]):
            answer = "Goodbye! Have a great day!"
        else:
            answer = "Hello! I'm here to answer factual questions about HDFC mutual fund schemes. What would you like to know?"
        
        return {
            "question": question,
            "answer": answer,
            "is_greeting": True,
            "timestamp": datetime.now().isoformat(),
            "sources": []
        }
    
    def is_advice_seeking(self, question: str) -> bool:
        """
        Determine if a question is seeking investment advice.
        
        Args:
            question: User's question
            
        Returns:
            True if question seeks advice, False if factual
        """
        question_lower = question.lower().strip()
        
        # Check keywords with word boundaries to avoid partial matches
        for keyword in self.ADVICE_KEYWORDS:
            # Use word boundaries for more precise matching
            if keyword in ["recommend", "suggest", "compare"]:
                # These need word boundaries to avoid matching "recommended", "suggested", etc.
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, question_lower):
                    return True
            elif keyword in question_lower:
                return True
        
        # Check patterns
        for pattern in self.compiled_patterns:
            if pattern.search(question_lower):
                return True
        
        return False
    
    def get_refusal_message(self, question: str) -> Dict:
        """
        Generate a polite refusal message for advice-seeking questions.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with refusal message and educational resources
        """
        refusal_template = """I cannot provide investment advice or recommendations.

However, I can share **factual information** about mutual fund schemes, such as:
- Expense ratios
- Exit loads
- Minimum SIP amounts
- Lock-in periods
- Riskometer levels
- Benchmark indices

**For personalized investment advice, please consult:**
- A SEBI-registered investment advisor
- Your financial planner
- An AMFI-registered mutual fund distributor

**Educational Resources:**
- [SEBI Investor Education](https://investor.sebi.gov.in/)
- [AMFI Investor Corner](https://www.amfiindia.com/investor-corner)
- [NISM Mutual Fund FAQs](https://www.nism.ac.in/)

Would you like to know any **factual information** about our covered schemes?"""
        
        return {
            "question": question,
            "answer": refusal_template,
            "is_advice_refusal": True,
            "timestamp": datetime.now().isoformat(),
            "sources": []
        }
    
    def check_and_respond(self, question: str) -> Tuple[bool, Dict]:
        """
        Check if question seeks advice and return appropriate response.
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (is_advice, response_dict)
            - is_advice: True if advice-seeking, False if factual
            - response_dict: Refusal message if advice, None if factual
        """
        if self.is_advice_seeking(question):
            return True, self.get_refusal_message(question)
        return False, None
    
    def get_example_factual_questions(self) -> list:
        """
        Get example factual questions users can ask.
        
        Returns:
            List of example questions
        """
        return [
            "What is the expense ratio of HDFC Flexi Cap Fund?",
            "What is the exit load for HDFC Large Cap Fund?",
            "What is the minimum SIP amount for HDFC ELSS Tax Saver?",
            "What is the lock-in period for HDFC ELSS Tax Saver?",
            "What is the riskometer level of HDFC Small Cap Fund?",
            "What is the benchmark index for HDFC Balanced Advantage Fund?",
            "How do I download my mutual fund statement?"
        ]
    
    def get_example_advice_questions(self) -> list:
        """
        Get example advice-seeking questions (for testing).
        
        Returns:
            List of advice-seeking questions
        """
        return [
            "Should I invest in HDFC Flexi Cap Fund?",
            "Which fund is better: HDFC Large Cap or HDFC Small Cap?",
            "How much should I invest in HDFC ELSS?",
            "Is HDFC Balanced Advantage Fund a good investment?",
            "When is the right time to invest in mutual funds?",
            "Can you recommend a fund for me?",
            "HDFC Flexi Cap vs HDFC Large Cap - which is better?",
            "Will HDFC Small Cap Fund give good returns?"
        ]


def get_guardrails() -> Guardrails:
    """
    Get Guardrails instance.
    
    Returns:
        Configured Guardrails instance
    """
    return Guardrails()


if __name__ == "__main__":
    # Test the guardrails
    guardrails = get_guardrails()
    
    print("Testing Guardrails Module")
    print("=" * 80)
    
    # Test factual questions
    print("\n✅ FACTUAL QUESTIONS (Should Pass):")
    for q in guardrails.get_example_factual_questions()[:3]:
        is_advice, _ = guardrails.check_and_respond(q)
        status = "❌ BLOCKED" if is_advice else "✅ ALLOWED"
        print(f"{status}: {q}")
    
    # Test advice questions
    print("\n🚫 ADVICE QUESTIONS (Should Block):")
    for q in guardrails.get_example_advice_questions()[:3]:
        is_advice, response = guardrails.check_and_respond(q)
        status = "✅ BLOCKED" if is_advice else "❌ ALLOWED"
        print(f"{status}: {q}")
