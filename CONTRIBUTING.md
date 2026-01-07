# Contributing to Markerless Biomechanical Analysis

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the markerless computer vision pipeline for biomechanical analysis.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or experience level.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information
- Other conduct that could reasonably be considered inappropriate

## How Can I Contribute?

### Reporting Bugs

**Before Submitting a Bug Report**:
- Check the documentation to see if the issue is already addressed
- Search existing issues to avoid duplicates
- Collect relevant information (error messages, system specs, etc.)

**Submitting a Bug Report**:
1. Use the issue tracker
2. Provide a clear, descriptive title
3. Describe the exact steps to reproduce
4. Provide specific examples
5. Describe the observed vs. expected behavior
6. Include system information and versions

**Bug Report Template**:
```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Run command '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**System Information**
- OS: [e.g., Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- GPU: [e.g., NVIDIA RTX 3080]
- Relevant Package Versions

**Additional Context**
Any other relevant information.
```

### Suggesting Enhancements

**Before Submitting**:
- Check if the enhancement is already suggested
- Consider if it fits the project scope
- Think about how it would benefit users

**Enhancement Suggestion Template**:
```markdown
**Feature Description**
Clear description of the proposed feature.

**Motivation**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered.

**Additional Context**
Any other relevant information.
```

### Contributing Code

We welcome code contributions in the following areas:

1. **Pipeline Improvements**
   - Enhanced algorithms for existing stages
   - Performance optimizations
   - Bug fixes

2. **New Features**
   - Additional movement types (walking, jumping, etc.)
   - Real-time processing capabilities
   - Multi-person tracking
   - Integration with other tools

3. **Documentation**
   - Improved tutorials
   - Additional examples
   - Translation to other languages

4. **Testing**
   - Unit tests
   - Integration tests
   - Validation on new datasets

## Getting Started

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/thesis.git
   cd thesis
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   conda create -n biomech python=3.9
   conda activate biomech
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

4. **Verify Setup**
   ```bash
   # Run tests
   pytest tests/
   
   # Check code style
   flake8 src/
   black --check src/
   ```

### Development Dependencies

```
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.950
pre-commit>=2.17.0
sphinx>=4.5.0
```

## Development Workflow

### Branching Strategy

- `main`: Stable, production-ready code
- `develop`: Integration branch for features
- `feature/feature-name`: New features
- `bugfix/bug-name`: Bug fixes
- `docs/doc-name`: Documentation updates

### Workflow Steps

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to GitHub and create a pull request
   - Fill out the PR template
   - Link related issues

### Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(pose-estimation): add support for HALPE-136 keypoints
fix(triangulation): correct reprojection error calculation
docs(methodology): update camera calibration guide
test(grf-estimation): add unit tests for contact detection
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specifics:

**Formatting**:
- Use `black` for automatic formatting
- Line length: 100 characters
- Use 4 spaces for indentation

**Naming Conventions**:
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

**Type Hints**:
```python
def triangulate_keypoint(
    observations: List[np.ndarray],
    weights: List[float],
    projection_matrices: List[np.ndarray]
) -> np.ndarray:
    """
    Triangulate 3D point from multi-view observations.
    
    Args:
        observations: List of 2D observations from each camera
        weights: Confidence weights for each observation
        projection_matrices: Camera projection matrices
        
    Returns:
        3D point in world coordinates
    """
    # Implementation
    pass
```

**Docstrings**:
- Use Google-style docstrings
- Document all public functions and classes
- Include examples for complex functions

### Code Organization

```
src/
├── calibration/       # Camera calibration module
├── enhancement/       # Video enhancement module
├── pose_estimation/   # 2D pose estimation module
├── synchronization/   # Camera synchronization module
├── triangulation/     # 3D triangulation module
├── marker_mapping/    # Keypoint-to-marker mapping module
├── grf_estimation/    # GRF estimation module
└── utils/             # Utility functions
```

## Testing Guidelines

### Writing Tests

**Unit Tests**:
```python
import pytest
import numpy as np
from src.triangulation import weighted_triangulation

def test_weighted_triangulation_basic():
    """Test basic triangulation with perfect observations."""
    # Setup
    observations = [np.array([100, 200]), np.array([150, 200])]
    weights = [1.0, 1.0]
    projection_matrices = [P1, P2]
    
    # Execute
    point_3d = weighted_triangulation(observations, weights, projection_matrices)
    
    # Assert
    assert point_3d.shape == (3,)
    assert np.allclose(point_3d, expected_point, atol=1e-3)

def test_weighted_triangulation_with_outlier():
    """Test triangulation with one outlier observation."""
    # Test implementation
    pass
```

**Integration Tests**:
```python
def test_complete_pipeline():
    """Test complete pipeline from videos to GRF."""
    # Load test data
    videos = load_test_videos()
    calibration = load_test_calibration()
    
    # Run pipeline
    grf_estimated = run_pipeline(videos, calibration)
    
    # Compare with ground truth
    grf_ground_truth = load_ground_truth()
    rmse = compute_rmse(grf_estimated, grf_ground_truth)
    
    assert rmse < 0.20  # BW
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_triangulation.py

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_triangulation.py::test_weighted_triangulation_basic
```

## Documentation

### Code Documentation

- Document all public APIs
- Include usage examples
- Explain complex algorithms
- Add references to papers/methods

### User Documentation

- Update relevant markdown files
- Add tutorials for new features
- Include screenshots/diagrams
- Provide example code

### Building Documentation

```bash
cd docs/
make html
# Open docs/_build/html/index.html
```

## Submitting Changes

### Pull Request Process

1. **Ensure Quality**
   - All tests pass
   - Code follows style guidelines
   - Documentation is updated
   - No merge conflicts

2. **Create Pull Request**
   - Use descriptive title
   - Fill out PR template
   - Link related issues
   - Request reviewers

3. **Address Feedback**
   - Respond to review comments
   - Make requested changes
   - Update PR as needed

4. **Merge**
   - Maintainer will merge when approved
   - Delete feature branch after merge

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Related Issues
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No breaking changes (or documented)
```

## Questions?

If you have questions:
- Check the [documentation](docs/)
- Search [existing issues](https://github.com/YOUR_USERNAME/thesis/issues)
- Open a new issue with the "question" label

## Thank You!

Your contributions help make biomechanical analysis more accessible to everyone!

---

**Back to**: [Main README](README.md)

