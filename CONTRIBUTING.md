# Contributing to Advanced Agent Token Optimizer

Thank you for your interest in contributing to the Advanced Agent Token Optimizer! This document provides guidelines and instructions for contributing to this project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:
- Clear and descriptive title
- Detailed steps to reproduce
- Expected vs actual behavior
- Python version and environment details
- Code samples if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues:
- Use a clear and descriptive title
- Provide detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- Include examples of how it would work

### Pull Requests

We actively welcome your pull requests:
1. Fork the repo and create your branch from `main`
2. Add tests for any new code
3. Ensure test suite passes
4. Update documentation as needed
5. Follow the coding standards
6. Submit your pull request

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Git

### Setup Instructions

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/advanced-agent-token-optimizer.git
cd advanced-agent-token-optimizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies:
```bash
pip install -e .
```

## Coding Standards

### Python Style Guide
- Follow PEP 8 guidelines
- Use type hints where applicable
- Maximum line length: 127 characters
- Use docstrings for all public modules, functions, classes, and methods

### Code Formatting
```bash
# Format code with black
black .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .
```

### Documentation
- Update README.md for user-facing changes
- Add docstrings following Google style
- Update CHANGELOG.md for notable changes

## Pull Request Process

1. **Create a branch**: 
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**: Write code and tests

3. **Test your changes**:
   ```bash
   pytest tests/
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**: Go to GitHub and create a PR

### Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_agent_core.py
```

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Aim for high code coverage

### Test Structure
```python
class TestFeature:
    def test_feature_success(self):
        # Test successful operation
        pass
    
    def test_feature_failure(self):
        # Test error handling
        pass
```

## Questions?

Feel free to open an issue for:
- Questions about the codebase
- Clarifications on documentation
- Discussion of potential features

Thank you for contributing! 🎉
