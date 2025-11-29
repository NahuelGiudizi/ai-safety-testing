"""
Comprehensive Test Runner with Severity Scoring & Benchmarking
Run this to generate full security reports with remediation advice
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict
import pytest
from ai_safety_tester import SimpleAITester, SeverityScorer, Severity, get_severity_badge, BenchmarkDashboard, ModelBenchmark


def collect_test_results(model: str) -> Dict[str, bool]:
    """Run pytest and collect results for a model"""
    
    # Run pytest programmatically
    print(f"\n{'='*80}")
    print(f"Testing model: {model}")
    print('='*80)
    
    # Create temporary pytest plugin to collect results
    class ResultCollector:
        def __init__(self):
            self.results = {}
        
        def pytest_runtest_logreport(self, report):
            if report.when == "call":
                # Extract test name without path
                test_name = report.nodeid.split("::")[-1]
                # Remove parametrize suffix if present
                test_name = test_name.split("[")[0]
                self.results[test_name] = report.outcome == "passed"
    
    collector = ResultCollector()
    
    # Run pytest with custom args
    args = [
        "tests/test_simple_ai.py",
        "-v",
        "--tb=no",
        "-q",
        f"--model={model}"  # Pass model as custom arg
    ]
    
    pytest.main(args, plugins=[collector])
    
    return collector.results


def generate_security_report(model: str, output_file: str = None):
    """Generate comprehensive security report for a single model"""
    
    print(f"\n🔍 Running security analysis on {model}...")
    
    # Collect test results
    test_results = collect_test_results(model)
    
    if not test_results:
        print("⚠️ No test results collected. Make sure test_simple_ai.py exists.")
        return
    
    # Score vulnerabilities
    vulnerabilities = [
        SeverityScorer.score_test(test_name, passed)
        for test_name, passed in test_results.items()
    ]
    
    # Generate report
    report = SeverityScorer.generate_report(vulnerabilities)
    
    # Print to console
    print(report)
    
    # Save to file if specified
    if output_file:
        Path(output_file).write_text(report, encoding='utf-8')
        print(f"\n✅ Report saved to: {output_file}")


def run_multi_model_benchmark(models: List[str], output_dir: str = "."):
    """Run benchmark across multiple models and generate comparison dashboard"""
    
    print(f"\n🚀 Running multi-model benchmark...")
    print(f"Models: {', '.join(models)}\n")
    
    benchmarks = []
    
    for model in models:
        print(f"\n{'='*80}")
        print(f"Benchmarking: {model}")
        print('='*80)
        
        # Check if model is available
        try:
            tester = SimpleAITester(model=model)
            # Quick connectivity test
            response = tester.chat("Hello")
            print(f"✅ Model {model} is available")
        except Exception as e:
            print(f"⚠️ Model {model} not available: {e}")
            print(f"   Run: ollama pull {model}")
            continue
        
        # Collect test results
        test_results = collect_test_results(model)
        
        if not test_results:
            print(f"⚠️ No results for {model}")
            continue
        
        # Generate benchmark
        benchmark = BenchmarkDashboard.run_benchmark(model, test_results)
        benchmarks.append(benchmark)
        
        print(f"✅ {model}: {benchmark.pass_rate:.1f}% pass rate, "
              f"{benchmark.aggregate_score:.1f} security score")
    
    if not benchmarks:
        print("\n❌ No benchmarks completed. Make sure models are installed.")
        return
    
    # Generate comparison outputs
    print("\n" + "="*80)
    print("GENERATING BENCHMARK REPORTS")
    print("="*80)
    
    # 1. Markdown comparison
    markdown = BenchmarkDashboard.generate_comparison_table(benchmarks)
    markdown += BenchmarkDashboard.generate_detailed_comparison(benchmarks)
    
    md_file = Path(output_dir) / "BENCHMARK_COMPARISON.md"
    md_file.write_text(markdown, encoding='utf-8')
    print(f"✅ Markdown report: {md_file}")
    
    # 2. JSON data
    json_file = Path(output_dir) / "benchmark_results.json"
    BenchmarkDashboard.save_benchmark_data(benchmarks, str(json_file))
    print(f"✅ JSON data: {json_file}")
    
    # 3. HTML dashboard
    html = BenchmarkDashboard.generate_html_dashboard(benchmarks)
    html_file = Path(output_dir) / "benchmark_dashboard.html"
    html_file.write_text(html, encoding='utf-8')
    print(f"✅ HTML dashboard: {html_file}")
    
    # Print summary
    print("\n" + markdown)
    
    print("\n" + "="*80)
    print("🎉 BENCHMARK COMPLETE")
    print("="*80)
    print(f"View HTML dashboard: file://{html_file.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description="AI Safety Testing with Severity Scoring & Benchmarking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single model security report
  python run_comprehensive_tests.py --model llama3.2:1b --report security_report.txt
  
  # Multi-model benchmark
  python run_comprehensive_tests.py --benchmark --models llama3.2:1b mistral:7b phi3:mini
  
  # Quick benchmark with default models
  python run_comprehensive_tests.py --benchmark-quick
        """
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="llama3.2:1b",
        help="Model to test (default: llama3.2:1b)"
    )
    
    parser.add_argument(
        "--report",
        type=str,
        help="Save security report to file"
    )
    
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run multi-model benchmark comparison"
    )
    
    parser.add_argument(
        "--benchmark-quick",
        action="store_true",
        help="Quick benchmark with recommended models"
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        help="Models to benchmark (space-separated)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory for reports (default: current directory)"
    )
    
    args = parser.parse_args()
    
    if args.benchmark or args.benchmark_quick:
        # Multi-model benchmark
        if args.benchmark_quick:
            models = ["llama3.2:1b", "mistral:7b", "phi3:mini", "gemma:2b"]
        elif args.models:
            models = args.models
        else:
            print("❌ --benchmark requires --models or use --benchmark-quick")
            return 1
        
        run_multi_model_benchmark(models, args.output_dir)
    
    else:
        # Single model report
        generate_security_report(args.model, args.report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
