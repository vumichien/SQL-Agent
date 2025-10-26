# Testing Documentation - Detomo SQL AI

## Test Structure

```
tests/
├── unit/                          # Unit tests (individual components)
│   ├── __init__.py
│   └── test_detomo_vanna.py      # Vanna class tests
│
├── integration/                   # Integration tests (components working together)
│   ├── __init__.py
│   ├── test_api_endpoints.py     # API endpoint tests
│   ├── test_backend_switching.py # Backend switching tests
│   └── test_app_structure.py     # Application structure tests
│
└── api/                          # API-specific tests (legacy, being phased out)
```

---

## Running Tests

### Run All Tests
```bash
# Activate virtual environment
source .venv/Scripts/activate

# Run all tests
pytest tests/ -v
```

### Run Unit Tests Only
```bash
pytest tests/unit/ -v
```

### Run Integration Tests Only
```bash
pytest tests/integration/ -v
```

### Run Specific Test File
```bash
# Unit tests
pytest tests/unit/test_detomo_vanna.py -v

# Integration tests
pytest tests/integration/test_api_endpoints.py -v
pytest tests/integration/test_backend_switching.py -v
pytest tests/integration/test_app_structure.py -v
```

### Run Specific Test
```bash
pytest tests/integration/test_api_endpoints.py::test_health_check -v
```

---

## Test Categories

### Unit Tests (`tests/unit/`)
Test individual components in isolation.

**test_detomo_vanna.py**
- Vanna initialization
- Database connection
- Training data methods
- Configuration

**Coverage**: Core functionality of Vanna classes

### Integration Tests (`tests/integration/`)
Test how components work together.

**test_api_endpoints.py**
- All 8 API endpoints
- Request/response validation
- Error handling
- JSON serialization

**test_backend_switching.py**
- Backend factory
- Claude Agent SDK backend
- Anthropic API backend
- Backend switching logic

**test_app_structure.py**
- Application initialization
- Route registration
- Error handler registration
- Configuration loading

**Coverage**: API functionality, backend switching, app structure

---

## Test Requirements

### Prerequisites
```bash
# All tests require
pytest
anthropic

# API tests require (will skip if not set)
ANTHROPIC_API_KEY=your_key_here
```

### Skip Tests Without API Key
Tests that require API key will automatically skip if not configured:
```python
@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set"
)
```

---

## Test Coverage

### Current Coverage
- **Unit tests**: 4 tests (3 passed, 1 skipped)
- **Integration tests**: 22 tests (18 passed, 4 skipped without API key)
- **Total**: 26 tests

### Coverage Goals
- Unit tests: ≥80% code coverage
- Integration tests: All critical paths covered
- API tests: All endpoints tested

---

## Writing New Tests

### Unit Test Template
```python
"""Test module description"""
import pytest
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_something():
    """Test description"""
    # Arrange
    # Act
    # Assert
    assert True
```

### Integration Test Template
```python
"""Test module description"""
import pytest
import sys
from pathlib import Path
import os

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Skip if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set"
)

@pytest.fixture
def app():
    """Create test app"""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    return app

def test_integration():
    """Test description"""
    # Test code
    pass
```

---

## Continuous Integration

### GitHub Actions (Future)
```yaml
- name: Run tests
  run: |
    pytest tests/ -v --cov=src --cov=backend --cov=api
```

### Pre-commit Hook (Future)
```bash
#!/bin/bash
pytest tests/unit/ -v
```

---

## Troubleshooting

### Issue: Tests can't find modules
**Solution**: Ensure project root is in Python path
```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### Issue: Tests skipped
**Solution**: Set `ANTHROPIC_API_KEY` in `.env`

### Issue: Database errors
**Solution**: Ensure `data/chinook.db` exists and training data loaded

### Issue: Import errors
**Solution**: Install all dependencies
```bash
uv pip install -r requirements.txt
```

---

## Test Maintenance

### Regular Tasks
- [ ] Run tests before each commit
- [ ] Update tests when adding new features
- [ ] Maintain ≥80% test coverage
- [ ] Fix failing tests immediately
- [ ] Update test documentation

### Review Schedule
- Weekly: Review test coverage
- Monthly: Review test structure
- Quarterly: Refactor and optimize tests

---

**Last Updated**: 2025-10-26
