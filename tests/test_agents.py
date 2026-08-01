"""Tests validating AGENTS.md against the acceptance criteria for branch management and Python best practices guidelines."""
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _agents():
    """Read and return AGENTS.md content."""
    path = os.path.join(ROOT_DIR, "AGENTS.md")
    with open(path, "r") as f:
        return f.read()


def _find_section(content, header):
    """Return the text under a given markdown header (## Header)."""
    pattern = r"^## " + re.escape(header) + r"\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


class TestAGENTSExists:
    """Test that AGENTS.md exists and is properly formatted."""

    def test_agents_md_exists(self):
        """AGENTS.md must exist in the repository root."""
        path = os.path.join(ROOT_DIR, "AGENTS.md")
        assert os.path.isfile(path), "AGENTS.md must exist in the repository root"

    def test_agents_has_title_heading(self):
        """AGENTS.md must have a level-1 heading as title."""
        content = _agents()
        assert re.search(r"^# ", content, re.MULTILINE), (
            "AGENTS.md must have a level-1 heading (e.g. '# Developer Guidelines')"
        )

    def test_agents_formatted_with_headings(self):
        """AGENTS.md must be formatted with clear section headings (##)."""
        content = _agents()
        sections = re.findall(r"^## \S.*$", content, re.MULTILINE)
        assert len(sections) >= 6, (
            f"AGENTS.md must have at least 6 section headings, found {len(sections)}: {sections}"
        )

    def test_agents_formatted_with_bullet_points(self):
        """AGENTS.md must use bullet points for guideline items."""
        content = _agents()
        bullets = re.findall(r"^-\s+\S", content, re.MULTILINE)
        assert len(bullets) >= 15, (
            f"AGENTS.md must have meaningful bullet-point content, found {len(bullets)} bullets"
        )


class TestBranchManagement:
    """Test the Branch Management section."""

    def test_branch_management_section_exists(self):
        """AGENTS.md must contain a 'Branch Management' section."""
        content = _agents()
        section = _find_section(content, "Branch Management")
        assert section, "AGENTS.md must have a '## Branch Management' section"

    def test_branch_management_latest_main(self):
        """Branch Management must advise working from the latest main branch."""
        content = _agents()
        section = _find_section(content, "Branch Management")
        assert section, "AGENTS.md must have a '## Branch Management' section"
        section_lower = section.lower()
        assert "latest main" in section_lower or "latest.*main" in section_lower, (
            "Branch Management must advise working from the latest main branch"
        )

    def test_branch_management_pull_before_start(self):
        """Branch Management must advise pulling changes before starting tasks."""
        content = _agents()
        section = _find_section(content, "Branch Management")
        assert section, "AGENTS.md must have a '## Branch Management' section"
        assert "pull" in section.lower(), (
            "Branch Management must advise pulling changes before starting tasks"
        )

    def test_branch_management_merge_to_main(self):
        """Branch Management must advise ensuring final changes are merged to main."""
        content = _agents()
        section = _find_section(content, "Branch Management")
        assert section, "AGENTS.md must have a '## Branch Management' section"
        assert "merged to main" in section.lower() or "merged.*main" in section.lower(), (
            "Branch Management must advise ensuring final changes are merged to main"
        )

    def test_branch_management_git_pull_command(self):
        """Branch Management must reference running git pull."""
        content = _agents()
        section = _find_section(content, "Branch Management")
        assert "git pull" in section, (
            "Branch Management must reference running `git pull origin main`"
        )


