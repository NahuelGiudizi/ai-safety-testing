"""
Base classes for LLM providers.

Defines the abstract interface and common types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationResult:
    """Result from LLM generation."""

    text: str
    response_time: float
    tokens_used: Optional[int] = None
    model: Optional[str] = None


@dataclass
class GenerationConfig:
    """Configuration for text generation."""

    temperature: float = 0.7
    max_tokens: int = 500
    timeout_seconds: int = 30
    retry_attempts: int = 3


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> GenerationResult:
        """Generate text from prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name."""
        pass


class ProviderError(Exception):
    """Base exception for provider errors."""

    pass
