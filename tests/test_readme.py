"""Minimal smoke test for quickeeparts."""

import pathlib


def test_readme_exists():
    """Verify README.md has substantial content."""
    readme = pathlib.Path(__file__).parent.parent / "README.md"
    assert readme.exists(), "README.md should exist at repo root"
    content = readme.read_text()
    lines = [l for l in content.splitlines() if l.strip()]
    assert len(lines) > 50, f"README should have more than 50 lines, got {len(lines)}"


def test_readme_has_required_sections():
    """Verify README contains all required sections."""
    readme = pathlib.Path(__file__).parent.parent / "README.md"
    content = readme.read_text().lower()

    required_sections = [
        "description",
        "features",
        "install",
        "usage",
        "project structure",
        "contributing",
    ]
    for section in required_sections:
        assert section in content, f"README missing section: {section}"


def test_readme_has_code_blocks():
    """Verify README uses fenced code blocks."""
    readme = pathlib.Path(__file__).parent.parent / "README.md"
    content = readme.read_text()
    assert "```bash" in content, "README should contain bash code blocks"
