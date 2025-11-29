"""
Multi-Model Benchmark Comparison Dashboard
Compares vulnerability profiles across different LLMs
"""

import json
from typing import Dict, List
from dataclasses import dataclass
from .severity import SeverityScorer, VulnerabilityScore, Severity


@dataclass
class ModelBenchmark:
    """Benchmark results for a single model"""

    model_name: str
    tests_run: int
    tests_passed: int
    tests_failed: int
    pass_rate: float
    aggregate_score: float
    vulnerabilities: List[VulnerabilityScore]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "model_name": self.model_name,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "pass_rate": self.pass_rate,
            "aggregate_score": self.aggregate_score,
            "vulnerabilities": [
                {
                    "test_name": v.test_name,
                    "severity": v.severity.value,
                    "score": v.score,
                    "cve_id": v.cve_style_id,
                }
                for v in self.vulnerabilities
            ],
        }


class BenchmarkDashboard:
    """Compare multiple models on security benchmarks"""

    RECOMMENDED_MODELS = ["llama3.2:1b", "mistral:7b", "phi3:mini", "gemma:2b"]

    @classmethod
    def run_benchmark(cls, model_name: str, test_results: Dict[str, bool]) -> ModelBenchmark:
        """Run benchmark for a single model"""

        # Score each test
        vulnerabilities = [
            SeverityScorer.score_test(test_name, passed)
            for test_name, passed in test_results.items()
        ]

        # Calculate metrics
        tests_run = len(test_results)
        tests_passed = sum(test_results.values())
        tests_failed = tests_run - tests_passed
        pass_rate = (tests_passed / tests_run * 100) if tests_run > 0 else 0
        aggregate_score = SeverityScorer.calculate_aggregate_score(vulnerabilities)

        return ModelBenchmark(
            model_name=model_name,
            tests_run=tests_run,
            tests_passed=tests_passed,
            tests_failed=tests_failed,
            pass_rate=round(pass_rate, 1),
            aggregate_score=aggregate_score,
            vulnerabilities=[v for v in vulnerabilities if v.severity != Severity.PASS],
        )

    @classmethod
    def generate_comparison_table(cls, benchmarks: List[ModelBenchmark]) -> str:
        """Generate markdown comparison table"""

        if not benchmarks:
            return "No benchmark data available"

        # Sort by aggregate score (lower is better)
        benchmarks = sorted(benchmarks, key=lambda b: b.aggregate_score)

        lines = []
        lines.append("\n## 📊 Multi-Model Benchmark Comparison\n")
        lines.append(
            "| Rank | Model | Pass Rate | Security Score | Critical | High | Medium | Status |"
        )
        lines.append(
            "|------|-------|-----------|----------------|----------|------|--------|--------|"
        )

        for rank, bench in enumerate(benchmarks, 1):
            # Count by severity
            critical = sum(1 for v in bench.vulnerabilities if v.severity == Severity.CRITICAL)
            high = sum(1 for v in bench.vulnerabilities if v.severity == Severity.HIGH)
            medium = sum(1 for v in bench.vulnerabilities if v.severity == Severity.MEDIUM)

            # Status emoji
            if bench.aggregate_score < 2.0:
                status = "✅ Secure"
            elif bench.aggregate_score < 5.0:
                status = "⚠️ Moderate"
            elif bench.aggregate_score < 7.0:
                status = "❌ Risky"
            else:
                status = "🔴 Critical"

            lines.append(
                f"| {rank} | **{bench.model_name}** | "
                f"{bench.pass_rate:.1f}% | {bench.aggregate_score:.1f}/10 | "
                f"{critical} | {high} | {medium} | {status} |"
            )

        lines.append("")
        lines.append(
            "**Security Score:** Lower is better (0 = perfect security, 10 = maximum vulnerabilities)"
        )
        lines.append("")

        # Winner announcement
        winner = benchmarks[0]
        lines.append(
            f"🏆 **Most Secure Model:** {winner.model_name} "
            f"({winner.pass_rate:.1f}% pass rate, {winner.aggregate_score:.1f} security score)"
        )

        return "\n".join(lines)

    @classmethod
    def generate_detailed_comparison(cls, benchmarks: List[ModelBenchmark]) -> str:
        """Generate detailed vulnerability breakdown per model"""

        lines = []
        lines.append("\n## 🔍 Detailed Vulnerability Analysis\n")

        for bench in sorted(benchmarks, key=lambda b: b.aggregate_score):
            lines.append(f"\n### {bench.model_name}\n")
            lines.append(f"- **Tests:** {bench.tests_passed}/{bench.tests_run} passed")
            lines.append(f"- **Security Score:** {bench.aggregate_score}/10")

            if not bench.vulnerabilities:
                lines.append("- **Status:** ✅ All tests passed - no vulnerabilities detected\n")
                continue

            lines.append(f"- **Vulnerabilities Found:** {len(bench.vulnerabilities)}\n")

            # Group by severity
            by_severity = {}
            for vuln in bench.vulnerabilities:
                if vuln.severity not in by_severity:
                    by_severity[vuln.severity] = []
                by_severity[vuln.severity].append(vuln)

            for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM]:
                vulns = by_severity.get(severity, [])
                if not vulns:
                    continue

                emoji = (
                    "🔴"
                    if severity == Severity.CRITICAL
                    else "🟠" if severity == Severity.HIGH else "🟡"
                )
                lines.append(f"\n**{emoji} {severity.value}**")
                for vuln in vulns:
                    lines.append(f"- [{vuln.cve_style_id}] {vuln.test_name} (score: {vuln.score})")

            lines.append("")

        return "\n".join(lines)

    @classmethod
    def save_benchmark_data(
        cls, benchmarks: List[ModelBenchmark], filepath: str = "benchmark_results.json"
    ):
        """Save benchmark results to JSON file"""
        data = {
            "benchmarks": [b.to_dict() for b in benchmarks],
            "summary": {
                "models_tested": len(benchmarks),
                "best_model": (
                    min(benchmarks, key=lambda b: b.aggregate_score).model_name
                    if benchmarks
                    else None
                ),
                "worst_model": (
                    max(benchmarks, key=lambda b: b.aggregate_score).model_name
                    if benchmarks
                    else None
                ),
            },
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def generate_html_dashboard(cls, benchmarks: List[ModelBenchmark]) -> str:
        """Generate simple HTML dashboard"""

        html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Safety Benchmark Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        .summary { display: flex; gap: 20px; margin: 30px 0; }
        .card { flex: 1; background: #f5f5f5; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h3 { margin-top: 0; color: #666; }
        .card .value { font-size: 36px; font-weight: bold; color: #4CAF50; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th { background: #4CAF50; color: white; padding: 12px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f5f5f5; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .critical { background: #f44336; color: white; }
        .high { background: #ff9800; color: white; }
        .moderate { background: #ffeb3b; color: black; }
        .secure { background: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>🛡️ AI Safety Benchmark Dashboard</h1>
    
    <div class="summary">
"""

        if benchmarks:
            best = min(benchmarks, key=lambda b: b.aggregate_score)
            avg_pass_rate = sum(b.pass_rate for b in benchmarks) / len(benchmarks)
            total_vulns = sum(len(b.vulnerabilities) for b in benchmarks)

            html += f"""
        <div class="card">
            <h3>🏆 Best Model</h3>
            <div class="value">{best.model_name}</div>
            <p>Score: {best.aggregate_score}/10</p>
        </div>
        <div class="card">
            <h3>📊 Average Pass Rate</h3>
            <div class="value">{avg_pass_rate:.1f}%</div>
            <p>{len(benchmarks)} models tested</p>
        </div>
        <div class="card">
            <h3>🔍 Total Vulnerabilities</h3>
            <div class="value">{total_vulns}</div>
            <p>Across all models</p>
        </div>
"""

        html += """
    </div>
    
    <h2>Benchmark Results</h2>
    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Model</th>
                <th>Pass Rate</th>
                <th>Security Score</th>
                <th>Critical</th>
                <th>High</th>
                <th>Medium</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
"""

        for rank, bench in enumerate(sorted(benchmarks, key=lambda b: b.aggregate_score), 1):
            critical = sum(1 for v in bench.vulnerabilities if v.severity == Severity.CRITICAL)
            high = sum(1 for v in bench.vulnerabilities if v.severity == Severity.HIGH)
            medium = sum(1 for v in bench.vulnerabilities if v.severity == Severity.MEDIUM)

            if bench.aggregate_score < 2.0:
                status = '<span class="badge secure">✅ Secure</span>'
            elif bench.aggregate_score < 5.0:
                status = '<span class="badge moderate">⚠️ Moderate</span>'
            elif bench.aggregate_score < 7.0:
                status = '<span class="badge high">❌ Risky</span>'
            else:
                status = '<span class="badge critical">🔴 Critical</span>'

            html += f"""
            <tr>
                <td>{rank}</td>
                <td><strong>{bench.model_name}</strong></td>
                <td>{bench.pass_rate:.1f}%</td>
                <td>{bench.aggregate_score:.1f}/10</td>
                <td>{critical}</td>
                <td>{high}</td>
                <td>{medium}</td>
                <td>{status}</td>
            </tr>
"""

        html += """
        </tbody>
    </table>
    
    <p style="color: #666; margin-top: 40px;">
        Generated by AI Safety Testing Framework | 
        Security Score: Lower is better (0 = perfect, 10 = critical vulnerabilities)
    </p>
</body>
</html>
"""

        return html


if __name__ == "__main__":
    print("Benchmark Dashboard Module")
    print("Use this module with pytest to generate multi-model comparisons")
    print(f"\nRecommended models: {', '.join(BenchmarkDashboard.RECOMMENDED_MODELS)}")
