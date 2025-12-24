---
title: "pytest Fixture Patterns: A Practical Guide"
date: 2025-12-24 15:30:00 +0900
categories: [Development, Testing]
tags: [python, pytest, fixture, testing, best-practices]
description: "Common pytest fixture patterns for clean, maintainable, and reusable test code."
image:
  path: assets/img/posts/troubleshooting/pytest_fixture_thumbnail.png
  alt: pytest Fixture Patterns
author: seoultech
---

## Introduction

pytest fixtures are a powerful way to manage test setup and teardown. This post covers practical patterns that make tests cleaner and more maintainable.

## Basic Fixture

A fixture is a function decorated with `@pytest.fixture`:

```python
import pytest

@pytest.fixture
def sample_user() -> dict:
    """Create a sample user for testing."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }
# end def

def test_user_has_email(sample_user: dict) -> None:
    """Verify user has email field."""
    assert "email" in sample_user
# end def
```

## Scope Patterns

### Function Scope (Default)

New instance for each test:

```python
@pytest.fixture(scope="function")
def db_connection():
    """Fresh connection for each test."""
    conn = create_connection()
    yield conn
    conn.close()
# end def
```

### Module Scope

Shared across all tests in a file:

```python
@pytest.fixture(scope="module")
def api_client():
    """Shared client for the module."""
    client = APIClient()
    client.authenticate()
    yield client
    client.logout()
# end def
```

### Session Scope

Shared across entire test session:

```python
@pytest.fixture(scope="session")
def database():
    """Single database instance for all tests."""
    db = Database()
    db.migrate()
    yield db
    db.cleanup()
# end def
```

## Factory Pattern

When you need multiple instances with different configurations:

```python
@pytest.fixture
def create_user():
    """Factory fixture for creating users."""
    created_users = []
    
    def _create_user(name: str, role: str = "user") -> dict:
        user = {"name": name, "role": role, "id": len(created_users) + 1}
        created_users.append(user)
        return user
    # end def
    
    yield _create_user
    
    # Cleanup
    for user in created_users:
        # delete_user(user["id"])
        pass
    # end for
# end def

def test_multiple_users(create_user) -> None:
    """Test with multiple users."""
    admin = create_user("Admin", role="admin")
    guest = create_user("Guest", role="guest")
    
    assert admin["role"] == "admin"
    assert guest["role"] == "guest"
# end def
```

## Parameterized Fixtures

Test with multiple input values:

```python
@pytest.fixture(params=[
    {"status": 200, "expected": "success"},
    {"status": 404, "expected": "not found"},
    {"status": 500, "expected": "error"},
])
def api_response(request):
    """Fixture with multiple response scenarios."""
    return request.param
# end def

def test_response_handling(api_response) -> None:
    """Test runs 3 times with different responses."""
    status = api_response["status"]
    expected = api_response["expected"]
    # Test logic here
# end def
```

## Fixture Composition

Combine fixtures for complex setups:

```python
@pytest.fixture
def database():
    """Database connection."""
    return Database()
# end def

@pytest.fixture
def repository(database):
    """Repository that uses database fixture."""
    return UserRepository(database)
# end def

@pytest.fixture
def service(repository):
    """Service that uses repository fixture."""
    return UserService(repository)
# end def

def test_service(service) -> None:
    """Service gets repository and database automatically."""
    result = service.get_users()
    assert result is not None
# end def
```

## Autouse Fixtures

Run automatically without explicit request:

```python
@pytest.fixture(autouse=True)
def reset_environment():
    """Reset before each test (auto-applied)."""
    os.environ["TEST_MODE"] = "true"
    yield
    os.environ.pop("TEST_MODE", None)
# end def

def test_something() -> None:
    """Environment is automatically reset."""
    assert os.environ.get("TEST_MODE") == "true"
# end def
```

## conftest.py Organization

Place shared fixtures in `conftest.py`:

```
tests/
├── conftest.py          # Shared fixtures
├── unit/
│   ├── conftest.py      # Unit test specific fixtures
│   └── test_user.py
└── integration/
    ├── conftest.py      # Integration test specific fixtures
    └── test_api.py
```

Example `conftest.py`:

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def base_url() -> str:
    """API base URL for all tests."""
    return "http://localhost:8000"
# end def

@pytest.fixture
def auth_headers(base_url: str) -> dict:
    """Get authentication headers."""
    # Login and get token
    return {"Authorization": "Bearer test-token"}
# end def
```

## Cleanup Pattern

Ensure cleanup even if test fails:

```python
@pytest.fixture
def temp_file():
    """Create temporary file with guaranteed cleanup."""
    import tempfile
    import os
    
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    yield path  # Test runs here
    
    # Cleanup runs even if test fails
    if os.path.exists(path):
        os.remove(path)
    # end if
# end def
```

## Request Context

Access test information in fixtures:

```python
@pytest.fixture
def logger(request):
    """Logger with test name context."""
    import logging
    
    test_name = request.node.name
    logger = logging.getLogger(test_name)
    logger.info(f"Starting test: {test_name}")
    
    yield logger
    
    logger.info(f"Finished test: {test_name}")
# end def
```

## Best Practices

### 1. Keep Fixtures Focused

Each fixture should do one thing:

```python
#  Bad: Too much in one fixture
@pytest.fixture
def everything():
    db = Database()
    client = APIClient()
    user = create_user()
    return db, client, user
# end def

#  Good: Separate concerns
@pytest.fixture
def database():
    return Database()
# end def

@pytest.fixture
def api_client():
    return APIClient()
# end def

@pytest.fixture
def test_user():
    return create_user()
# end def
```

### 2. Use Type Hints

Make fixtures self-documenting:

```python
@pytest.fixture
def sample_data() -> list[dict[str, str]]:
    """Return list of sample records."""
    return [
        {"id": "1", "name": "Item A"},
        {"id": "2", "name": "Item B"},
    ]
# end def
```

### 3. Document with Docstrings

Explain what the fixture provides:

```python
@pytest.fixture
def authenticated_client(api_client, test_user) -> APIClient:
    """
    API client authenticated as test_user.
    
    Returns:
        APIClient configured with valid auth token.
    """
    api_client.login(test_user)
    return api_client
# end def
```

## Summary

| Pattern | Use Case |
|---------|----------|
| **Basic** | Simple setup/teardown |
| **Scope** | Control instance lifetime |
| **Factory** | Multiple instances with variations |
| **Parameterized** | Test with multiple inputs |
| **Composition** | Build complex setups from simple parts |
| **Autouse** | Apply to all tests automatically |

Master these patterns to write cleaner, more maintainable tests!
