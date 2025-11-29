"""
Quick demo of severity scoring system
Run this to see example output without running full tests
"""

from ai_safety_tester import SeverityScorer, Severity

# Simulate test results (False = failed/vulnerable)
test_results = {
    "test_prompt_injection_basic": False,
    "test_prompt_injection_jailbreak_dan": False,
    "test_violent_content_refusal": True,
    "test_illegal_activity_refusal": True,
    "test_gender_bias_hiring": True,
    "test_math_reasoning": True,
}

# Score each test
vulnerabilities = [
    SeverityScorer.score_test(test_name, passed)
    for test_name, passed in test_results.items()
]

# Generate report
report = SeverityScorer.generate_report(vulnerabilities)

print(report)

print("\n" + "="*80)
print("INDIVIDUAL VULNERABILITY DETAILS")
print("="*80)

for vuln in vulnerabilities:
    if vuln.severity != Severity.PASS:
        print(f"\n🚨 {vuln.cve_style_id}: {vuln.test_name}")
        print(f"   Score: {vuln.score}/10 | Severity: {vuln.severity.value}")
        print(f"   {vuln.description}")
