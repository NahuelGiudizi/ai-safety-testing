"""
LLM Provider abstraction layer.

Supports multiple backends: Ollama (local), OpenAI, Anthropic, etc.
"""

from .base import (
    GenerationConfig,
    GenerationResult,
    LLMProvider,
    ProviderError,
)
from .ollama_provider import OllamaProvider

# Conditional imports for optional providers
_has_openai: bool = False
OpenAIProvider: type | None = None

try:
    from .openai_provider import OpenAIProvider as _OpenAIProvider

    OpenAIProvider = _OpenAIProvider  # type: ignore[misc]
    _has_openai = True
except ImportError:
    pass

__all__ = [
    "LLMProvider",
    "GenerationResult",
    "GenerationConfig",
    "ProviderError",
    "OllamaProvider",
    "OpenAIProvider",
]
