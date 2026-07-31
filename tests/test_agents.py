"""Tests for AGENTS.md — validate that all required sections exist."""

import os

AGENTS_PATH = os.path.join(os.path.dirname(__file__), "..", "AGENTS.md")


def test_agents_md_exists():
    """AGENTS.md must exist at the repository root."""
    assert os.path.isfile(AGENTS_PATH), "AGENTS.md not found at repository root"


def test_agents_md_has_sandbox_testing_section():
    """Must contain a Sandbox Testing section with error handling guidance."""
    content = open(AGENTS_PATH).read()
    assert "Sandbox Testing" in content, "Missing 'Sandbox Testing' section"
    assert "try" in content.lower() or "except" in content.lower(), (
        "Sandbox Testing section should mention try/except"
    )
    assert "commit" in content.lower(), (
        "Sandbox Testing section should mention not committing known failures"
    )


def test_agents_md_has_general_python_best_practices_section():
    """Must contain a General Python Best Practices section."""
    content = open(AGENTS_PATH).read()
    assert "General Python Best Practices" in content, (
        "Missing 'General Python Best Practices' section"
    )
    assert "type hint" in content.lower(), "Should mention type hints"
    assert "pep 8" in content.lower(), "Should mention PEP 8"
    assert "config" in content.lower(), "Should mention avoiding hardcoded values via config"
    assert "factory" in content.lower(), "Should mention application factory pattern"
    assert "context manager" in content.lower() or "with" in content.lower(), (
        "Should mention context managers"
    )
    assert "database" in content.lower() or "db" in content.lower(), (
        "Should mention proper database initialization"
    )


def test_agents_md_has_making_changes_section():
    """Must contain a Making Changes to Existing Code section."""
    content = open(AGENTS_PATH).read()
    assert "Making Changes" in content, "Missing 'Making Changes' section"
    assert "read" in content.lower(), "Should mention reading existing files"
    assert "consistent" in content.lower() or "consistency" in content.lower(), (
        "Should mention consistency"
    )
    assert "remove" in content.lower(), (
        "Should mention not removing existing functionality"
    )
    assert "focused" in content.lower() or "minimal" in content.lower(), (
        "Should mention keeping changes focused and minimal"
    )


def test_agents_md_has_sandbox_specific_section():
    """Must contain a Sandbox-Specific Behavior section."""
    content = open(AGENTS_PATH).read()
    assert "Sandbox-Specific" in content or "Sandbox specific" in content, (
        "Missing 'Sandbox-Specific Behavior' section"
    )
    assert "verify" in content.lower() or "run" in content.lower(), (
        "Should mention verifying code runs"
    )
    assert "depend" in content.lower(), "Should mention installing dependencies"
