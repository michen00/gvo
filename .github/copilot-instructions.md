# Repository Instructions for GitHub Copilot

Welcome to **GVO** (Guidance vs. Outlines) — a comparative analysis and benchmarking project for structured generation libraries in Python. This file provides comprehensive guidance for generating high-quality, contextually appropriate code contributions.

---

## 1) High‑Level Details

### Project Purpose

GVO evaluates and compares two popular structured generation libraries for Large Language Models:

- **Guidance** ([guidance-ai/guidance](https://github.com/guidance-ai/guidance)): Python-first DSL with interleaved control flow, fine-grained constraints (regex/CFG grammars), token healing, and notebook widgets. Best for: programmatic orchestration, custom generation loops, and advanced constraint experiments.

- **Outlines** ([dottxt-ai/outlines](https://github.com/dottxt-ai/outlines)): Schema-first API using Python types (Literal, BaseModel, Regex) for guaranteed structured outputs. Best for: production pipelines requiring validated JSON-like payloads with minimal glue code.

### Project Goals

1. **Cross-Library Tutorial Implementations**: Reimplement each library's tutorials using the other library to demonstrate equivalent patterns and identify strengths/weaknesses.
2. **Dynamic Task-Based Evaluation**: Benchmark performance metrics including correctness (edit distance, embedding similarity), latency (TTFT, completion time), and cost estimation.
3. **Objective Task Testing**: Generate standardized outputs (lorem ipsum, pi digits, tongue twisters, regex patterns) to measure library performance.

### Tech Stack

- **Python**: 3.11+ (target: 3.12 in CI)
- **Package Manager**: `uv` (modern, fast alternative to pip/poetry)
- **Core Libraries**: guidance (≥0.3.0), outlines (≥1.2.7), openai (≥2.4.0), pydantic (≥2.12.2)
- **Data/Analysis**: polars (≥1.32.2), pandera (≥0.25.0), plotly (≥6.3.1), numpy (≥2.3.4)
- **CLI**: typer (≥0.16.0), rich-argparse (≥1.7.1), structlog (≥25.4.0)
- **Quality Tools**: ruff (≥0.12.4), mypy (≥1.18.2), pytest (≥8.4.0), pre-commit (≥4.3.0)

---

## 2) Build and Validation Information

### Installation & Setup

```bash
# Install uv if not present (auto-installed by make targets)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Quick install
make install              # Production dependencies only

# Development install (recommended)
make develop              # Install dev deps + git hooks + type stubs
make develop WITH_HOOKS=false  # Skip git hooks installation

# Development shortcuts
uv sync                   # Install dependencies
uv sync --only-dev        # Install dev dependencies only
uv sync --only-group test # Install test dependencies only
```

### Quality Checks

```bash
# Pre-commit checks (gitleaks, bandit, ruff, mypy, shellcheck, codespell)
make run-pre-commit

# Formatting and linting
make format               # Lint with ruff + format (safe fixes only)
make format-unsafe        # Lint with --unsafe-fixes + format
make format-all           # Run pre-commit + unsafe formatting

# Type checking (strict mode)
uv run mypy .             # Check src/gvo/ (excludes notebooks, tests)

# Testing
make test                 # Run pytest with coverage
make check                # Alias for make test
make check PARALLEL=true  # Run tests in parallel with pytest-xdist
uv run pytest -v          # Verbose test output
uv run pytest -n auto     # Parallel test execution

# Nox automation
uv run nox -s precommit   # Run pre-commit checks in isolated env
uv run nox -s test        # Run pytest in isolated env with parallel execution

# Clean up
make clean                # Remove build artifacts, caches, __pycache__
make clean-reinstall-dev  # Clean + uninstall + reinstall for dev
```

### CI Pipeline

- **Trigger**: PRs to `main` branch
- **Runner**: Ubuntu latest with Python 3.12
- **Checks**: Pre-commit hooks (security, linting, type checking) + pytest with coverage
- **Caching**: `.venv` and pre-commit hooks cached for faster runs
- **Cache Busting**: `make bust-ci-cache` to force fresh CI builds

---

## 3) Project Layout and Architecture

### Directory Structure

```text
gvo/
├── src/gvo/                          # Main package source
│   ├── __init__.py                  # Package initialization
│   ├── core.py                      # Core module (extensible)
│   ├── bin/
│   │   └── example_script.py         # CLI entry point (typer-based)
│   └── py.typed                      # PEP 561 type hint marker
│
├── docs/tutorials/                   # Library-specific tutorials
│   ├── guidance/
│   │   └── tool_calling.ipynb        # Tool calling with Guidance
│   └── outlines/
│       └── react_agent.md            # ReAct agent with Outlines
│
├── notebooks/                        # Cross-library implementations (working area)
│   ├── react_agent-guidance.ipynb    # ReAct agent in Guidance
│   └── tool_calling-outlines.ipynb   # Tool calling in Outlines
│
├── tests/                            # Test suite (pytest + pytest-xdist)
│   └── .gitkeep                      # Placeholder for future tests
│
├── data/                             # Data directory (datasets, benchmarks)
│   └── .gitignore                    # Reserved for future use
│
├── .github/
│   ├── workflows/                    # CI/CD automation
│   │   ├── CI.yml                    # Main CI pipeline
│   │   └── lint-github-actions.yml
│   └── copilot-instructions.md       # This file
│
├── .githooks/                        # Custom git hooks (managed via Makefile)
├── .gitconfigs/                      # Git configurations (aliases, hooks)
├── pyproject.toml                    # Project metadata, dependencies, tool configs
├── noxfile.py                        # Test automation (precommit, test sessions)
├── .pre-commit-config.yaml           # Pre-commit hook definitions
├── .ruff.toml                        # Ruff linter/formatter configuration
├── Makefile                          # Development workflow automation
└── .readthedocs.yaml                 # Read the Docs build config
```

### Key Files & Their Purposes

File                            | Purpose
------------------------------- | ------------------------------------------------------------------------------------------
`pyproject.toml`                | PEP 621 project metadata, dependencies, tool configs (mypy, pytest, uv)
`noxfile.py`                    | Session-based test automation (isolated environments)
`.pre-commit-config.yaml`       | Security scanning (gitleaks, bandit), linting (ruff), type checking (mypy), spell checking
`Makefile`                      | Development workflows (install, test, lint, clean, git hooks)
`.ruff.toml`                    | Ruff config: `select = ["ALL"]`, Google-style docstrings, line-length=88, target=py312
`src/gvo/bin/example_script.py` | CLI template using typer for future command-line tools
`src/gvo/py.typed`              | PEP 561 marker indicating type hints are available

### Architecture Principles

1. **Type Safety**: Strict mypy checking across all source files (excluding notebooks/tests)
2. **Validation**: Pydantic models for structured data, pandera for DataFrame validation
3. **Separation of Concerns**:
   - `docs/tutorials/`: Original library tutorials (read-only references)
   - `notebooks/`: Working notebooks for cross-library implementations
   - `src/gvo/`: Production-ready package code (type-checked, tested)
4. **Testing Philosophy**: Pytest with coverage reporting, parallel execution support, strict markers

---

## 4) Conventional Commits and Contribution Workflow

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

#### Common Types

- `feat`: New feature or capability
- `fix`: Bug fix
- `docs`: Documentation changes (README, tutorials, docstrings)
- `refactor`: Code restructuring without behavior changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system changes (Makefile, pyproject.toml, noxfile)
- `ci`: CI/CD pipeline changes (.github/workflows)
- `chore`: Maintenance tasks (dependencies, git hooks, tooling)
- `style`: Code style/formatting (usually auto-committed by pre-commit)

#### Useful Scopes for This Repo

- `guidance`: Changes specific to Guidance implementations
- `outlines`: Changes specific to Outlines implementations
- `tutorials`: Tutorial content or cross-library implementations
- `notebooks`: Jupyter notebook updates
- `cli`: Command-line interface (src/gvo/bin/)
- `core`: Core module functionality (src/gvo/core.py)
- `validation`: Data validation (pydantic, pandera)
- `benchmarks`: Performance evaluation code
- `deps`: Dependency updates
- `hooks`: Git hooks or pre-commit configuration
- `config`: Configuration files (ruff, mypy, pytest)

#### Examples

```bash
# New feature
feat(guidance): implement token healing for regex constraints

# Bug fix
fix(outlines): correct type hints for BaseModel generators

# Documentation
docs(tutorials): add performance comparison section to README

# Refactor
refactor(core): extract validation logic into separate module

# Test
test(outlines): add integration tests for schema-first API

# Build
build(deps): bump guidance from 0.3.0 to 0.3.1

# CI
ci: add caching for pytest artifacts in GitHub Actions

# Chore
chore(hooks): update pre-commit hook versions
```

### Pre-Commit/PR Checklist

1. **Run Quality Checks**: `make run-pre-commit` or `make format-all`
2. **Type Check**: `uv run mypy .` (should pass with strict mode)
3. **Test**: `make check` or `make check PARALLEL=true`
4. **Update CHANGELOG**: Use conventional commits (automated via `git-cliff` if configured)
5. **Review Diff**: Ensure no unintended changes, secrets, or `.env` files
6. **Branch Naming**: Use descriptive names (e.g., `feat/tool-calling-outlines`, `fix/guidance-token-healing`)

### Git Hooks

```bash
# Enable all hooks (pre-commit + commit-msg)
make enable-git-hooks

# Enable only pre-commit hooks
make enable-pre-commit-only

# Enable only commit hooks (conventional commits)
make enable-commit-hooks-only

# Disable all hooks
make disable-git-hooks
```

Pre-commit hooks enforce:

- **Security**: gitleaks (secrets), bandit (Python security)
- **Quality**: ruff (lint + format), mypy (strict type checking)
- **Standards**: shellcheck (shell scripts), codespell (spelling)
- **Consistency**: trailing whitespace, EOF newlines, merge conflict markers

### Recommended VSCode Extensions

Install these for optimal development experience:

- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
- [GitHub Actions](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-github-actions)
- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
- [MyPy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [ShellCheck](https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck)
- [shfmt](https://marketplace.visualstudio.com/items?itemName=mkhl.shfmt)
- [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)

---

## 5) Code Style and Quality Standards

### Ruff Configuration

- **Select**: ALL rules enabled (comprehensive linting)
- **Ignore**:
  - `COM812`: missing-trailing-comma (conflicts with formatter)
  - `ERA001`: commented-out-code (allowed for tutorial/research code)
  - `PLR2004`: magic-value-comparison (common in notebooks)
  - `TD002`, `TD003`: TODO author/link requirements
- **Line Length**: 88 characters (Black-compatible)
- **Docstrings**: Google-style convention
- **Per-File Ignores**:
  - `__init__.py`: Unused imports, star imports allowed
  - `noxfile.py`: Subprocess without shell allowed
  - `tests/*.py`: Asserts allowed
  - `*/bin/*.py`: Print statements allowed (CLI tools)
  - `*.ipynb`: Unused imports, asserts, prints allowed

### MyPy Configuration

- **Strict Mode**: Enabled (`strict = true`)
- **Plugins**: pydantic.mypy for Pydantic model validation
- **Excludes**: notebooks/, tests/, \*.ipynb (runtime-checked by pytest)
- **Error Codes**: `ignore-without-code`, `redundant-expr`, `truthy-bool`
- **Settings**: `warn_return_any`, `warn_unreachable`, `show_error_code_links`

### Pytest Configuration

- **Markers**:
  - `no_ci`: Tests skipped in CI (use `-m "not no_ci"`)
- **Coverage**: Reports missing lines (`--cov=gvo --cov-report=term-missing`)
- **Parallel Execution**: `pytest -n auto` (via pytest-xdist)
- **Strict**: `xfail_strict = true`, `--strict-markers`, `--strict-config`
- **Warnings**: Errors on warnings (except DeprecationWarning)

### General Code Guidelines

1. **Type Hints**: Required for all public functions/methods in `src/gvo/`
2. **Docstrings**: Google-style for public APIs (encouraged for notebooks)
3. **Imports**: Absolute imports preferred, organize with ruff's isort rules
4. **Error Handling**: Use Pydantic validation for data, explicit exceptions for logic errors
5. **Logging**: Use structlog for structured logging (not print statements in src/)
6. **Variable Naming**: `snake_case` for functions/variables, `PascalCase` for classes
7. **Notebooks**: Allowed to be more exploratory, but aim for clarity and reproducibility

---

## 6) Testing Approach

### Current State

- Tests directory exists but is minimal (`.gitkeep` placeholder)
- CI runs pytest with coverage reporting
- Parallel execution supported via pytest-xdist

### Testing Priorities (Future Development)

1. **Unit Tests**: Core functionality in `src/gvo/core.py`
2. **Integration Tests**: Guidance and Outlines API interactions
3. **Benchmark Tests**: Performance comparison tests (mark with `@pytest.mark.no_ci`)
4. **Notebook Tests**: Optional execution tests for tutorial notebooks (using `nbconvert` or `testbook`)

### Writing Tests

```python
# tests/test_example.py
import pytest
from gvo.core import example_function

def test_example_function():
    """Test that example_function returns expected output."""
    result = example_function(input_data)
    assert result == expected_output

@pytest.mark.no_ci
def test_expensive_benchmark():
    """Expensive test skipped in CI."""
    # Long-running benchmark test
    pass
```

Run tests:

```bash
make check                 # Run all tests except no_ci
make check PARALLEL=true   # Parallel execution
pytest -v -m "not no_ci"   # Explicit marker exclusion
pytest tests/test_example.py::test_example_function  # Run specific test
```

---

## 7) Working with Guidance vs. Outlines

### When to Use Each Library

| Criterion             | Guidance                                        | Outlines                                      |
| --------------------- | ----------------------------------------------- | --------------------------------------------- |
| **Programming Model** | Imperative DSL (context managers, control flow) | Declarative type hints (schema-first)         |
| **Best For**          | Custom generation loops, fine-grained control   | Production pipelines, validated JSON payloads |
| **Constraint System** | Regex/CFG grammars, token healing               | Python types (Literal, BaseModel, Regex)      |
| **Backend Support**   | Transformers, llama.cpp, OpenAI                 | OpenAI, vLLM, Ollama, Transformers, Gemini    |
| **Integration Style** | Programmatic orchestration                      | Minimal glue code                             |
| **Learning Curve**    | Steeper (requires understanding DSL patterns)   | Gentler (familiar Python type hints)          |

### Implementation Patterns

#### Guidance Pattern

```python
import guidance

lm = guidance.llms.OpenAI("gpt-4")

# Imperative control flow with context managers
with guidance.system():
    lm += "You are a helpful assistant."

with guidance.user():
    lm += "What is the capital of France?"

with guidance.assistant():
    lm += guidance.gen("answer", max_tokens=50)
```

#### Outlines Pattern

```python
from outlines import models, generate
from pydantic import BaseModel

# Schema-first with type hints
class Answer(BaseModel):
    capital: str
    country: str

model = models.openai("gpt-4")
generator = generate.json(model, Answer)
result = generator("What is the capital of France?")
```

### Cross-Library Implementation Guidelines

1. **Understand Paradigm Differences**: Guidance uses imperative control flow; Outlines uses declarative types
2. **Preserve Intent**: Focus on the tutorial's goal, not line-by-line translation
3. **Document Trade-offs**: Note where one library excels or struggles
4. **Benchmark Fairly**: Use equivalent model backends and temperature settings
5. **Include Working Examples**: Ensure notebooks run end-to-end with minimal setup

---

## 8) Package Management with `uv`

### Why `uv`?

- **Fast**: 10-100x faster than pip
- **Deterministic**: Lock file ensures reproducible installs
- **Modern**: PEP 621 native, workspace support, Python version management

### Common `uv` Commands

```bash
# Install dependencies
uv sync                        # Install all dependencies
uv sync --only-dev             # Install dev dependencies only
uv sync --only-group test      # Install test dependencies only
uv sync --no-editable          # Install without editable mode

# Add/remove dependencies
uv add "guidance>=0.3.1"         # Add new dependency
uv add --dev pytest-benchmark  # Add dev dependency
uv remove unused-package       # Remove dependency

# Run commands in uv environment
uv run python script.py        # Run Python script
uv run pytest                  # Run pytest
uv run mypy .                  # Run mypy

# Python version management
uv python install 3.12         # Install Python 3.12
uv python list                 # List available Python versions

# Publishing (future)
uv build                       # Build package (wheel + sdist)
uv publish --index testpypi    # Publish to TestPyPI
uv publish                     # Publish to PyPI
```

---

## 9) Development Workflow Examples

### Adding a New Feature

```bash
# 1. Create feature branch
git checkout -b feat/new-evaluation-metric

# 2. Install development environment
make develop

# 3. Implement feature
# Edit src/gvo/core.py, add tests, update docstrings

# 4. Run quality checks
make format-all
make check

# 5. Commit with conventional commit message
git add .
git commit -m "feat(benchmarks): add embedding similarity metric

Implements cosine similarity comparison for generated outputs
using sentence-transformers. Useful for semantic correctness
evaluation.

Refs: #42"

# 6. Push and create PR
git push -u origin feat/new-evaluation-metric
```

### Debugging CI Failures

```bash
# Run exact CI checks locally
uv run nox -s precommit        # Pre-commit checks
uv run nox -s test             # Pytest in isolated env

# If pre-commit fails, run specific hooks
uv run pre-commit run mypy --all-files
uv run pre-commit run ruff --all-files

# Bust CI cache if stale
make bust-ci-cache
git push
```

### Updating Dependencies

```bash
# Update single dependency
uv add "guidance>=0.3.2"

# Update all dependencies (major versions)
uv lock --upgrade

# Update all dependencies (minor/patch only)
uv lock --upgrade-package guidance

# Verify tests still pass
make check PARALLEL=true
```

---

## 10) Jupyter Notebook Guidelines

### Notebook Organization

- **Tutorials** (`docs/tutorials/`): Official library tutorials (read-only, large outputs)
- **Notebooks** (`notebooks/`): Working implementations (experimental, cross-library)

### Best Practices

1. **Clear Markdown Cells**: Explain what each section does and why
2. **Reproducibility**: Include setup cells (imports, API keys, model selection)
3. **Output Management**: Keep outputs for reference but consider using `nbstripout` for version control
4. **Error Handling**: Gracefully handle API failures, rate limits
5. **Dependencies**: Document any additional packages needed beyond `pyproject.toml`

### Running Notebooks

```bash
# Install Jupyter kernel
uv run python -m ipykernel install --user --name=gvo

# Launch Jupyter
uv run jupyter notebook

# Or use JupyterLab
uv run jupyter lab

# Convert notebook to script
uv run jupyter nbconvert --to script notebook.ipynb
```

---

## 11) Documentation Standards

### README Updates

Update `README.md` when:

- Adding new features or benchmark results
- Changing project scope or goals
- Adding new tutorials or cross-library implementations

### Docstring Format (Google Style)

```python
def compare_libraries(task: str, metrics: list[str]) -> dict[str, float]:
    """Compare Guidance and Outlines on a specific task.

    Args:
        task: The evaluation task name (e.g., "tool_calling", "react_agent").
        metrics: List of metrics to compute (e.g., ["latency", "correctness"]).

    Returns:
        A dictionary mapping metric names to computed values.

    Raises:
        ValueError: If task or metrics are invalid.

    Examples:
        >>> compare_libraries("tool_calling", ["latency"])
        {'latency': 0.245}
    """
    pass
```

### Inline Comments

- Explain **why**, not **what** (code should be self-documenting)
- Use `# TODO:` for future improvements
- Use `# FIXME:` for known issues
- Use `# NOTE:` for important context

---

## 12) Security and Secrets Management

### Pre-Commit Security Checks

- **gitleaks**: Scans for secrets in commits
- **bandit**: Identifies Python security issues

### API Key Management

```bash
# NEVER commit API keys to version control
# Use environment variables or .env files (ensure .env is in .gitignore)

# Example .env (NOT committed)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Load in code
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 13) Troubleshooting Common Issues

### `uv` Not Found

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use make target
make check-install-uv
```

### Pre-Commit Hooks Failing

```bash
# Reinstall hooks
make enable-pre-commit-only

# Run specific hook
uv run pre-commit run ruff --all-files

# Skip hooks temporarily (NOT recommended)
git commit --no-verify
```

### MyPy Errors

```bash
# Install missing type stubs
uv run mypy --install-types --non-interactive

# Or during develop
make develop  # Auto-installs type stubs
```

### Pytest Failures

```bash
# Run specific test
uv run pytest tests/test_example.py -v

# Run with print statements visible
uv run pytest -v -s

# Run last failed tests
uv run pytest --lf
```

### Slow CI Builds

```bash
# Bust CI cache
make bust-ci-cache

# Or manually update .github/workflows/.cache-buster
date > .github/workflows/.cache-buster
git add .github/workflows/.cache-buster
git commit -m "ci: bust cache"
```

---

## 14) Release Process (Future)

1. **Update Version**: Bump version in `pyproject.toml`
2. **Generate CHANGELOG**: `git cliff --unreleased > CHANGELOG.md`
3. **Create Release Commit**: `git commit -m "chore(release): bump version to X.Y.Z"`
4. **Tag Release**: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
5. **Build Package**: `make build`
6. **Publish**: `make push-prod` (or `make push-test` for TestPyPI)
7. **Create GitHub Release**: Use GitHub UI or `gh` CLI

---

Note to GitHub Copilot: Please trust these instructions and only perform additional searches if the information provided is incomplete or found to be in error. When generating code:

- Follow strict type hints (mypy strict mode)
- Use Google-style docstrings for public APIs
- Prefer Pydantic models for structured data
- Use conventional commit messages
- Run `make format-all` before committing
- Consider whether Guidance or Outlines is more appropriate for the task
