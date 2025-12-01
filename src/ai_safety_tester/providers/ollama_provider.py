"""
Ollama Provider for AI Safety Testing

Local LLM execution using Ollama
"""

import time
from typing import Optional

import ollama

from .base import GenerationConfig, GenerationResult, LLMProvider, ProviderError


class OllamaProvider(LLMProvider):
    """
    Ollama provider for local LLM execution

    Supported models:
    - llama3.2:1b - Fast, 1.3GB
    - mistral:7b - More capable, 4.1GB
    - phi3:mini - Microsoft's 3.8B model
    - gemma:2b - Google's efficient model
    """

    def __init__(self, model: str = "llama3.2:1b", config: Optional[GenerationConfig] = None):
        self.model = model
        self.config = config or GenerationConfig()

    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> GenerationResult:
        """Generate text using Ollama"""
        cfg = config or self.config

        start_time = time.time()

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": cfg.temperature,
                    "num_predict": cfg.max_tokens,
                },
            )

            elapsed = time.time() - start_time

            return GenerationResult(
                text=response["message"]["content"], response_time=elapsed, model=self.model
            )
        except Exception as e:
            raise ProviderError(f"Ollama generation failed: {e}")

    def is_available(self) -> bool:
        """Check if Ollama and model are available"""
        try:
            ollama.list()
            return True
        except Exception:
            return False

    def get_model_name(self) -> str:
        """Get the model name"""
        return self.model
