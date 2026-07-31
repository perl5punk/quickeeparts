"""Tests for quickeeparts README.md."""

import pathlib


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _readme():
    """Return the README.md content (stripped of blank lines)."""
    readme = pathlib.Path(__file__).parent.parent / "README.md"
    return readme.read_text()


def _readme_lines():
    return [l for l in _readme().splitlines() if l.strip()]


# ---------------------------------------------------------------------------
# Criterion 1: README exists with substantial content (>50 lines)
# ---------------------------------------------------------------------------

def test_readme_exists():
    """Verify README.md exists at repo root."""
    readme = pathlib.Path(__file__).parent.parent / "README.md"
    assert readme.exists(), "README.md should exist at repo root"


def test_readme_substantial_content():
    """README should have more than 50 non-blank lines."""
    lines = _readme_lines()
    assert len(lines) > 50, f"README should have more than 50 lines, got {len(lines)}"


# ---------------------------------------------------------------------------
# Criterion 8: Proper Markdown formatting
# ---------------------------------------------------------------------------

def test_readme_has_code_blocks():
    """Verify README uses fenced code blocks."""
    content = _readme()
    assert "```bash" in content, "README should contain bash code blocks"


def test_readme_has_h1_header():
    """README should have an H1 (project title)."""
    assert "# " in _readme(), "README should have an H1 header"


def test_readme_has_h2_headers():
    """README should use H2 headers for sections."""
    assert "## " in _readme(), "README should have H2 headers for sections"


def test_readme_has_lists():
    """README should use bullet lists."""
    content = _readme()
    # Bullet lists: lines starting with '- ' or '* '
    lines = [l for l in content.splitlines() if l.strip().startswith(("-", "*"))]
    assert len(lines) >= 5, f"README should have bullet lists (found {len(lines)})"


def test_readme_has_tables():
    """README should use a Markdown table (e.g. config table)."""
    assert "|---" in _readme() or "|---" in _readme() or "| --" in _readme() or "|--" in _readme(), (
        "README should contain at least one Markdown table"
    )


# ---------------------------------------------------------------------------
# Criterion 2: Description section
# ---------------------------------------------------------------------------

def test_readme_has_description_section():
    """README contains a Description section."""
    content = _readme().lower()
    assert "description" in content, "README missing 'Description' section"


def test_readme_description_mentions_surplus_parts():
    """Description explains quickeeparts identifies/valued/listed surplus parts."""
    content = _readme().lower()
    assert "surplus" in content, "Description should mention 'surplus' parts"


def test_readme_description_mentions_multi_platform():
    """Description mentions multiple selling platforms."""
    content = _readme().lower()
    assert any(w in content for w in ["ebay", "marketplace", "marketplaces"]), (
        "Description should mention eBay or marketplaces"
    )


def test_readme_overall_goal_mentioned():
    """README mentions the overall goal: utility for shops with surplus parts."""
    content = _readme().lower()
    # The spec says the goal is about providing utility for shops with surplus
    # parts to automate identification, valuation, and listing
    mentions_shop = "shop" in content
    mentions_identify = "identify" in content or "photograph" in content or "take a photo" in content
    mentions_value = "value" in content or "worth" in content or "valued" in content
    mentions_list = "list" in content or "listing" in content
    assert mentions_shop, "README should mention 'shop'"
    assert mentions_identify, "README should mention identifying parts"
    assert mentions_value, "README should mention valuing parts"
    assert mentions_list, "README should mention listing parts"


# ---------------------------------------------------------------------------
# Criterion 3: Feature overview
# ---------------------------------------------------------------------------

def test_readme_has_features_section():
    """README contains a Features section."""
    content = _readme().lower()
    assert "features" in content, "README missing 'Features' section"


def test_readme_feature_photo_identification():
    """Features mentions photo-based part identification."""
    content = _readme().lower()
    assert "photo" in content and ("identify" in content or "identify" in content), (
        "Features should mention photo-based identification"
    )


def test_readme_feature_demand_value():
    """Features mentions demand and value assessment."""
    content = _readme().lower()
    assert any(w in content for w in ["demand", "value"]), (
        "Features should mention demand and value"
    )


def test_readme_feature_approval_queue():
    """Features mentions approval queue workflow."""
    content = _readme().lower()
    assert "approval" in content, "Features should mention approval workflow"


def test_readme_feature_multi_platform_listing():
    """Features mentions multi-platform listing (eBay and others)."""
    content = _readme().lower()
    assert "ebay" in content, "Features should mention eBay"
    # Should also mention extensibility to other platforms
    assert any(w in content for w in ["extensible", "other", "mercari", "facebook"]), (
        "Features should mention other/extendable platforms"
    )


