# Contributing to BrowserJQuery

Thank you for your interest in contributing to BrowserJQuery! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/browserjquery.git
cd browserjquery
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -r requirements/dev.txt
```

5. Install the package in development mode:
```bash
pip install -e .
```

## Code Style

We follow PEP 8 style guidelines. The project uses several tools to maintain code quality:

- flake8 for linting
- black for code formatting
- isort for import sorting
- mypy for type checking

Run the quality checks:
```bash
make lint
make format
make type-check
```

## Testing

We use pytest for testing. Run the tests with:
```bash
pytest
```

For test coverage:
```bash
pytest --cov=browserjquery
```

## Pull Request Process

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of changes"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request from your fork to the main repository

## Commit Message Guidelines

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add support for custom jQuery selectors

- Implement custom selector parser
- Add tests for new functionality
- Update documentation

Fixes #123
```

## Documentation

When adding new features or changing existing ones:

1. Update docstrings in the code
2. Update the API documentation in `docs/source/browserjquery.md`
3. Add examples in `docs/source/examples.md` if applicable
4. Update the README.md if necessary

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. The CI/CD pipeline will automatically publish to PyPI

## Getting Help

- Open an issue for bugs or feature requests
- Join our community chat (if available)
- Check existing issues and pull requests

## Code of Conduct

Please be respectful and considerate of others when contributing. We aim to foster an inclusive and welcoming community. 