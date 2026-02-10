"""
Unit tests for llm.py module.
Tests LLM wrapper, providers, and prompt generation.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm import LLM, GeminiProvider, GrokProvider, get_llm


class TestGeminiProvider:
    """Test suite for GeminiProvider class."""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_init(self, mock_model_class, mock_configure):
        """Test Gemini provider initialization."""
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        provider = GeminiProvider("test_api_key", "gemini-1.5-flash")
        
        mock_configure.assert_called_once_with(api_key="test_api_key")
        mock_model_class.assert_called_once_with("gemini-1.5-flash")
        assert provider.model == mock_model
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_generate_success(self, mock_model_class, mock_configure):
        """Test successful text generation."""
        mock_response = Mock()
        mock_response.text = "Generated response"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        provider = GeminiProvider("test_key")
        result = provider.generate("Test prompt", temperature=0.5, max_tokens=500)
        
        assert result == "Generated response"
        mock_model.generate_content.assert_called_once()
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_generate_error(self, mock_model_class, mock_configure):
        """Test error handling in generation."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model
        
        provider = GeminiProvider("test_key")
        
        with pytest.raises(RuntimeError, match="Gemini API error"):
            provider.generate("Test prompt")


class TestGrokProvider:
    """Test suite for GrokProvider class."""
    
    @patch('openai.OpenAI')
    def test_init(self, mock_openai_class):
        """Test Grok provider initialization."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        provider = GrokProvider("test_api_key", "grok-beta")
        
        mock_openai_class.assert_called_once_with(
            api_key="test_api_key",
            base_url="https://api.x.ai/v1"
        )
        assert provider.client == mock_client
        assert provider.model == "grok-beta"
    
    @patch('openai.OpenAI')
    def test_generate_success(self, mock_openai_class):
        """Test successful text generation."""
        mock_message = Mock()
        mock_message.content = "Generated response"
        
        mock_choice = Mock()
        mock_choice.message = mock_message
        
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        provider = GrokProvider("test_key")
        result = provider.generate("Test prompt", temperature=0.5, max_tokens=500)
        
        assert result == "Generated response"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('openai.OpenAI')
    def test_generate_error(self, mock_openai_class):
        """Test error handling in generation."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client
        
        provider = GrokProvider("test_key")
        
        with pytest.raises(RuntimeError, match="Grok API error"):
            provider.generate("Test prompt")