# ---------------------------------------------------------------------------
# Criterion 4: Install/Setup section
# ---------------------------------------------------------------------------

def test_readme_has_setup_section():
    """README contains an Install/Setup section."""
    content = _readme().lower()
    assert any(w in content for w in ["install", "setup", "prerequisite"]), (
        "README missing Install/Setup section"
    )


def test_readme_setup_python_version():
    """Setup mentions Python version requirement."""
    content = _readme().lower()
    assert "python" in content and ("3.1" in content or "3.9" in content or "3.8" in content or "python" in content), (
        "Setup should mention Python version"
    )


def test_readme_setup_venv():
    """Setup mentions virtual environment."""
    content = _readme().lower()
    assert "venv" in content or "virtualenv" in content or "virtual environment" in content, (
        "Setup should mention creating a virtual environment"
    )


def test_readme_setup_dependencies():
    """Setup mentions installing dependencies."""
    content = _readme().lower()
    assert "pip" in content and ("requirements" in content or "install" in content), (
        "Setup should mention pip install / requirements.txt"
    )


def test_readme_setup_env_config():
    """Setup mentions .env / API keys."""
    content = _readme()
    assert ".env" in content, "Setup should mention .env configuration"


def test_readme_setup_api_keys_vision():
    """Setup mentions API keys for vision/image service."""
    content = _readme().lower()
    assert "api" in content and ("key" in content or "keys" in content), (
        "Setup should mention API keys"
    )


def test_readme_setup_api_keys_ebay():
    """Setup mentions eBay API credentials."""
    content = _readme().lower()
    assert "ebay" in content, "Setup should mention eBay API credentials"


def test_readme_setup_db_migrations():
    """Setup mentions database setup or migrations."""
    content = _readme().lower()
    assert "migrat" in content or "database" in content or "createdb" in content, (
        "Setup should mention database setup or migrations"
    )


# ---------------------------------------------------------------------------
# Criterion 5: Usage section
# ---------------------------------------------------------------------------

def test_readme_has_usage_section():
    """README contains a Usage section."""
    content = _readme().lower()
    assert "usage" in content, "README missing 'Usage' section"


def test_readme_usage_upload_example():
    """Usage includes uploading a part photo."""
    content = _readme().lower()
    assert "upload" in content or "photo" in content, (
        "Usage should include uploading a part photo"
    )


def test_readme_usage_approve_example():
    """Usage includes approving a part."""
    content = _readme().lower()
    assert "approve" in content, "Usage should include approving a part"


def test_readme_usage_list_example():
    """Usage includes listing/publishing a part."""
    content = _readme().lower()
    assert "publish" in content or "list" in content or "listing" in content, (
        "Usage should include listing/publishing a part"
    )


def test_readme_usage_cli_commands():
    """Usage includes concrete CLI command examples."""
    content = _readme()
    assert "```bash" in content, "Usage should include bash code blocks with CLI examples"


# ---------------------------------------------------------------------------
# Criterion 6: Project structure section
# ---------------------------------------------------------------------------

def test_readme_has_project_structure_section():
    """README contains a Project Structure section."""
    content = _readme().lower()
    assert "project structure" in content, "README missing 'Project Structure' section"


def test_readme_project_structure_describes_directories():
    """Project Structure describes main modules/directories."""
    content = _readme().lower()
    # Should mention at least a few directories like src/, tests/, config/
    mentioned_dirs = [d for d in ["src", "tests", "config", "marketplace"] if d in content]
    assert len(mentioned_dirs) >= 2, (
        f"Project Structure should describe main directories, found: {mentioned_dirs}"
    )


# ---------------------------------------------------------------------------
# Criterion 7: Contributing section
# ---------------------------------------------------------------------------

def test_readme_has_contributing_section():
    """README contains a Contributing section."""
    content = _readme().lower()
    assert "contributing" in content, "README missing 'Contributing' section"


def test_readme_contributing_fork_branch_pr():
    """Contributing mentions fork, branch, and pull request."""
    content = _readme().lower()
    assert "fork" in content, "Contributing should mention forking"
    assert "branch" in content, "Contributing should mention branches"
    assert "pull request" in content or "pull-request" in content, (
        "Contributing should mention pull requests"
    )


def test_readme_contributing_coding_standards():
    """Contributing mentions coding standards and tests."""
    content = _readme().lower()
    assert any(w in content for w in ["pep 8", "coding standard", "docstring"]), (
        "Contributing should mention coding standards"
    )
    assert "test" in content, "Contributing should mention tests"
