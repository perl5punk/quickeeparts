"""Tests validating README.md against the acceptance criteria for the quickeeparts project."""
import os
import re


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _readme():
    """Read and return README.md content."""
    path = os.path.join(ROOT_DIR, "README.md")
    with open(path, "r") as f:
        return f.read()


def _find_section(content, header):
    """Return the text under a given markdown header (## Header)."""
    pattern = r"^## " + re.escape(header) + r"\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


# ── 1. Title and Description ────────────────────────────────────────────

class TestTitleAndDescription:

    def test_readme_exists(self):
        """README.md must exist."""
        path = os.path.join(ROOT_DIR, "README.md")
        assert os.path.isfile(path), "README.md must exist in the repository root"

    def test_project_title_present(self):
        """README.md must include a project title 'quickeeparts'."""
        content = _readme()
        assert "quickeeparts" in content.lower(), "README must include the project title 'quickeeparts'"
        # The title should be a level-1 heading
        assert re.search(r"^# quickeeparts", content, re.MULTILINE | re.IGNORECASE), (
            "README must have '# quickeeparts' as a level-1 heading"
        )

    def test_description_explains_application(self):
        """README must have a one-paragraph description explaining what the app does."""
        content = _readme()
        # Must mention core concepts: shop, parts, identify, value/listing
        mentions_photo = "photo" in content.lower() or "image" in content.lower()
        mentions_identify = "identify" in content.lower() or "recognition" in content.lower()
        mentions_value = "value" in content.lower() or "price" in content.lower()
        mentions_listing = "list" in content.lower() or "eBay" in content.lower()
        assert any([mentions_photo, mentions_identify, mentions_value, mentions_listing]), (
            "Description must explain the app's purpose (photo → identify → value → listing)"
        )


# ── 2. Features section ─────────────────────────────────────────────────

class TestFeatures:

    def test_features_section_exists(self):
        """README must include a Features section."""
        content = _readme()
        section = _find_section(content, "Features")
        assert section, "README must include a '## Features' section"

    def test_feature_photo_capture(self):
        """Features must include photo capture/upload."""
        content = _readme()
        section = _find_section(content, "Features")
        assert re.search(r"(photo|image|upload|capture)", section, re.IGNORECASE), (
            "Features must list photo capture/upload capability"
        )

    def test_feature_ai_identification(self):
        """Features must include AI-powered part identification."""
        content = _readme()
        section = _find_section(content, "Features")
        assert re.search(r"(AI|artificial intelligence|identification|identify)", section, re.IGNORECASE), (
            "Features must list AI-powered part identification"
        )

    def test_feature_demand_value_estimation(self):
        """Features must include demand and value estimation."""
        content = _readme()
        section = _find_section(content, "Features")
        assert re.search(r"(demand|value|price|estimate|cost)", section, re.IGNORECASE), (
            "Features must list demand/value estimation"
        )

    def test_feature_approval_workflow(self):
        """Features must include approval workflow/queue."""
        content = _readme()
        section = _find_section(content, "Features")
        assert re.search(r"(approve|queue|workflow)", section, re.IGNORECASE), (
            "Features must list approval workflow/queue management"
        )

    def test_feature_multi_platform_listing(self):
        """Features must include multi-platform listing (eBay and others)."""
        content = _readme()
        section = _find_section(content, "Features")
        assert re.search(r"(platform|eBay|ebay|multi)", section, re.IGNORECASE), (
            "Features must list multi-platform listing creation (eBay and others)"
        )

    def test_features_bulleted(self):
        """Features must be bulleted/listed."""
        content = _readme()
        section = _find_section(content, "Features")
        bullet_count = len(re.findall(r"^[\s]*[-*•]\s+", section, re.MULTILINE))
        assert bullet_count >= 5, f"Features must list at least 5 items (found {bullet_count})"


# ── 3. How It Works section ─────────────────────────────────────────────

