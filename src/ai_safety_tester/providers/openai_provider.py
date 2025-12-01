"""
OpenAI Provider for AI Safety Testing

Supports GPT-3.5, GPT-4, and other OpenAI models
"""

import os
import time
from typing import Optional

from . import LLMProvider, GenerationResult, GenerationConfig, ProviderError

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class OpenAIProvider(LLMProvider):
    """
    OpenAI provider for cloud-based LLM execution
    
    Supported models:
    - gpt-3.5-turbo - Fast and cost-effective
    - gpt-4 - Most capable
    - gpt-4-turbo - Fast and capable
    - gpt-4o - Latest optimized model
    
    Example:
        >>> provider = OpenAIProvider(model="gpt-3.5-turbo", api_key="sk-...")
        >>> result = provider.generate("Hello, world!")
        >>> print(result.text)
    """
    
    def __init__(
        self, 
        model: str = "gpt-3.5-turbo", 
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ):
        if not HAS_OPENAI:
            raise ImportError(
                "OpenAI library not installed. Install with: pip install ai-safety-tester[openai]"
            )
        
        self.model = model
        self.config = config or GenerationConfig()
        
        # Use provided API key or fall back to environment variable
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ProviderError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> GenerationResult:
        """Generate text using OpenAI API"""
        cfg = config or self.config
        
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=cfg.temperature,
                max_tokens=cfg.max_tokens,
                timeout=cfg.timeout_seconds,
            )
            
            elapsed = time.time() - start_time
            
            # Extract response text
            text = response.choices[0].message.content or ""
            tokens_used = response.usage.total_tokens if response.usage else None
            
            return GenerationResult(
                text=text,
                response_time=elapsed,
                tokens_used=tokens_used,
                model=self.model
            )
        except openai.AuthenticationError as e:
            raise ProviderError(f"OpenAI authentication failed: {e}")
        except openai.RateLimitError as e:
            raise ProviderError(f"OpenAI rate limit exceeded: {e}")
        except openai.APITimeoutError as e:
            raise ProviderError(f"OpenAI request timed out: {e}")
        except Exception as e:
            raise ProviderError(f"OpenAI generation failed: {e}")
    
    def is_available(self) -> bool:
        """Check if OpenAI API is available"""
        try:
            # Simple test call
            self.client.models.list()
            return True
        except Exception:
            return False
    
    def get_model_name(self) -> str:
        """Get the model name"""
        return self.model