class TestPythonBestPractices:
    """Test the Python Best Practices section."""

    def test_python_best_practices_section_exists(self):
        """AGENTS.md must contain a 'Python Best Practices' section."""
        content = _agents()
        section = _find_section(content, "Python Best Practices")
        assert section, "AGENTS.md must have a '## Python Best Practices' section"

    def test_python_flask_app_factory(self):
        """Python Best Practices must mention Flask app factory pattern."""
        content = _agents()
        section = _find_section(content, "Python Best Practices")
        assert section, "AGENTS.md must have a '## Python Best Practices' section"
        assert "flask" in section.lower() and "app factory" in section.lower(), (
            "Python Best Practices must cover the Flask app factory pattern"
        )

    def test_python_error_handling(self):
        """Python Best Practices must mention error handling with try/except."""
        content = _agents()
        section = _find_section(content, "Python Best Practices")
        assert section, "AGENTS.md must have a '## Python Best Practices' section"
        assert "try" in section.lower() and "except" in section.lower(), (
            "Python Best Practices must cover error handling with try/except blocks"
        )

    def test_python_no_known_failures(self):
        """Python Best Practices must mention not committing broken code."""
        content = _agents()
        section = _find_section(content, "Python Best Practices")
        assert section, "AGENTS.md must have a '## Python Best Practices' section"
        assert "known failures" in section.lower() or "known.*failures" in section.lower(), (
            "Python Best Practices must advise not committing code that has known failures"
        )

    def test_python_test_before_completion(self):
        """Python Best Practices must advise testing changes before completion."""
        content = _agents()
        section = _find_section(content, "Python Best Practices")
        assert section, "AGENTS.md must have a '## Python Best Practices' section"
        assert "test" in section.lower() and "completion" in section.lower(), (
            "Python Best Practices must advise testing changes before claiming completion"
        )

    def test_python_validate_imports(self):
        """Python Best Practices must mention validating imports and dependencies."""
        content = _agents()
        section = _find_section(content, "Python Best Practices")
        assert section, "AGENTS.md must have a '## Python Best Practices' section"
        assert "validate" in section.lower() and ("import" in section.lower() or "dependency" in section.lower()), (
            "Python Best Practices must advise validating imports and dependencies"
        )


class TestSandboxTesting:
    """Test the Sandbox Testing section."""

    def test_sandbox_testing_section_exists(self):
        """AGENTS.md must contain a 'Sandbox Testing' section."""
        content = _agents()
        section = _find_section(content, "Sandbox Testing")
        assert section, "AGENTS.md must have a '## Sandbox Testing' section"

    def test_sandbox_test_before_commit(self):
        """Sandbox Testing must advise testing code in sandbox before committing."""
        content = _agents()
        section = _find_section(content, "Sandbox Testing")
        assert section, "AGENTS.md must have a '## Sandbox Testing' section"
        assert "sandbox" in section.lower() and "commit" in section.lower(), (
            "Sandbox Testing must advise testing code in sandbox before committing"
        )

    def test_sandbox_verify_dependencies(self):
        """Sandbox Testing must advise verifying dependencies are installed."""
        content = _agents()
        section = _find_section(content, "Sandbox Testing")
        assert section, "AGENTS.md must have a '## Sandbox Testing' section"
        assert "dependenc" in section.lower(), (
            "Sandbox Testing must advise verifying all dependencies are installed"
        )

    def test_sandbox_app_runs(self):
        """Sandbox Testing must advise verifying the app runs successfully."""
        content = _agents()
        section = _find_section(content, "Sandbox Testing")
        assert section, "AGENTS.md must have a '## Sandbox Testing' section"
        assert ("run" in section.lower() and "successful" in section.lower()) or (
            "app" in section.lower() and "run" in section.lower()
        ), (
            "Sandbox Testing must advise verifying the app runs successfully"
        )

    def test_sandbox_database_init(self):
        """Sandbox Testing must advise checking database initialization."""
        content = _agents()
        section = _find_section(content, "Sandbox Testing")
        assert section, "AGENTS.md must have a '## Sandbox Testing' section"
        assert "database" in section.lower() and "init" in section.lower(), (
            "Sandbox Testing must advise checking that database initialization works"
        )

    def test_sandbox_templates_render(self):
        """Sandbox Testing must advise confirming templates render correctly."""
        content = _agents()
        section = _find_section(content, "Sandbox Testing")
        assert section, "AGENTS.md must have a '## Sandbox Testing' section"
        assert "template" in section.lower() and "render" in section.lower(), (
            "Sandbox Testing must advise confirming templates render correctly"
        )