class TestHowItWorks:

    def test_how_it_works_section_exists(self):
        """README must include a How It Works section."""
        content = _readme()
        section = _find_section(content, "How It Works")
        assert section, "README must include a '## How It Works' section"

    def test_how_it_works_describes_capture(self):
        """How It Works must describe capturing/uploading a photo."""
        content = _readme()
        section = _find_section(content, "How It Works")
        assert re.search(r"(capture|photo|image|snap|take)", section, re.IGNORECASE), (
            "How It Works must describe photo capture step"
        )

    def test_how_it_works_describes_identify(self):
        """How It Works must describe AI identification."""
        content = _readme()
        section = _find_section(content, "How It Works")
        assert re.search(r"(identify|recognize|AI|analyze)", section, re.IGNORECASE), (
            "How It Works must describe AI identification step"
        )

    def test_how_it_works_describes_estimate(self):
        """How It Works must describe demand/value estimation."""
        content = _readme()
        section = _find_section(content, "How It Works")
        assert re.search(r"(estimate|demand|value|price|cost)", section, re.IGNORECASE), (
            "How It Works must describe demand/value estimation step"
        )

    def test_how_it_works_describes_queue(self):
        """How It Works must describe queuing."""
        content = _readme()
        section = _find_section(content, "How It Works")
        assert re.search(r"(queue|wait|pending|review)", section, re.IGNORECASE), (
            "How It Works must describe the queue step"
        )

    def test_how_it_works_describes_approve(self):
        """How It Works must describe approval."""
        content = _readme()
        section = _find_section(content, "How It Works")
        assert re.search(r"(approve|approved|review)", section, re.IGNORECASE), (
            "How It Works must describe the approval step"
        )

    def test_how_it_works_describes_list(self):
        """How It Works must describe listing on platforms."""
        content = _readme()
        section = _find_section(content, "How It Works")
        assert re.search(r"(list|eBay|platform|create listing|marketplace)", section, re.IGNORECASE), (
            "How It Works must describe listing creation step"
        )

    def test_how_it_works_explains_end_to_end(self):
        """How It Works must explain the full end-to-end workflow."""
        content = _readme()
        section = _find_section(content, "How It Works")
        # Must mention at least 3 of the 6 steps
        steps_found = sum([
            bool(re.search(r"(capture|photo|snap|take)", section, re.IGNORECASE)),
            bool(re.search(r"(identify|recognize|identify)", section, re.IGNORECASE)),
            bool(re.search(r"(estimate|demand|value|price)", section, re.IGNORECASE)),
            bool(re.search(r"(queue|wait)", section, re.IGNORECASE)),
            bool(re.search(r"(approve|review)", section, re.IGNORECASE)),
            bool(re.search(r"(list|create)", section, re.IGNORECASE)),
        ])
        assert steps_found >= 4, (
            f"How It Works must describe at least 4 of the 6 workflow steps (found {steps_found}): capture → identify → estimate → queue → approve → list"
        )


# ── 4. Project Structure section ────────────────────────────────────────

class TestProjectStructure:

    def test_project_structure_section_exists(self):
        """README must include a Project Structure section."""
        content = _readme()
        section = _find_section(content, "Project Structure")
        assert section, "README must include a '## Project Structure' section"

    def test_project_structure_shows_tree(self):
        """Project Structure must use a tree-style directory listing."""
        content = _readme()
        section = _find_section(content, "Project Structure")
        # Look for tree characters (├──, └──, │)
        assert re.search(r"[├└│]", section), (
            "Project Structure must use a tree-style listing (characters ├──, └──, │)"
        )

    def test_project_structure_shows_top_level(self):
        """Project Structure must show top-level directories."""
        content = _readme()
        section = _find_section(content, "Project Structure")
        assert re.search(r"(src|tests)", section), (
            "Project Structure must show top-level directories like src/ and tests/"
        )


# ── 5. Prerequisites section ────────────────────────────────────────────

