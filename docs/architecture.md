# Architecture Documentation

## System Overview

The AI Enterprise Chatbot is built using a modern web architecture with clear separation of concerns.

## Components

### 1. Web Framework (FastAPI)
- **Purpose**: HTTP request handling, routing, and API documentation
- **Features**: Automatic OpenAPI generation, dependency injection, async support
- **Location**: `app/main.py`

### 2. Authentication System
- **Type**: Session-based authentication
- **Storage**: Server-side sessions with secure cookies
- **Security**: CSRF protection, secure session keys

### 3. Template Engine (Jinja2)
- **Purpose**: Server-side HTML rendering
- **Templates**: Login page, chat interface
- **Location**: `app/templates/`

### 4. AI Integration (AWS Bedrock)
- **Service**: AWS Bedrock Runtime API
- **Model**: Configurable via environment variables
- **Error Handling**: Graceful degradation on API failures

### 5. Session Management
- **Storage**: In-memory session store
- **Data**: User authentication, conversation history
- **Security**: Encrypted session cookies

## Data Flow

```
User Request → FastAPI → Authentication Check → Template Rendering → Response
     ↓
Chat Message → Bedrock API → Response Processing → Session Update → Redirect
```

### Request Flow Details

1. **Authentication Flow**
   ```
   GET /login → Login Form
   POST /login → Credential Validation → Session Creation → Redirect
   ```

2. **Chat Flow**
   ```
   GET / → Session Check → Conversation Retrieval → Template Render
   POST /chat → Message Processing → Bedrock API → Session Update → Redirect
   ```

## Security Architecture

### Authentication Layer
- Session-based authentication
- Secure cookie configuration
- Automatic session expiration

### Input Validation
- Form data validation via FastAPI
- HTML escaping for XSS prevention
- Request size limitations

### API Security
- AWS credential management
- Error message sanitization
- Request logging and monitoring

## Database Design

### Current Implementation (Demo)
```python
# In-memory user storage
USERS = {
    "admin": "secret",
    "user": "password"
}

# Session-based conversation storage
session["conversation"] = [
    {"role": "user", "text": "Hello"},
    {"role": "assistant", "text": "Hi there!"}
]
```

### Production Recommendations
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(255),
    messages JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Configuration Management

### Environment Variables
- AWS credentials and configuration
- Application secrets
- Feature flags and settings

### Configuration Hierarchy
1. Environment variables (highest priority)
2. .env file
3. Default values (lowest priority)

## Error Handling

### Application Errors
- HTTP exception handling
- Graceful API failure responses
- User-friendly error messages

### Logging Strategy
- Structured logging with timestamps
- Multiple output handlers (file + console)
- Different log levels for different components

## Performance Considerations

### Current Limitations
- Synchronous Bedrock API calls
- In-memory session storage
- Single-threaded conversation processing

### Optimization Opportunities
- Async Bedrock client (aioboto3)
- Redis for session storage
- Connection pooling
- Response caching

## Scalability

### Horizontal Scaling
- Stateless application design
- External session storage required
- Load balancer configuration

### Vertical Scaling
- Memory usage optimization
- CPU-bound operation identification
- Database query optimization

## Monitoring and Observability

### Current Logging
- Authentication events
- API calls and responses
- Error conditions
- Performance metrics

### Recommended Additions
- Application metrics (Prometheus)
- Distributed tracing
- Health check endpoints
- Performance monitoring