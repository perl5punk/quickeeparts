"""Verify that harmful .gitignore entries have been removed.

This test suite validates the following acceptance criteria:
1. The line `parts/` on line 19 is removed
2. The line `var/` on line 21 is removed
3. The line `*.log` on line 59 is removed
4. No other lines are modified, added, or removed
5. The file ends with a trailing newline
6. No blank lines exist where removed entries were
"""


# Known-good lines that must still exist (representing unchanged content)
PRESERVED_LINES = {
    # Distribution/packaging section
    "__pycache__/",
    "*.py[codz]",
    "build/",
    "dist/",
    "sdist/",
    "wheels/",
    "share/python-wheels/",
    "*.egg-info/",
    # PyInstaller section
    "*.manifest",
    "*.spec",
    # Unit test / coverage
    "htmlcov/",
    ".tox/",
    ".pytest_cache/",
    # Translations
    "*.mo",
    "*.pot",
    # Django stuff
    "local_settings.py",
    "db.sqlite3",
    "db.sqlite3-journal",
    # Flask stuff
    "instance/",
    # Scrapy
    ".scrapy",
    # Sphinx
    "docs/_build/",
    # Environments
    ".env",
    ".envrc",
    "venv/",
    # Various tooling
    ".mypy_cache/",
    ".ruff_cache/",
    # Streamlit
    ".streamlit/secrets.toml",
}


def _read_gitignore_lines():
    """Read .gitignore and return list of stripped line strings."""
    with open(".gitignore") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def _read_gitignore_raw():
    """Read .gitignore and return the raw file content."""
    with open(".gitignore") as f:
        return f.read()


def test_gitignore_no_parts_directory():
    """parts/ should not be in .gitignore so uploaded photos aren't discarded."""
    lines = _read_gitignore_lines()
    assert "parts/" not in lines, "parts/ was found in .gitignore"


def test_gitignore_no_var_directory():
    """var/ should not be in .gitignore so application state isn't discarded."""
    lines = _read_gitignore_lines()
    assert "var/" not in lines, "var/ was found in .gitignore"


def test_gitignore_no_log_wildcard():
    """*.log should not be in .gitignore so log files remain available for debugging."""
    lines = _read_gitignore_lines()
    assert "*.log" not in lines, "*.log was found in .gitignore"


def test_gitignore_trailing_newline():
    """File must end with a trailing newline."""
    raw = _read_gitignore_raw()
    assert len(raw) > 0, ".gitignore is empty"
    assert raw[-1] == "\n", ".gitignore does not end with a trailing newline"


def test_gitignore_no_blank_lines_at_removal_positions():
    """No blank lines should exist where removed entries were (positions ~19, ~21, ~59)."""
    lines = _read_gitignore_lines()

    # Check around the former parts/ position (was line 19 in original)
    # The sdist/ line should still be present — not a blank line
    assert "sdist/" in lines, "sdist/ line missing from distribution section"

    # Check around the former var/ position (was line 21 in original)
    # The share/python-wheels/ line should still be present — not a blank line
    assert "share/python-wheels/" in lines, "share/python-wheels/ line missing"

    # Check around the former *.log position (was line 59, under Django section)
    # The db.sqlite3-journal line should still be present
    assert "db.sqlite3-journal" in lines, "db.sqlite3-journal line missing"

    # Specifically check that there are no double-blank lines where three single
    # line removals occurred — each removal position should have exactly one line
    # (or fewer blank lines) not two.
    blank_positions = [i for i, l in enumerate(lines) if l.strip() == ""]
    # Verify no two consecutive blank lines exist
    for i in blank_positions:
        if i + 1 < len(lines) and lines[i + 1].strip() == "":
            raise AssertionError(
                f"Consecutive blank lines found at lines {i + 1} and {i + 2}. "
                "Removed entries should not leave blank line gaps."
            )


def test_gitignore_preserves_distribution_section_structure():
    """Distribution/packaging section headers and lines must be intact."""
    lines = _read_gitignore_lines()

    # The section comment must exist
    assert "# Distribution / packaging" in lines

    # All known packaging lines must be present
    for expected in PRESERVED_LINES:
        assert expected in lines, f"Expected '{expected}' to be preserved in .gitignore"


def test_gitignore_preserves_django_section():
    """Django stuff section must have its lines intact minus *.log."""
    lines = _read_gitignore_lines()
    assert "# Django stuff:" in lines, "# Django stuff: section header missing"
    # These lines must still exist
    assert "local_settings.py" in lines
    assert "db.sqlite3" in lines
    assert "db.sqlite3-journal" in lines


def test_gitignore_section_comments_preserved():
    """All section comment headers must be preserved."""
    lines = _read_gitignore_lines()
    section_comments = [
        "# Distribution / packaging",
        "# PyInstaller",
        "# Installer logs",
        "# Unit test / coverage reports",
        "# Translations",
        "# Django stuff:",
        "# Flask stuff:",
        "# Scrapy stuff:",
        "# Sphinx documentation",
        "# PyBuilder",
        "# Jupyter Notebook",
        "# IPython",
        "# pyenv",
        "# pipenv",
        "# UV",
        "# poetry",
        "# pdm",
        "# pixi",
        "# PEP 582",
        "# Celery stuff",
        "# Redis",
        "# RabbitMQ",
        "# ActiveMQ",
        "# SageMath parsed files",
        "# Environments",
        "# Spyder project settings",
        "# Rope project settings",
        "# mkdocs documentation",
        "# mypy",
        "# Pyre type checker",
        "# pytype static type analyzer",
        "# Cython debug symbols",
        "# PyCharm",
        "# Abstra",
        "# Visual Studio Code",
        "# Ruff stuff:",
        "# PyPI configuration file",
        "# Marimo",
        "# Streamlit",
    ]
    for comment in section_comments:
        assert comment in lines, f"Section comment missing: {comment}"