class TestPrerequisites:

    def test_prerequisites_section_exists(self):
        """README must include a Prerequisites section."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert section, "README must include a '## Prerequisites' section"

    def test_prerequisites_mentions_python(self):
        """Prerequisites must mention Python."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert re.search(r"python", section, re.IGNORECASE), (
            "Prerequisites must list Python as a required software"
        )

    def test_prerequisites_mentions_python_version(self):
        """Prerequisites must mention a specific Python version."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert re.search(r"python\s*3\.\d+", section, re.IGNORECASE), (
            "Prerequisites must specify a Python version (e.g., Python 3.10)"
        )

    def test_prerequisites_mentions_python_packages(self):
        """Prerequisites must mention Python packages/dependencies."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert re.search(r"(pip|package|dependency|requirements)", section, re.IGNORECASE), (
            "Prerequisites must mention Python packages/dependencies"
        )

    def test_prerequisites_mentions_virtual_env(self):
        """Prerequisites must mention virtual environment."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert re.search(r"(virtual env|venv|isolat)", section, re.IGNORECASE), (
            "Prerequisites must mention virtual environment setup"
        )

    def test_prerequisites_mentions_api_keys(self):
        """Prerequisites must mention external API keys."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert re.search(r"(api key|API|credential)", section, re.IGNORECASE), (
            "Prerequisites must mention external API keys (eBay API, AI service)"
        )

    def test_prerequisites_mentions_ebay_api(self):
        """Prerequisites must specifically mention eBay API."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert re.search(r"(eBay|ebay)", section, re.IGNORECASE), (
            "Prerequisites must mention eBay API credentials"
        )

    def test_prerequisites_mentions_ai_service(self):
        """Prerequisites must mention image recognition/AI service."""
        content = _readme()
        section = _find_section(content, "Prerequisites")
        assert re.search(r"(image recognit|AI|vision|reko|computer vision|Azure|AWS|Google)", section, re.IGNORECASE), (
            "Prerequisites must mention image recognition / AI service"
        )


# ── 6. Installation section ─────────────────────────────────────────────

class TestInstallation:

    def test_installation_section_exists(self):
        """README must include an Installation section."""
        content = _readme()
        section = _find_section(content, "Installation")
        assert section, "README must include a '## Installation' section"

    def test_installation_has_step_by_step(self):
        """Installation must have step-by-step instructions."""
        content = _readme()
        section = _find_section(content, "Installation")
        numbered = len(re.findall(r"(?:^|\n)\s*\d+[\.]\s+", section))
        assert numbered >= 3, f"Installation must have at least 3 steps (found {numbered})"

    def test_installation_mentions_venv(self):
        """Installation must mention virtual environment setup."""
        content = _readme()
        section = _find_section(content, "Installation")
        assert re.search(r"(venv|virtual env|python3 -m venv)", section, re.IGNORECASE), (
            "Installation must include virtual environment setup step"
        )

    def test_installation_mentions_dependencies(self):
        """Installation must mention installing dependencies."""
        content = _readme()
        section = _find_section(content, "Installation")
        assert re.search(r"(pip install|requirements)", section, re.IGNORECASE), (
            "Installation must include dependency installation step"
        )


# ── 7. Configuration section ────────────────────────────────────────────

class TestConfiguration:

    def test_configuration_section_exists(self):
        """README must include a Configuration section."""
        content = _readme()
        section = _find_section(content, "Configuration")
        assert section, "README must include a '## Configuration' section"

    def test_configuration_documents_env_vars(self):
        """Configuration must document environment variables."""
        content = _readme()
        section = _find_section(content, "Configuration")
        assert re.search(r"(EBAY|DATABASE|SECRET|AI_|APPROVAL|ALLOWED|\.env)", section, re.IGNORECASE), (
            "Configuration must document required environment variables"
        )

    def test_configuration_documents_ebay_api(self):
        """Configuration must document eBay API configuration."""
        content = _readme()
        section = _find_section(content, "Configuration")
        assert re.search(r"(EBAY|eBay)", section, re.IGNORECASE), (
            "Configuration must document eBay API configuration"
        )

    def test_configuration_documents_ai_service(self):
        """Configuration must document AI service configuration."""
        content = _readme()
        section = _find_section(content, "Configuration")
        assert re.search(r"(AI_|image recognit|vision|reko)", section, re.IGNORECASE), (
            "Configuration must document AI / image recognition service configuration"
        )

    def test_configuration_documents_database(self):
        """Configuration must document database configuration."""
        content = _readme()
        section = _find_section(content, "Configuration")
        assert re.search(r"(DATABASE|postgres|sqlite|database)", section, re.IGNORECASE), (
            "Configuration must document database configuration"
        )


# ── 8. Usage Examples section ───────────────────────────────────────────

class TestUsageExamples:

    def test_usage_examples_section_exists(self):
        """README must include a Usage Examples section."""
        content = _readme()
        section = _find_section(content, "Usage Examples")
        assert section, "README must include a '## Usage Examples' section"

    def test_example_upload_photo(self):
        """Usage Examples must demonstrate uploading a part photo."""
        content = _readme()
        section = _find_section(content, "Usage Examples")
        assert re.search(r"(upload-photo|upload.*photo|upload.*image)", section, re.IGNORECASE), (
            "Usage Examples must include an example for uploading a part photo"
        )

    def test_example_check_identification(self):
        """Usage Examples must demonstrate checking part identification."""
        content = _readme()
        section = _find_section(content, "Usage Examples")
        assert re.search(r"(check-identification|check.*identification|identify.*--id)", section, re.IGNORECASE), (
            "Usage Examples must include an example for checking part identification"
        )

    def test_example_view_queue(self):
        """Usage Examples must demonstrate viewing the approval queue."""
        content = _readme()
        section = _find_section(content, "Usage Examples")
        assert re.search(r"(view-queue|view.*queue|queue)", section, re.IGNORECASE), (
            "Usage Examples must include an example for viewing the approval queue"
        )

    def test_example_list_approved_part(self):
        """Usage Examples must demonstrate listing an approved part."""
        content = _readme()
        section = _find_section(content, "Usage Examples")
        assert re.search(r"(list-part|list.*approved|approve.*list|create.*list)", section, re.IGNORECASE), (
            "Usage Examples must include an example for listing an approved part"
        )

    def test_examples_are_runnable_commands(self):
        """Usage Examples must include concrete, runnable command examples."""
        content = _readme()
        section = _find_section(content, "Usage Examples")
        # Look for fenced code blocks (```bash ... ```)
        code_blocks = re.findall(r"```(?:\w+)\s*\n(.*?)\n```", section, re.DOTALL)
        command_blocks = [b for b in code_blocks if re.search(r"(python |pytest |pip |cp )", b)]
        assert len(command_blocks) >= 4, (
            f"Usage Examples must include at least 4 runnable command examples (found {len(command_blocks)})"
        )


# ── 9. Testing section ──────────────────────────────────────────────────

class TestTesting:

    def test_testing_section_exists(self):
        """README must include a Testing section."""
        content = _readme()
        section = _find_section(content, "Testing")
        assert section, "README must include a '## Testing' section"

    def test_testing_mentions_pytest(self):
        """Testing must mention pytest."""
        content = _readme()
        section = _find_section(content, "Testing")
        assert re.search(r"pytest", section, re.IGNORECASE), (
            "Testing section must mention pytest as the test runner"
        )

    def test_testing_has_commands(self):
        """Testing must include commands to run the test suite."""
        content = _readme()
        section = _find_section(content, "Testing")
        assert re.search(r"pytest", section), (
            "Testing section must include commands showing how to run pytest"
        )


# ── 10. License section ─────────────────────────────────────────────────

class TestLicense:

    def test_license_section_exists(self):
        """README must include a License section."""
        content = _readme()
        section = _find_section(content, "License")
        assert section, "README must include a '## License' section"

    def test_license_mentions_license(self):
        """License section must mention a license type."""
        content = _readme()
        section = _find_section(content, "License")
        assert re.search(r"(MIT|Apache|BSD|GPL|License|licen)", section, re.IGNORECASE), (
            "License section must specify a license type (e.g., MIT License)"
        )


# ── 11. Formatting ──────────────────────────────────────────────────────

class TestFormatting:

    def test_has_section_headers(self):
        """README must use proper Markdown section headers (##)."""
        content = _readme()
        headers = re.findall(r"^## .+$", content, re.MULTILINE)
        assert len(headers) >= 8, (
            f"README must have at least 8 section headers (found {len(headers)}): {headers}"
        )

    def test_has_code_blocks(self):
        """README must use code blocks for commands."""
        content = _readme()
        blocks = re.findall(r"```(?:\w+)?\n(.*?)```", content, re.DOTALL)
        assert len(blocks) >= 5, (
            f"README must include at least 5 code blocks (found {len(blocks)})"
        )
