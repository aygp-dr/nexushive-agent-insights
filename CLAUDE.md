# NexusHive Agent Insights Development Guide

## Build & Test Commands
- Setup: `poetry install` (recommended) or `pip install -e .`
- Run tests: `pytest tests/` or `pytest tests/unit/` for unit tests only
- Run single test: `pytest tests/path/to/test.py::test_function_name -v`
- Run with coverage: `pytest --cov=src tests/`
- Lint Python code: `ruff check src/ tests/`
- Type checking: `mypy src/`

## Code Style Guidelines
- **Python**: PEP 8 style, type annotations, docstrings (Google style)
  - Imports: standard lib → third-party → local modules, alphabetized within groups
  - Error handling: use specific exceptions with context messages
  - Naming: snake_case for functions/variables, PascalCase for classes
  - OpenTelemetry: follow OTLP conventions for spans, metrics, and logs
- **Documentation**: Markdown for docs, Google-style docstrings for code
- **Git**: Conventional Commits
  - Format: `<type>(<scope>): <description>`
  - Example: `feat(collector): add span attribute processor`

## Project Structure
- `src/client/`: Agent instrumentation libraries
- `src/collector/`: Telemetry data collection, processing
- `src/examples/`: Usage examples and templates