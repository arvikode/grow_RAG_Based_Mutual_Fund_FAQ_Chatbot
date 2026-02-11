"""
Unit tests for guardrails.py module.
Tests advice detection, refusal messages, and edge cases.
"""
import os
import sys
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.guardrails import Guardrails, get_guardrails


class TestGuardrails:
    """Test suite for Guardrails class."""
    
    @pytest.fixture
    def guardrails(self):
        """Create a guardrails instance."""
        return Guardrails()
    
    def test_init(self, guardrails):
        """Test guardrails initialization."""
        assert guardrails is not None
        assert len(guardrails.ADVICE_KEYWORDS) > 0
        assert len(guardrails.ADVICE_PATTERNS) > 0
        assert len(guardrails.compiled_patterns) > 0
    
    def test_factual_questions_allowed(self, guardrails):
        """Test that factual questions are allowed."""
        factual_questions = [
            "What is the expense ratio of HDFC Flexi Cap Fund?",
            "What is the exit load for HDFC Large Cap Fund?",
            "What is the minimum SIP amount?",
            "What is the lock-in period for ELSS?",
            "What is the riskometer level?",
            "What is the benchmark index?",
            "How do I download my statement?"
        ]
        
        for question in factual_questions:
            assert not guardrails.is_advice_seeking(question), f"Incorrectly blocked: {question}"
    
    def test_advice_questions_blocked_keywords(self, guardrails):
        """Test that advice questions with keywords are blocked."""
        advice_questions = [
            "Should I invest in HDFC Flexi Cap Fund?",
            "Can you recommend a fund for me?",
            "Which fund is the best?",
            "Please suggest a good fund",
            "Is this a good investment?",
            "How much should I invest?",
            "When should I invest?",
            "Will this fund give good returns?"
        ]
        
        for question in advice_questions:
            assert guardrails.is_advice_seeking(question), f"Failed to block: {question}"
    
    def test_advice_questions_blocked_patterns(self, guardrails):
        """Test that advice questions with patterns are blocked."""
        pattern_questions = [
            "Should I buy this fund?",
            "HDFC Flexi Cap vs HDFC Large Cap",
            "Compare HDFC Small Cap and HDFC Large Cap",
            "Which is better than HDFC ELSS?",
            "Is it worth investing in this fund?"
        ]
        
        for question in pattern_questions:
            assert guardrails.is_advice_seeking(question), f"Failed to block: {question}"
    
    def test_case_insensitive_detection(self, guardrails):
        """Test that detection is case-insensitive."""
        questions = [
            "SHOULD I INVEST?",
            "should i invest?",
            "Should I Invest?",
            "sHoUlD i InVeSt?"
        ]
        
        for question in questions:
            assert guardrails.is_advice_seeking(question)
    
    def test_get_refusal_message(self, guardrails):
        """Test refusal message generation."""
        question = "Should I invest in HDFC Flexi Cap?"
        response = guardrails.get_refusal_message(question)
        
        assert 'question' in response
        assert 'answer' in response
        assert 'is_advice_refusal' in response
        assert 'timestamp' in response
        assert 'sources' in response
        
        assert response['question'] == question
        assert response['is_advice_refusal'] is True
        assert len(response['sources']) == 0
        
        # Check refusal message content
        answer = response['answer']
        assert 'cannot provide investment advice' in answer.lower()
        assert 'SEBI' in answer
        assert 'AMFI' in answer
        assert 'factual information' in answer.lower()
    
    def test_check_and_respond_advice(self, guardrails):
        """Test check_and_respond for advice questions."""
        question = "Should I invest in this fund?"
        is_advice, response = guardrails.check_and_respond(question)
        
        assert is_advice is True
        assert response is not None
        assert response['is_advice_refusal'] is True
    
    def test_check_and_respond_factual(self, guardrails):
        """Test check_and_respond for factual questions."""
        question = "What is the expense ratio?"
        is_advice, response = guardrails.check_and_respond(question)
        
        assert is_advice is False
        assert response is None
    
    def test_get_example_factual_questions(self, guardrails):
        """Test getting example factual questions."""
        examples = guardrails.get_example_factual_questions()
        
        assert len(examples) > 0
        assert all(isinstance(q, str) for q in examples)
        
        # Verify examples are actually factual
        for question in examples:
            assert not guardrails.is_advice_seeking(question)
    
    def test_get_example_advice_questions(self, guardrails):
        """Test getting example advice questions."""
        examples = guardrails.get_example_advice_questions()
        
        assert len(examples) > 0
        assert all(isinstance(q, str) for q in examples)
        
        # Verify examples are actually advice-seeking
        for question in examples:
            assert guardrails.is_advice_seeking(question)
    
    def test_edge_case_empty_question(self, guardrails):
        """Test handling of empty questions."""
        assert not guardrails.is_advice_seeking("")
        assert not guardrails.is_advice_seeking("   ")
    
    def test_edge_case_single_word(self, guardrails):
        """Test handling of single-word questions."""
        assert not guardrails.is_advice_seeking("What?")
        assert not guardrails.is_advice_seeking("How?")
        assert guardrails.is_advice_seeking("Recommend")
    
    def test_partial_keyword_match(self, guardrails):
        """Test that partial keyword matches work correctly."""
        # Should match
        assert guardrails.is_advice_seeking("I want to invest, should I?")
        assert guardrails.is_advice_seeking("Can you recommend something?")
        
        # Should not match (different context)
        assert not guardrails.is_advice_seeking("What is the recommended minimum SIP?")
    
    def test_comparison_questions(self, guardrails):
        """Test detection of comparison questions."""
        comparison_questions = [
            "Fund A vs Fund B",
            "HDFC Flexi Cap versus HDFC Large Cap",
            "Compare these two funds"
        ]
        
        for question in comparison_questions:
            assert guardrails.is_advice_seeking(question)
    
    def test_get_guardrails_helper(self):
        """Test get_guardrails helper function."""
        guardrails = get_guardrails()
        assert isinstance(guardrails, Guardrails)
    
    def test_refusal_message_structure(self, guardrails):
        """Test that refusal message has proper structure."""
        response = guardrails.get_refusal_message("Test question")
        
        # Check all required fields
        required_fields = ['question', 'answer', 'is_advice_refusal', 'timestamp', 'sources']
        for field in required_fields:
            assert field in response
        
        # Check field types
        assert isinstance(response['question'], str)
        assert isinstance(response['answer'], str)
        assert isinstance(response['is_advice_refusal'], bool)
        assert isinstance(response['timestamp'], str)
        assert isinstance(response['sources'], list)
    
    def test_educational_links_in_refusal(self, guardrails):
        """Test that refusal message includes educational links."""
        response = guardrails.get_refusal_message("Test")
        answer = response['answer']
        
        # Check for educational resource mentions
        assert 'SEBI' in answer
        assert 'AMFI' in answer
        assert 'NISM' in answer or 'educational' in answer.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
