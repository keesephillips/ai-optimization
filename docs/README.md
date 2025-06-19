# AI Enterprise Chatbot

A secure, enterprise-ready chatbot application built with FastAPI and AWS Bedrock.

## Overview

This application provides a web-based chat interface that integrates with AWS Bedrock for AI-powered conversations. It features session-based authentication, conversation persistence, and enterprise security practices.

## Features

- 🔐 **Secure Authentication** - Session-based login system
- 💬 **AI-Powered Chat** - Integration with AWS Bedrock
- 🛡️ **XSS Protection** - HTML escaping for user inputs
- 📝 **Conversation History** - Session-based chat persistence
- 🚀 **FastAPI Backend** - Modern, fast web framework
- 📊 **Comprehensive Logging** - Application monitoring and debugging

## Architecture

```
ai-optimization/
├── app/                    # Application code
│   ├── main.py            # FastAPI application
│   └── templates/         # Jinja2 HTML templates
├── docs/                  # Documentation
├── tests/                 # Test suite
├── .env                   # Environment variables
└── requirements.txt       # Python dependencies
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials
   ```

3. **Run Application**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access Application**
   - Open http://localhost:8000
   - Login with: admin/secret or user/password

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for Bedrock | us-east-2 |
| `AWS_ACCESS_KEY_ID` | AWS access key | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Required |
| `BEDROCK_ARN` | Bedrock model ARN | Default ARN |
| `SESSION_SECRET_KEY` | Session encryption key | Generated |

### AWS Bedrock Setup

1. Enable AWS Bedrock in your AWS account
2. Create or identify your model ARN
3. Ensure your AWS credentials have Bedrock permissions

## Security

- **Authentication**: Session-based with secure cookies
- **XSS Prevention**: All user inputs are HTML-escaped
- **CSRF Protection**: Built into FastAPI forms
- **Logging**: All authentication attempts are logged
- **Environment Variables**: Sensitive data stored securely

## Development

### Project Structure
- `app/main.py` - Main application logic
- `app/templates/` - HTML templates
- `tests/` - Comprehensive test suite
- `docs/` - Documentation files

### Running Tests
```bash
cd tests
python -m pytest test_main.py -v
```

### Adding Features
1. Update `app/main.py` for backend logic
2. Modify templates for UI changes
3. Add tests in `tests/test_main.py`
4. Update documentation

## Deployment

### Production Considerations
- Use a proper database instead of in-memory user storage
- Implement proper password hashing (bcrypt)
- Set up HTTPS with SSL certificates
- Configure proper logging and monitoring
- Use environment-specific configuration

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Support

For issues and questions:
1. Check the [troubleshooting guide](troubleshooting.md)
2. Review the [testing documentation](testing.md)
3. Check application logs in `app.log`

## License

This project is for educational and enterprise use.