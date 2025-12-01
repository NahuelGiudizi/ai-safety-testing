# AI Safety Testing

[![PyPI version](https://img.shields.io/pypi/v/ai-safety-tester.svg)](https://pypi.org/project/ai-safety-tester/)
[![Python versions](https://img.shields.io/pypi/pyversions/ai-safety-tester.svg)](https://pypi.org/project/ai-safety-tester/)
[![Tests](https://github.com/NahuelGiudizi/ai-safety-testing/workflows/Tests/badge.svg)](https://github.com/NahuelGiudizi/ai-safety-testing/actions)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/NahuelGiudizi/ai-safety-testing/blob/master/LICENSE)

> **LLM Security Testing Framework** with CVE-style severity scoring and multi-model benchmarking

## ⚡ Quick Start (30 seconds)

```bash
pip install ai-safety-tester
```

```python
from ai_safety_tester import SimpleAITester

tester = SimpleAITester(model="llama3.2:1b")
results = tester.run_all_tests()
```

**Output:**
```
==================================================
AI Safety Testing Results
==================================================
basic_response       ✅ PASS
refusal              ✅ PASS
math                 ✅ PASS
==================================================
Total: 3/3 tests passed
==================================================
```

## 🎯 Features

- ✅ **Real benchmarks** (MMLU, TruthfulQA, HellaSwag - 24K+ questions)
- ✅ **CVE-style severity scoring** (CRITICAL/HIGH/MEDIUM/LOW)
- ✅ **Multi-provider** (Ollama local, OpenAI cloud)
- ✅ **Multi-model comparison** with HTML dashboards
- ✅ **Semantic similarity** detection (optional)

## 📊 Compare Models

```python
from ai_safety_tester import SimpleAITester
from ai_safety_tester.benchmark import BenchmarkDashboard

# Test multiple models
results_llama = SimpleAITester(model="llama3.2:1b").run_all_tests()
results_mistral = SimpleAITester(model="mistral:7b").run_all_tests()

# Generate comparison
bench_llama = BenchmarkDashboard.run_benchmark("llama3.2:1b", results_llama)
bench_mistral = BenchmarkDashboard.run_benchmark("mistral:7b", results_mistral)

print(BenchmarkDashboard.generate_comparison_table([bench_llama, bench_mistral]))
```

**Output:**
```
| Rank | Model         | Pass Rate | Security Score | Status     |
|------|---------------|-----------|----------------|------------|
| 1    | mistral:7b    | 95.8%     | 1.2/10         | ✅ Secure  |
| 2    | llama3.2:1b   | 83.3%     | 4.8/10         | ⚠️ Moderate |
```

## 🔬 Run Academic Benchmarks

```python
from ai_safety_tester import SimpleAITester
from ai_safety_tester.benchmark import BenchmarkRunner

tester = SimpleAITester(model="llama3.2:1b")

# Quick sample (100 questions, ~5 min)
runner = BenchmarkRunner(tester, use_full_datasets=True, sample_size=100)
results = runner.run_all()

print(f"MMLU: {results['mmlu']['accuracy']:.1%}")
print(f"TruthfulQA: {results['truthfulqa']['truthfulness_score']:.1%}")
print(f"HellaSwag: {results['hellaswag']['accuracy']:.1%}")
```

## 🔐 OpenAI Support

```bash
pip install ai-safety-tester[openai]
```

```python
from ai_safety_tester.providers import OpenAIProvider

provider = OpenAIProvider(model="gpt-3.5-turbo")  # Uses OPENAI_API_KEY env var
result = provider.generate("Test prompt")
```

## 📖 Documentation

- [Full Guide](docs/FULL_GUIDE.md) - Complete documentation
- [Examples](docs/EXAMPLES.md) - Usage examples
- [Dev.to Article](https://dev.to/nahuelgiudizi/i-found-4-critical-vulnerabilities-testing-llama-32-and-you-can-too-3mff) - Full analysis

## 🔗 Requirements

- Python 3.11+
- [Ollama](https://ollama.com/download) (for local models)
- Models: `ollama pull llama3.2:1b`

## 📝 License

MIT

---

**Author:** Nahuel | **Date:** November 2025
