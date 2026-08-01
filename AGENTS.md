# AGENTS.md — Guidelines for AI Agents

These guidelines are for AI agents working on this Python project. Follow them carefully to ensure quality, consistency, and reliability.

---

## Sandbox Testing

When running or testing code in the sandbox, you must exercise diligence and verify that your work is sound before claiming completion.

- **Always use proper error handling.** Wrap potentially-failing operations in `try`/`except` blocks. Never leave bare `except` clauses — always catch a specific exception type.
- **Never commit code that has known failures.** If a test fails or an error occurs, fix the root cause before proceeding. Do not commit broken code with the intention of fixing it later.
- **Test all changes in the sandbox before committing.** Validate that the code runs end-to-end in the sandbox environment. Simulate the conditions under which the code will be used.
- **Validate imports and dependencies before running code.** Confirm that all required packages are installed and available. Use `pip install` to install missing dependencies before attempting to run or import them.
- **Handle exceptions gracefully.** When catching exceptions, log or surface meaningful error messages. Never silently swallow errors.

---

## General Python Best Practices

Follow these principles when writing or modifying Python code in this project.

- **Use type hints where appropriate.** Annotate function signatures and key variables with types to improve code readability and enable static analysis. Use `from __future__ import annotations` if needed for forward references.
- **Follow PEP 8 style guidelines.** Maintain consistent indentation, spacing, and naming conventions. Use descriptive variable and function names. Keep line lengths reasonable (≤120 characters).
- **Avoid hardcoding values.** Use config files, environment variables, or application config objects instead of magic numbers and strings. This makes the code portable and configurable.
- **Use the application factory pattern.** This project follows the Flask application factory pattern. Create your Flask app inside a factory function rather than at module level.
- **Properly initialize the database.** Ensure the database schema is created and migrations are applied before use. Handle database connection errors gracefully.
- **Use context managers for resource management.** Use `with` statements for file I/O, database connections, HTTP requests, and any other resource that needs cleanup. This ensures resources are properly released even if an error occurs.

---

## Making Changes to Existing Code

When modifying existing code, exercise restraint and consistency.

- **Read existing files before writing or modifying code.** Understand the current implementation, its conventions, and its dependencies before making changes. Never modify code based on assumptions.
- **Ensure consistency with the existing codebase style and patterns.** Match the naming conventions, formatting, and architectural patterns already present. If you are unsure, check nearby code for the established style.
- **Don't remove existing functionality without clear reason.** Every existing feature or behavior was added for a reason. If you need to replace something, provide a documented justification and a tested alternative.
- **Keep changes focused and minimal.** Make one logical change per commit. Avoid refactoring unrelated code, changing formatting across large files, or bundling multiple features into a single commit. This makes diffs easier to review and roll back if necessary.

---

## Sandbox-Specific Behavior

The sandbox is your testing ground — use it wisely to catch problems before they reach production.

- **Always verify the code runs successfully before claiming a task is complete.** Run the full test suite and manually verify edge cases. If you cannot get the code to run in the sandbox, do not claim completion.
- **Catch and handle exceptions gracefully.** Never leave bare `except` clauses or suppress errors silently. Always handle specific exception types and provide meaningful error messages. Log errors with sufficient context to aid debugging.
- **Don't assume dependencies are available.** Always install missing dependencies before running code. Check for required packages first, then install them using `pip install`. Verify installation succeeded before proceeding.
- **Confirm the sandbox environment is clean.** Before running tests, ensure your virtual environment is properly set up and free of stale artifacts. Clean up temporary files and cached data that could interfere with results.
- **Document any non-obvious workarounds.** If you need a workaround for a sandbox-specific limitation, document it clearly so other agents understand the rationale.
