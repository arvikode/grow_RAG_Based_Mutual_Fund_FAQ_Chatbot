"""
Unit tests for answer_generator.py module.
Tests RAG integration and answer generation.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.answer_generator import AnswerGenerator, get_answer_generator


class TestAnswerGenerator:
    """Test suite for AnswerGenerator class."""
    
    @pytest.fixture
    def mock_retriever(self):
        """Create a mock retriever."""
        retriever = Mock()
        retriever.retrieve_and_format.return_value = (
            "[Source 1] Test context",
            [{"scheme": "Test Scheme", "url": "https://test.com", "relevance_score": 0.85}]
        )
        return retriever
    
    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM."""
        llm = Mock()
        llm.create_prompt.return_value = "Test prompt"
        llm.generate.return_value = "Generated answer with [Source 1] citation"
        return llm
    
    def test_init_default(self):
        """Test AnswerGenerator initialization with defaults."""
        with patch('src.answer_generator.Retriever'), patch('src.answer_generator.LLM'):
            generator = AnswerGenerator()
            assert generator.k == 3
    
    def test_init_custom_k(self, mock_retriever, mock_llm):
        """Test AnswerGenerator initialization with custom k."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm, k=5)
        assert generator.k == 5
        assert generator.retriever == mock_retriever
        assert generator.llm == mock_llm
    
    def test_generate_answer_success(self, mock_retriever, mock_llm):
        """Test successful answer generation."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        
        result = generator.generate_answer("What is the expense ratio?")
        
        assert result['question'] == "What is the expense ratio?"
        assert result['answer'] == "Generated answer with [Source 1] citation"
        assert len(result['sources']) == 1
        assert result['retrieved_docs'] == 1
        assert 'timestamp' in result
        
        mock_retriever.retrieve_and_format.assert_called_once_with("What is the expense ratio?", k=3)
        mock_llm.create_prompt.assert_called_once()
        mock_llm.generate.assert_called_once()
    
    def test_generate_answer_custom_k(self, mock_retriever, mock_llm):
        """Test answer generation with custom k."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm, k=3)
        
        generator.generate_answer("Test question", k=5)
        
        mock_retriever.retrieve_and_format.assert_called_once_with("Test question", k=5)
    
    def test_generate_answer_no_sources(self, mock_llm):
        """Test answer generation when no sources are found."""
        mock_retriever = Mock()
        mock_retriever.retrieve_and_format.return_value = ("No relevant information found.", [])
        
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        result = generator.generate_answer("Unknown question")
        
        assert "don't have enough information" in result['answer']
        assert result['sources'] == []
        assert result['retrieved_docs'] == 0
        # LLM should not be called when no sources
        mock_llm.generate.assert_not_called()
    
    def test_generate_answer_llm_error(self, mock_retriever, mock_llm):
        """Test error handling when LLM fails."""
        mock_llm.generate.side_effect = Exception("API Error")
        
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        result = generator.generate_answer("Test question")
        
        assert "Error generating answer" in result['answer']
        assert 'error' in result
        assert result['error'] == "API Error"
    
    def test_generate_answer_custom_temperature(self, mock_retriever, mock_llm):
        """Test answer generation with custom temperature."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        
        generator.generate_answer("Test question", temperature=0.8)
        
        # Verify temperature was passed to LLM
        call_args = mock_llm.generate.call_args
        assert call_args[1]['temperature'] == 0.8
    
    def test_format_response(self, mock_retriever, mock_llm):
        """Test response formatting."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        
        result = {
            'question': 'What is the expense ratio?',
            'answer': 'The expense ratio is 1.05% [Source 1]',
            'sources': [
                {
                    'scheme': 'HDFC Flexi Cap',
                    'url': 'https://example.com',
                    'description': 'KIM PDF',
                    'relevance_score': 0.85
                }
            ],
            'timestamp': '2026-02-10T22:00:00',
            'retrieved_docs': 1
        }
        
        formatted = generator.format_response(result)
        
        assert 'What is the expense ratio?' in formatted
        assert 'The expense ratio is 1.05%' in formatted
        assert 'HDFC Flexi Cap' in formatted
        assert 'https://example.com' in formatted
        assert '0.85' in formatted or '0.8500' in formatted
        assert 'Retrieved 1 relevant documents' in formatted
    
    def test_format_response_no_sources(self, mock_retriever, mock_llm):
        """Test response formatting with no sources."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        
        result = {
            'question': 'Test?',
            'answer': 'No information available',
            'sources': [],
            'timestamp': '2026-02-10T22:00:00',
            'retrieved_docs': 0
        }
        
        formatted = generator.format_response(result)
        
        assert 'Test?' in formatted
        assert 'No information available' in formatted
        assert 'Retrieved 0 relevant documents' in formatted
    
    def test_answer_questions_batch(self, mock_retriever, mock_llm):
        """Test answering multiple questions in batch."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        
        questions = [
            "What is the expense ratio?",
            "What is the exit load?",
            "What is the minimum SIP?"
        ]
        
        results = generator.answer_questions(questions)
        
        assert len(results) == 3
        assert all('question' in r for r in results)
        assert all('answer' in r for r in results)
        assert mock_retriever.retrieve_and_format.call_count == 3
    
    def test_answer_questions_empty_list(self, mock_retriever, mock_llm):
        """Test answering empty question list."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        
        results = generator.answer_questions([])
        
        assert results == []
        mock_retriever.retrieve_and_format.assert_not_called()
    
    def test_timestamp_format(self, mock_retriever, mock_llm):
        """Test that timestamp is in ISO format."""
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        
        result = generator.generate_answer("Test?")
        
        # Verify timestamp can be parsed
        timestamp = result['timestamp']
        datetime.fromisoformat(timestamp)  # Should not raise
    
    def test_sources_metadata_preserved(self, mock_llm):
        """Test that source metadata is preserved."""
        mock_retriever = Mock()
        mock_retriever.retrieve_and_format.return_value = (
            "Context",
            [
                {
                    'scheme': 'Test Scheme',
                    'url': 'https://test.com',
                    'description': 'Test description',
                    'relevance_score': 0.95
                }
            ]
        )
        
        generator = AnswerGenerator(retriever=mock_retriever, llm=mock_llm)
        result = generator.generate_answer("Test?")
        
        assert result['sources'][0]['scheme'] == 'Test Scheme'
        assert result['sources'][0]['url'] == 'https://test.com'
        assert result['sources'][0]['description'] == 'Test description'
        assert result['sources'][0]['relevance_score'] == 0.95
    
    @patch('src.answer_generator.Retriever')
    @patch('src.answer_generator.LLM')
    def test_get_answer_generator(self, mock_llm_class, mock_retriever_class):
        """Test get_answer_generator helper function."""
        generator = get_answer_generator(k=5)
        
        assert isinstance(generator, AnswerGenerator)
        assert generator.k == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
