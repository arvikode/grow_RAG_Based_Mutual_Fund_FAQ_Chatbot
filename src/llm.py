"""
LLM wrapper module supporting multiple providers (Gemini, Grok).
Handles API calls, prompt formatting, and error handling.
"""
import os
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider:
    """Base class for LLM providers."""
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM."""
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """Google Gemini API provider."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google Gemini API key
            model: Model name (default: gemini-1.5-flash)
        """
        try:
            import google.generativeai as genai
            self.genai = genai
        except ImportError:
            raise ImportError(
                "google-generativeai not installed. "
                "Install with: pip install google-generativeai"
            )
        
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel(model)
    
    def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 1000) -> str:
        """
        Generate response using Gemini.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
        """
        try:
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")


class GrokProvider(LLMProvider):
    """Grok API provider (using OpenAI-compatible API)."""
    
    def __init__(self, api_key: str, model: str = "grok-beta"):
        """
        Initialize Grok provider.
        
        Args:
            api_key: Grok API key
            model: Model name (default: grok-beta)
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai not installed. "
                "Install with: pip install openai"
            )
        
        # Grok uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 1000) -> str:
        """
        Generate response using Grok.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Grok API error: {str(e)}")


class LLM:
    """
    LLM wrapper that supports multiple providers.
    Automatically selects provider based on environment variables.
    """
    
    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize LLM wrapper.
        
        Args:
            provider: LLM provider ('gemini' or 'grok'). Defaults to env var LLM_PROVIDER
            api_key: API key. Defaults to env var based on provider
            model: Model name. Defaults to env var based on provider
        """
        # Get provider from env or argument
        self.provider_name = provider or os.getenv("LLM_PROVIDER", "gemini")
        
        # Initialize provider
        if self.provider_name == "gemini":
            api_key = api_key or os.getenv("GEMINI_API_KEY")
            model = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            
            if not api_key or api_key == "your_gemini_api_key_here":
                raise ValueError(
                    "GEMINI_API_KEY not set. "
                    "Please set it in .env file or pass as argument."
                )
            
            self.provider = GeminiProvider(api_key, model)
            
        elif self.provider_name == "grok":
            api_key = api_key or os.getenv("GROK_API_KEY")
            model = model or os.getenv("GROK_MODEL", "grok-beta")
            
            if not api_key or api_key == "your_grok_api_key_here":
                raise ValueError(
                    "GROK_API_KEY not set. "
                    "Please set it in .env file or pass as argument."
                )
            
            self.provider = GrokProvider(api_key, model)
            
        else:
            raise ValueError(f"Unknown provider: {self.provider_name}")
        
        # Get default settings from env
        self.temperature = float(os.getenv("TEMPERATURE", "0.1"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
    
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from LLM.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (overrides default)
            max_tokens: Maximum tokens (overrides default)
            
        Returns:
            Generated text response
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        return self.provider.generate(prompt, temperature=temp, max_tokens=tokens)
    
    def create_prompt(
        self,
        question: str,
        context: str,
        sources: list
    ) -> str:
        """
        Create a prompt for factual Q&A with citations.
        
        Args:
            question: User's question
            context: Retrieved context from documents
            sources: List of source metadata
            
        Returns:
            Formatted prompt
        """
        timestamp = datetime.now().strftime("%B %d, %Y")
        
        prompt = f"""You are a factual mutual fund information assistant. Your role is to provide accurate, fact-based answers ONLY using the information provided in the context below.

IMPORTANT RULES:
1. Answer ONLY based on the provided context
2. If the context doesn't contain the answer, say "I don't have enough information to answer this question."
3. ALWAYS cite sources using [Source N] format
4. Do NOT provide investment advice or recommendations
5. Be concise and factual
6. Include relevant numbers, percentages, and specific details from the context

DISCLAIMER: This is for informational purposes only and does not constitute investment advice.

CONTEXT:
{context}

QUESTION: {question}

Please provide a factual answer with source citations. Format your response as:

Answer: [Your factual answer with [Source N] citations]

Sources:
[List the sources you referenced]

Last updated: {timestamp}
"""
        return prompt


def get_llm() -> LLM:
    """
    Get LLM instance with default configuration from environment.
    
    Returns:
        Configured LLM instance
    """
    return LLM()


if __name__ == "__main__":
    # Test the LLM wrapper
    try:
        llm = get_llm()
        print(f"LLM Provider: {llm.provider_name}")
        print("LLM initialized successfully!")
    except Exception as e:
        print(f"Error: {e}")
