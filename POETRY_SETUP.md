# Poetry Setup Guide for AutoGen-Claude Integration

## Installation

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   
   Or using pip:
   ```bash
   pip install poetry
   ```

2. **Install Project Dependencies**:
   ```bash
   cd autogen-claude-integration
   poetry install
   ```

3. **Install with Optional Dependencies**:
   ```bash
   # Install with all optional dependencies
   poetry install --extras all
   
   # Install with specific extras
   poetry install --extras "langchain websocket"
   ```

## Usage

### Activate Virtual Environment
```bash
poetry shell
```

### Run Commands
```bash
# Run AutoGen CLI
poetry run autogen-claude

# Start Claude API wrapper
poetry run claude-wrapper

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy .
```

### Add New Dependencies
```bash
# Add a production dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Add with specific version
poetry add "package-name>=1.0,<2.0"
```

### Update Dependencies
```bash
# Update all dependencies
poetry update

# Update specific package
poetry update package-name
```

### Build and Publish
```bash
# Build distribution packages
poetry build

# Publish to PyPI (requires credentials)
poetry publish
```

## Development Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes and Test**:
   ```bash
   poetry run pytest
   poetry run black .
   poetry run mypy .
   ```

3. **Update Dependencies** (if needed):
   ```bash
   poetry add new-package
   # This updates pyproject.toml automatically
   ```

4. **Commit Changes**:
   ```bash
   git add pyproject.toml POETRY_SETUP.md
   git commit -m "feat: Add Poetry configuration for dependency management"
   ```

## Troubleshooting

### Poetry Not Found
Add Poetry to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Virtual Environment Issues
```bash
# Remove existing environment
poetry env remove python3.9

# Create new environment
poetry env use python3.9
```

### Lock File Conflicts
```bash
# Regenerate lock file
rm poetry.lock
poetry lock
```

### Installation Errors
```bash
# Clear cache
poetry cache clear pypi --all

# Try verbose install
poetry install -vvv
```

## Integration with VS Code

Add to `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.sortImports.path": "isort",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

## CI/CD Integration

Example GitHub Actions workflow:
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install Poetry
        run: pip install poetry
      - name: Install dependencies
        run: poetry install
      - name: Run tests
        run: poetry run pytest
      - name: Run linting
        run: |
          poetry run black --check .
          poetry run isort --check-only .
          poetry run mypy .
```