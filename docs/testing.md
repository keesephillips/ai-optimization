# Testing Guide

This document explains how to run and understand the tests for the AI Enterprise Chatbot application.

## Test Structure

The test suite covers:

- **Authentication**: User login/registration functionality
- **HTTP Endpoints**: All API routes and responses
- **Chat Functionality**: Message processing and AI integration
- **Session Management**: Conversation persistence
- **Security**: XSS protection and input validation

## Running Tests

### Quick Start
```bash
# Navigate to tests directory
cd tests

# Install test dependencies 
pip install pytest pytest-asyncio httpx

# Run all tests
python -m pytest test_main.py -v

# Or use the test runner script
python run_tests.py
```

### Test Options
```bash
# Run specific test class
python -m pytest test_main.py::TestAuthentication -v

# Run specific test
python -m pytest test_main.py::TestAuthentication::test_authenticate_user_valid_credentials -v

# Run with coverage 
python -m pytest test_main.py --cov=main --cov-report=html
```

## Test Coverage

The test suite covers:

**Authentication System**
- Valid/invalid login credentials
- Session management
- Protected endpoint access

**HTTP Endpoints**
- Login page rendering
- Chat page access control
- Form submission handling
- Redirect responses

**Chat Functionality**
- Message processing
- Bedrock API integration (mocked)
- Error handling
- Empty message handling

**Conversation Management**
- HTML rendering with XSS protection
- Session persistence
- Multi-turn conversations

**Security Features**
- HTML escaping for XSS prevention
- Authentication requirements
- Session-based access control

## Mocking Strategy

The tests use mocking to avoid external dependencies:

- **AWS Bedrock API**: Mocked to return predictable responses
- **Sessions**: Handled by FastAPI's TestClient
- **Environment Variables**: Tested with default values

## Test Files

- `test_main.py` - Main test suite
- `pytest.ini` - Pytest configuration
- `run_tests.py` - Simple test runner script

## Adding New Tests

When adding new functionality, follow these patterns:

1. **Create a test class** for related functionality
2. **Use descriptive test names** that explain what's being tested
3. **Mock external dependencies** (AWS, databases, etc.)
4. **Test both success and failure cases**
5. **Include edge cases** (empty inputs, invalid data, etc.)

Example test structure:
```python
class TestNewFeature:
    def test_feature_success_case(self, client):
        # Test success conditions
        pass
    
    def test_feature_error_handling(self, client):
        # Test error conditions
        pass
```