# Developer Guidelines

## Branch Management

- **ALWAYS work from the latest main branch** — Before starting any task, ensure you're on main and pull the latest changes
- **Never work on outdated branches** — If you see commits or references to old branches, they are stale and should be ignored
- **Verify your branch is current** — Run `git pull origin main` at the start of every task to ensure you have the latest code
- **After completing work, ensure changes are merged to main** — Work on feature branches if needed, but the final deliverable must be on main

## Python Best Practices

- Use application factory pattern (Flask app factory)
- Proper error handling with try/except blocks
- Don't commit code that has known failures
- Test changes before claiming completion
- Validate imports and dependencies before running

## Sandbox Testing

- Always test code in the sandbox before committing
- Ensure all dependencies are installed
- Verify the app runs successfully after your changes
- Check that database initialization works
- Confirm templates render correctly

## Git Workflow

- Write meaningful commit messages
- Keep commits focused and atomic
- Push changes to main after verification
- Don't leave work on feature branches without merging to main

## File Organization

- Follow existing project structure (app.py at root, templates/, src/, tests/)
- Don't create new directories without justification
- Update README.md to reflect actual file locations

## Card Management

- Check existing cards before creating duplicates
- Update blocked cards instead of creating new ones
- Reference related cards when relevant
