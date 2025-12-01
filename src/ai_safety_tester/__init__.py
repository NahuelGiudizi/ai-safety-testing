"""
AI Safety Testing Framework
Test LLM security vulnerabilities with severity scoring
"""

from .tester import SimpleAITester
from .severity import SeverityScorer, Severity, VulnerabilityScore, get_severity_badge
from .benchmark import BenchmarkDashboard, ModelBenchmark
from .providers import LLMProvider, GenerationConfig, GenerationResult, ProviderError
from .providers.ollama_provider import OllamaProvider

# Conditional imports for optional providers
_has_openai: bool = False
OpenAIProvider: type | None = None

try:
    from .providers.openai_provider import OpenAIProvider as _OpenAIProvider

    OpenAIProvider = _OpenAIProvider  # type: ignore[misc]
    _has_openai = True
except ImportError:
    pass

__version__ = "1.3.0"
__all__ = [
    "SimpleAITester",
    "SeverityScorer",
    "Severity",
    "VulnerabilityScore",
    "get_severity_badge",
    "BenchmarkDashboard",
    "ModelBenchmark",
    # Provider system
    "LLMProvider",
    "GenerationConfig",
    "GenerationResult",
    "ProviderError",
    "OllamaProvider",
    "OpenAIProvider",
]
