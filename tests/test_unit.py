"""
Fast unit tests that don't require Ollama
These tests run in CI on every commit
"""

import pytest
from ai_safety_tester.severity import Severity, SeverityScorer, VulnerabilityScore


def test_severity_enum_values():
    """Test severity enum has expected values"""
    assert Severity.CRITICAL.value == "CRITICAL"
    assert Severity.HIGH.value == "HIGH"
    assert Severity.MEDIUM.value == "MEDIUM"
    assert Severity.LOW.value == "LOW"
    assert Severity.PASS.value == "PASS"


def test_vulnerability_score_creation():
    """Test creating VulnerabilityScore dataclass"""
    score = VulnerabilityScore(
        test_name="test_injection",
        severity=Severity.CRITICAL,
        score=9.5,
        description="Prompt injection vulnerability",
        impact="Complete bypass of safety measures",
        remediation="Implement input validation",
    )

    assert score.test_name == "test_injection"
    assert score.severity == Severity.CRITICAL
    assert score.score == 9.5
    assert score.cve_style_id.startswith("AIV-2025-")


def test_vulnerability_score_auto_id():
    """Test CVE-style ID is auto-generated"""
    score1 = VulnerabilityScore(
        test_name="test_1",
        severity=Severity.HIGH,
        score=8.0,
        description="Test",
        impact="Test",
        remediation="Test",
    )

    score2 = VulnerabilityScore(
        test_name="test_2",
        severity=Severity.HIGH,
        score=8.0,
        description="Test",
        impact="Test",
        remediation="Test",
    )

    # Different test names should generate different IDs
    assert score1.cve_style_id != score2.cve_style_id
    assert score1.cve_style_id.startswith("AIV-2025-")
    assert score2.cve_style_id.startswith("AIV-2025-")


def test_severity_scorer_has_vulnerability_matrix():
    """Test SeverityScorer has the vulnerability scoring matrix"""
    assert hasattr(SeverityScorer, "VULNERABILITY_SCORES")
    assert isinstance(SeverityScorer.VULNERABILITY_SCORES, dict)
    assert len(SeverityScorer.VULNERABILITY_SCORES) > 0


def test_vulnerability_scores_structure():
    """Test vulnerability scores have expected structure"""
    for test_name, info in SeverityScorer.VULNERABILITY_SCORES.items():
        assert isinstance(test_name, str)
        assert "score" in info
        assert "severity" in info
        assert "description" in info
        assert "impact" in info
        assert "remediation" in info

        assert isinstance(info["score"], (int, float))
        assert isinstance(info["severity"], Severity)
        assert isinstance(info["description"], str)
        assert isinstance(info["impact"], str)
        assert isinstance(info["remediation"], str)

        # Validate score ranges
        assert 0.0 <= info["score"] <= 10.0


def test_severity_ranges():
    """Test severity scoring ranges are correct"""
    # Test CRITICAL vulnerability
    critical_score = SeverityScorer.score_test("test_prompt_injection_basic", passed=False)
    assert critical_score.severity == Severity.CRITICAL
    assert critical_score.score >= 9.0

    # Test PASS
    pass_score = SeverityScorer.score_test("test_refusal_harmful_content", passed=True)
    assert pass_score.severity == Severity.PASS
    assert pass_score.score == 0.0


def test_severity_grouping():
    """Test grouping vulnerabilities by severity"""
    vulnerabilities = [
        SeverityScorer.score_test("test_prompt_injection_basic", False),  # CRITICAL
        SeverityScorer.score_test("test_gender_bias_hiring", False),  # MEDIUM
        SeverityScorer.score_test("test_refusal_harmful_content", True),  # PASS
    ]

    # Group by severity manually
    by_severity = {}
    for vuln in vulnerabilities:
        if vuln.severity not in by_severity:
            by_severity[vuln.severity] = []
        by_severity[vuln.severity].append(vuln)

    assert Severity.CRITICAL in by_severity
    assert Severity.MEDIUM in by_severity
    assert Severity.PASS in by_severity


def test_get_vulnerability_info():
    """Test retrieving vulnerability info for specific tests"""
    info = SeverityScorer.score_test("test_prompt_injection_basic", passed=False)

    assert info is not None
    assert info.severity == Severity.CRITICAL
    assert info.score >= 9.0
    assert len(info.description) > 0
    assert len(info.impact) > 0
    assert len(info.remediation) > 0


def test_unknown_test_handling():
    """Test handling of unknown test names"""
    info = SeverityScorer.score_test("test_nonexistent_test", passed=False)

    assert info is not None
    assert info.severity == Severity.MEDIUM  # Should default to MEDIUM
    assert info.test_name == "test_nonexistent_test"
    assert info.score == 5.0
