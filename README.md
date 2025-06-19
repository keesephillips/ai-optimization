# AI Enterprise Chatbot

A web-based chatbot application built with FastAPI that integrates with AWS Bedrock for AI-powered conversations.

## Features

- Clean, responsive web interface
- User authentication and session management
- Session-based conversation history
- AWS Bedrock integration for AI responses
- Secure environment variable configuration
- XSS protection with HTML escaping
- Comprehensive logging for monitoring and debugging

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-optimization
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the project root:
```env
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-2
BEDROCK_ARN=arn:aws:bedrock:region:account:prompt/prompt-id
SESSION_SECRET_KEY=your_session_secret_key
PROMPT_VAR_NAME=user_input
```

## Usage

1. Start the application:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to `http://localhost:8000`

3. Login with demo credentials:
   - Username: `admin`, Password: `secret`
   - Username: `user`, Password: `password`

4. Start chatting with the AI assistant

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key ID | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | Required |
| `AWS_REGION` | AWS region for Bedrock | `us-east-2` |
| `BEDROCK_ARN` | Bedrock prompt ARN | Default ARN provided |
| `SESSION_SECRET_KEY` | Secret key for session encryption | Auto-generated |
| `PROMPT_VAR_NAME` | Variable name for prompt template | `user_input` |

## Project Structure

```
ai-optimization/
├── templates/
│   └── index.html          # Web interface template
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## API Endpoints

- `GET /login` - Login page
- `POST /login` - Handle login form submission
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
- FastAPI - Web framework
- Boto3 - AWS SDK
- Uvicorn - ASGI server
- Jinja2 - Template engine
- python-dotenv - Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.