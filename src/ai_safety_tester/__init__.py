"""
AI Safety Testing Framework
Test LLM security vulnerabilities with severity scoring
"""

from .tester import SimpleAITester
from .severity import SeverityScorer, Severity, VulnerabilityScore, get_severity_badge
from .benchmark import BenchmarkDashboard, ModelBenchmark

__version__ = "1.0.0"
__all__ = [
    "SimpleAITester",
    "SeverityScorer",
    "Severity",
    "VulnerabilityScore",
    "get_severity_badge",
    "BenchmarkDashboard",
    "ModelBenchmark",
]
