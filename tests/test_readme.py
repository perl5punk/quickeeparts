"""Smoke tests for quickeeparts README.md — verifies acceptance criteria."""
import pathlib


def _readme():
    """Return the README.md content."""
    readme = pathlib.Path(__file__).parent.parent / "README.md"
    return readme.read_text()


def test_readme_exists():
    """README.md must exist at repo root."""
    assert pathlib.Path(__file__).parent.parent.joinpath("README.md").exists()


def test_readme_substantial_content():
    """README must have more than 50 non-blank lines."""
    lines = [l for l in _readme().splitlines() if l.strip()]
    assert len(lines) > 50


def test_readme_has_description_section():
    """README contains a Description section explaining quickeeparts."""
    content = _readme().lower()
    assert "description" in content
    assert "surplus" in content
    assert any(w in content for w in ["ebay", "marketplace"])


def test_readme_has_features_section():
    """README contains a Features section with core capabilities."""
    content = _readme().lower()
    assert "features" in content
    assert "photo" in content or "image" in content
    assert "identify" in content
    assert "demand" in content or "value" in content
    assert "approval" in content
    assert "ebay" in content


def test_readme_has_install_section():
    """README contains an Install/Setup section."""
    content = _readme().lower()
    assert any(w in content for w in ["install", "setup", "prerequisite"])
    assert "python" in content
    assert "venv" in content or "virtual environment" in content
    assert "pip" in content and "requirements" in content
    assert ".env" in content


def test_readme_has_usage_section():
    """README contains a Usage section with concrete examples."""
    content = _readme().lower()
    assert "usage" in content
    assert "upload" in content or "photo" in content
    assert "approve" in content


def test_readme_has_project_structure():
    """README contains a Project Structure section."""
    content = _readme().lower()
    assert "project structure" in content


def test_readme_has_contributing():
    """README contains a Contributing section."""
    content = _readme().lower()
    assert "contributing" in content
    assert "fork" in content
    assert "branch" in content
    assert "pull request" in content or "pull-request" in content


def test_readme_has_code_blocks():
    """README uses fenced code blocks for commands."""
    assert "```bash" in _readme()


def test_readme_uses_proper_markdown():
    """README uses headers and tables."""
    content = _readme()
    assert "# " in content  # H1
    assert "## " in content  # H2
    assert "|---" in content or "| --" in content or "|--" in content
