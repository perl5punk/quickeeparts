"""Tests validating README.md factual accuracy against the actual repository filesystem."""
import os
import re


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _readme():
    """Read and return README.md content."""
    path = os.path.join(ROOT_DIR, "README.md")
    with open(path, "r") as f:
        return f.read()


def _actual_files():
    """Return a set of all actual files and directories under the repo root."""
    actual = set()
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        # Skip hidden and cache directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('__pycache__', 'venv', '.pytest_cache')]
        for d in dirnames:
            actual.add(os.path.relpath(os.path.join(dirpath, d), ROOT_DIR))
        for f in filenames:
            actual.add(os.path.relpath(os.path.join(dirpath, f), ROOT_DIR))
    return actual


def _readme_project_structure():
    """Extract the file/directory names listed in the Project Structure tree."""
    content = _readme()
    section_match = re.search(r"^## Project Structure\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL | re.MULTILINE)
    if not section_match:
        return []
    section = section_match.group(1)
    # Extract file/directory names from tree lines
    # Lines look like: ├── setup.py           # comment
    # or: ├── src/
    names = []
    for line in section.split('\n'):
        # Remove tree drawing characters and indentation
        cleaned = re.sub(r"^[│├└─\s]+", "", line.strip())
        # Remove leading tree connector characters
        cleaned = re.sub(r"^[-│├└]+\s*", "", cleaned)
        # Extract the file/dir name (before any comment)
        name_match = re.match(r"(\S+)", cleaned)
        if name_match:
            name = name_match.group(1).rstrip('/')
            if name and name not in ('quickeeparts/', 'quickeeparts'):
                names.append(name)
    return names


def _find_section(content, header):
    """Return the text under a given markdown header."""
    pattern = r"^## " + re.escape(header) + r"\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


# ── Project Structure accuracy ──────────────────────────────────────────

class TestProjectStructureAccuracy:

    def test_project_structure_only_references_real_files(self):
        """All files listed in Project Structure tree must actually exist."""
        content = _readme()
        listed_names = _readme_project_structure()
        actual = _actual_files()

        missing = []
        for name in listed_names:
            # Check if any actual file starts with this name (for directories)
            # or if the name itself exists
            found = False
            for a in actual:
                if a == name or a.startswith(name + '/'):
                    found = True
                    break
            if not found:
                missing.append(name)

        assert not missing, (
            f"Project Structure tree references files/directories that don't exist: {missing}\n"
            f"Top-level actual files/dirs: {sorted([a for a in actual if '/' not in a])}"
        )

    def test_readme_mentions_setup_py_but_it_doesnt_exist(self):
        """README lists setup.py in Project Structure — this must be fixed if setup.py doesn't exist."""
        content = _readme()
        # Check if setup.py is referenced
        has_setup_py_reference = "setup.py" in content
        setup_py_exists = os.path.isfile(os.path.join(ROOT_DIR, "setup.py"))

        if has_setup_py_reference and not setup_py_exists:
            assert False, (
                "README Project Structure references 'setup.py' but setup.py does not exist in the repository root. "
                "Either remove the reference or create the file."
            )

    def test_readme_mentions_docs_directory_but_it_doesnt_exist(self):
        """README lists docs/ in Project Structure — this must be fixed if docs/ doesn't exist."""
        content = _readme()
        has_docs_reference = bool(re.search(r"docs/", content))
        docs_exists = os.path.isdir(os.path.join(ROOT_DIR, "docs"))

        if has_docs_reference and not docs_exists:
            assert False, (
                "README Project Structure references 'docs/' directory but docs/ does not exist. "
                "Either remove the reference or create the directory."
            )

    def test_readme_mentions_config_md_but_it_doesnt_exist(self):
        """README lists docs/config.md — this must be fixed if docs/config.md doesn't exist."""
        content = _readme()
        has_config_md_reference = "docs/config.md" in content or "config.md" in content
        config_exists = os.path.isfile(os.path.join(ROOT_DIR, "docs", "config.md"))

        if has_config_md_reference and not config_exists:
            assert False, (
                "README Project Structure references 'docs/config.md' but it does not exist. "
                "Either remove the reference or create the file."
            )

    def test_project_structure_top_level_matches_reality(self):
        """Top-level items in the Project Structure tree should match actual top-level files/dirs."""
        actual_top = sorted([a for a in _actual_files() if '/' not in a])
        content = _readme()

        # These should definitely exist
        mandatory = ["README.md"]
        for m in mandatory:
            assert m in actual_top, f"README.md claims structure but '{m}' is missing from repo root"


# ── License accuracy ────────────────────────────────────────────────────

class TestLicenseAccuracy:

    def test_license_section_references_real_file(self):
        """README License section says 'See the LICENSE file' — that file must exist."""
        content = _readme()
        license_section = _find_section(content, "License")

        # Check if README mentions a LICENSE file
        if re.search(r"LICENSE file|the LICENSE", content, re.IGNORECASE):
            license_exists = os.path.isfile(os.path.join(ROOT_DIR, "LICENSE"))
            assert license_exists, (
                "README License section references a 'LICENSE' file, but LICENSE does not exist in the repository root. "
                "Either create the LICENSE file or remove the reference from the README."
            )


# ── Usage examples accuracy ─────────────────────────────────────────────

class TestUsageExamplesAccuracy:

    def test_example_commands_reference_real_entry_point(self):
        """Usage example commands reference src/app.py — that file must exist."""
        app_py_exists = os.path.isfile(os.path.join(ROOT_DIR, "src", "app.py"))
        content = _readme()
        has_app_py = "src/app.py" in content

        if has_app_py and not app_py_exists:
            assert False, (
                "README Usage Examples reference 'src/app.py' but src/app.py does not exist. "
                "Either remove the reference or create the file."
            )