class TestGitWorkflow:
    """Test the Git Workflow section."""

    def test_git_workflow_section_exists(self):
        """AGENTS.md must contain a 'Git Workflow' section."""
        content = _agents()
        section = _find_section(content, "Git Workflow")
        assert section, "AGENTS.md must have a '## Git Workflow' section"

    def test_git_meaningful_commit_messages(self):
        """Git Workflow must advise writing meaningful commit messages."""
        content = _agents()
        section = _find_section(content, "Git Workflow")
        assert section, "AGENTS.md must have a '## Git Workflow' section"
        assert "meaningful" in section.lower() and "commit message" in section.lower(), (
            "Git Workflow must advise writing meaningful commit messages"
        )

    def test_git_atomic_commits(self):
        """Git Workflow must advise keeping commits focused and atomic."""
        content = _agents()
        section = _find_section(content, "Git Workflow")
        assert section, "AGENTS.md must have a '## Git Workflow' section"
        assert "atomic" in section.lower() or "focused" in section.lower(), (
            "Git Workflow must advise keeping commits focused and atomic"
        )

    def test_git_push_to_main(self):
        """Git Workflow must advise pushing changes to main after verification."""
        content = _agents()
        section = _find_section(content, "Git Workflow")
        assert section, "AGENTS.md must have a '## Git Workflow' section"
        assert "push" in section.lower() and "main" in section.lower(), (
            "Git Workflow must advise pushing changes to main after verification"
        )

    def test_git_no_orphan_feature_branches(self):
        """Git Workflow must advise not leaving work on feature branches without merging."""
        content = _agents()
        section = _find_section(content, "Git Workflow")
        assert section, "AGENTS.md must have a '## Git Workflow' section"
        assert "feature" in section.lower() and "merg" in section.lower(), (
            "Git Workflow must advise not leaving work on feature branches without merging to main"
        )


class TestFileOrganization:
    """Test the File Organization section."""

    def test_file_organization_section_exists(self):
        """AGENTS.md must contain a 'File Organization' section."""
        content = _agents()
        section = _find_section(content, "File Organization")
        assert section, "AGENTS.md must have a '## File Organization' section"

    def test_file_organization_project_structure(self):
        """File Organization must reference existing project structure (app.py, templates/, src/, tests/)."""
        content = _agents()
        section = _find_section(content, "File Organization")
        assert section, "AGENTS.md must have a '## File Organization' section"
        assert "app.py" in section, (
            "File Organization must reference app.py at root"
        )
        assert "templates" in section, (
            "File Organization must reference templates/ directory"
        )
        assert "tests" in section, (
            "File Organization must reference tests/ directory"
        )

    def test_file_organization_no_new_dirs_without_justification(self):
        """File Organization must advise against creating new directories without justification."""
        content = _agents()
        section = _find_section(content, "File Organization")
        assert section, "AGENTS.md must have a '## File Organization' section"
        assert "justif" in section.lower(), (
            "File Organization must advise not creating new directories without justification"
        )

    def test_file_organization_update_readme(self):
        """File Organization must advise updating README.md to reflect actual file locations."""
        content = _agents()
        section = _find_section(content, "File Organization")
        assert section, "AGENTS.md must have a '## File Organization' section"
        assert "readme" in section.lower(), (
            "File Organization must advise updating README.md to reflect actual file locations"
        )


class TestCardManagement:
    """Test the Card Management section."""

    def test_card_management_section_exists(self):
        """AGENTS.md must contain a 'Card Management' section."""
        content = _agents()
        section = _find_section(content, "Card Management")
        assert section, "AGENTS.md must have a '## Card Management' section"

    def test_card_management_check_duplicates(self):
        """Card Management must advise checking for duplicate cards."""
        content = _agents()
        section = _find_section(content, "Card Management")
        assert section, "AGENTS.md must have a '## Card Management' section"
        assert "duplic" in section.lower(), (
            "Card Management must advise checking existing cards before creating duplicates"
        )

    def test_card_management_update_blocked_cards(self):
        """Card Management must advise updating blocked cards instead of creating new ones."""
        content = _agents()
        section = _find_section(content, "Card Management")
        assert section, "AGENTS.md must have a '## Card Management' section"
        assert "block" in section.lower() or "update" in section.lower(), (
            "Card Management must advise updating blocked cards instead of creating new ones"
        )

    def test_card_management_reference_related(self):
        """Card Management must advise referencing related cards."""
        content = _agents()
        section = _find_section(content, "Card Management")
        assert section, "AGENTS.md must have a '## Card Management' section"
        assert "reference" in section.lower() or "related" in section.lower(), (
            "Card Management must advise referencing related cards when relevant"
        )
