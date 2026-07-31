"""Verify that harmful .gitignore entries have been removed."""


def test_gitignore_no_parts_directory():
    """parts/ should not be in .gitignore so uploaded photos aren't discarded."""
    with open(".gitignore") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    assert "parts/" not in lines, "parts/ was found in .gitignore"


def test_gitignore_no_var_directory():
    """var/ should not be in .gitignore so application state isn't discarded."""
    with open(".gitignore") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    assert "var/" not in lines, "var/ was found in .gitignore"


def test_gitignore_no_log_wildcard():
    """*.log should not be in .gitignore so log files remain available for debugging."""
    with open(".gitignore") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    assert "*.log" not in lines, "*.log was found in .gitignore"
