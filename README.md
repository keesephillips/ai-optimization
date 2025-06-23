# AI Chatbot

A modern web-based chatbot application built with FastAPI that integrates with AWS Bedrock for AI-powered conversations.

## Features

- **Dark Mode Interface** - Modern, responsive dark theme
- **User Authentication** - Login and registration system
- **Session Management** - Persistent conversation history
- **AWS Bedrock Integration** - Bedrock AI responses
- **Security** - XSS protection with HTML escaping
- **Real-time Chat** - Instant AI responses

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/keesephillips/ai-optimization
cd ai-optimization
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the project root:
```env
AWS_ACCESS_KEY_ID=access_key_id
AWS_SECRET_ACCESS_KEY=secret_access_key
AWS_REGION=us-east-1
```

## Usage

1. Start the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to `http://localhost:8000` or AWS App Runner hosted site

3. Login with demo credentials:
   - Username: `user`, Password: `password`
   - Or register a new account

4. Start chatting with the AI assistant

## Configuration

### Environment Variables

| Variable                | Description            | Default     |
| ----------------------- | ---------------------- | ----------- |
| `AWS_ACCESS_KEY_ID`     | AWS access key ID      | Required    |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key  | Required    |
| `AWS_REGION`            | AWS region for Bedrock | `us-east-1` |

## Project Structure

```
ai-optimization/
├── app/
│   ├── templates/
│   │   ├── index.html      # Main chat interface
│   │   ├── login.html      # Login page
│   │   └── register.html   # Registration page
│   └── main.py            # FastAPI application
├── docs/                  # Documentation
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
├── .env                  # Environment configuration
└── README.md             # This file
```

## API Endpoints

- `GET /login` - Login page
- `POST /login` - Handle login form submission
- `GET /register` - Registration page
- `POST /register` - Handle registration form submission
- `GET /logout` - Logout and clear session
- `GET /` - Main chat interface (requires authentication)
- `POST /chat` - Handle chat message submission (requires authentication)

## Security Features

- HTML escaping to prevent XSS attacks
- Session-based conversation storage
- Environment variable configuration for sensitive data
- Secure session middleware

## Dependencies

Key dependencies include:
- **FastAPI** - Modern web framework
- **Boto3** - AWS SDK for Bedrock integration
- **Uvicorn** - ASGI server
- **Jinja2** - Template engine
- **python-dotenv** - Environment variable management
- **Starlette** - Session middleware

## AI Use Disclaimer
This project used Amazon Q to help create the tests and documentations

## Author 

Keese Phillips