class TestLLM:
    """Test suite for LLM wrapper class."""
    
    @patch.dict(os.environ, {
        'LLM_PROVIDER': 'gemini',
        'GEMINI_API_KEY': 'test_gemini_key',
        'GEMINI_MODEL': 'gemini-1.5-flash',
        'TEMPERATURE': '0.2',
        'MAX_TOKENS': '800'
    })
    @patch('src.llm.GeminiProvider')
    def test_init_gemini_from_env(self, mock_gemini_provider):
        """Test LLM initialization with Gemini from environment."""
        mock_provider_instance = Mock()
        mock_gemini_provider.return_value = mock_provider_instance
        
        llm = LLM()
        
        assert llm.provider_name == 'gemini'
        assert llm.temperature == 0.2
        assert llm.max_tokens == 800
        mock_gemini_provider.assert_called_once_with('test_gemini_key', 'gemini-1.5-flash')
    
    @patch.dict(os.environ, {
        'LLM_PROVIDER': 'grok',
        'GROK_API_KEY': 'test_grok_key',
        'GROK_MODEL': 'grok-beta'
    })
    @patch('src.llm.GrokProvider')
    def test_init_grok_from_env(self, mock_grok_provider):
        """Test LLM initialization with Grok from environment."""
        mock_provider_instance = Mock()
        mock_grok_provider.return_value = mock_provider_instance
        
        llm = LLM()
        
        assert llm.provider_name == 'grok'
        mock_grok_provider.assert_called_once_with('test_grok_key', 'grok-beta')
    
    @patch('src.llm.GeminiProvider')
    def test_init_with_arguments(self, mock_gemini_provider):
        """Test LLM initialization with explicit arguments."""
        mock_provider_instance = Mock()
        mock_gemini_provider.return_value = mock_provider_instance
        
        llm = LLM(provider='gemini', api_key='custom_key', model='custom-model')
        
        mock_gemini_provider.assert_called_once_with('custom_key', 'custom-model')
    
    @patch.dict(os.environ, {'LLM_PROVIDER': 'gemini', 'GEMINI_API_KEY': 'your_gemini_api_key_here'})
    def test_init_invalid_api_key(self):
        """Test error when API key is not set."""
        with pytest.raises(ValueError, match="GEMINI_API_KEY not set"):
            LLM()
    
    def test_init_unknown_provider(self):
        """Test error with unknown provider."""
        with pytest.raises(ValueError, match="Unknown provider"):
            LLM(provider='unknown', api_key='test_key')
    
    @patch('src.llm.GeminiProvider')
    def test_generate(self, mock_gemini_provider):
        """Test generate method."""
        mock_provider_instance = Mock()
        mock_provider_instance.generate.return_value = "Generated text"
        mock_gemini_provider.return_value = mock_provider_instance
        
        llm = LLM(provider='gemini', api_key='test_key')
        result = llm.generate("Test prompt")
        
        assert result == "Generated text"
        mock_provider_instance.generate.assert_called_once()
    
    @patch('src.llm.GeminiProvider')
    def test_generate_with_custom_params(self, mock_gemini_provider):
        """Test generate with custom temperature and max_tokens."""
        mock_provider_instance = Mock()
        mock_provider_instance.generate.return_value = "Generated text"
        mock_gemini_provider.return_value = mock_provider_instance
        
        llm = LLM(provider='gemini', api_key='test_key')
        llm.generate("Test prompt", temperature=0.8, max_tokens=1500)
        
        # Verify custom params were passed
        call_args = mock_provider_instance.generate.call_args
        assert call_args[1]['temperature'] == 0.8
        assert call_args[1]['max_tokens'] == 1500
    
    @patch('src.llm.GeminiProvider')
    def test_create_prompt(self, mock_gemini_provider):
        """Test prompt creation for Q&A."""
        mock_provider_instance = Mock()
        mock_gemini_provider.return_value = mock_provider_instance
        
        llm = LLM(provider='gemini', api_key='test_key')
        
        question = "What is the expense ratio?"
        context = "[Source 1] HDFC Flexi Cap has 1.05% expense ratio"
        sources = [{"scheme": "HDFC Flexi Cap", "url": "https://example.com"}]
        
        prompt = llm.create_prompt(question, context, sources)
        
        assert "What is the expense ratio?" in prompt
        assert "HDFC Flexi Cap has 1.05% expense ratio" in prompt
        assert "factual" in prompt.lower()
        assert "cite sources" in prompt.lower() or "citation" in prompt.lower()
        assert "investment advice" in prompt.lower()
    
    @patch('src.llm.GeminiProvider')
    def test_create_prompt_includes_timestamp(self, mock_gemini_provider):
        """Test that prompt includes timestamp."""
        mock_provider_instance = Mock()
        mock_gemini_provider.return_value = mock_provider_instance
        
        llm = LLM(provider='gemini', api_key='test_key')
        prompt = llm.create_prompt("Test?", "Context", [])
        
        assert "Last updated:" in prompt or "updated" in prompt.lower()
    
    @patch.dict(os.environ, {'LLM_PROVIDER': 'gemini', 'GEMINI_API_KEY': 'test_key'})
    @patch('src.llm.GeminiProvider')
    def test_get_llm(self, mock_gemini_provider):
        """Test get_llm helper function."""
        mock_provider_instance = Mock()
        mock_gemini_provider.return_value = mock_provider_instance
        
        llm = get_llm()
        
        assert isinstance(llm, LLM)
        assert llm.provider_name == 'gemini'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
