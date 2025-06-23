import pytest
import os
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.main import app, authenticate_user, render_conversation, get_current_user
from fastapi import HTTPException, Request


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_bedrock():
    """Mock the Bedrock client to avoid actual AWS calls during testing."""
    with patch('app.main.bedrock') as mock:
        mock.converse.return_value = {
            "output": {
                "message": {
                    "content": [{"text": "This is a test response from the chatbot."}]
                }
            }
        }
        yield mock


class TestAuthentication:
    """Test authentication functionality."""
    
    def test_authenticate_user_valid_credentials(self):
        """Test authentication with valid credentials."""
        result = authenticate_user("admin", "secret")
        assert result == "admin"
        
        result = authenticate_user("user", "password")
        assert result == "user"
    
    def test_authenticate_user_invalid_credentials(self):
        """Test authentication with invalid credentials."""
        result = authenticate_user("admin", "wrong_password")
        assert result is None
        
        result = authenticate_user("nonexistent", "password")
        assert result is None
    
    def test_get_current_user_authenticated(self):
        """Test get_current_user with authenticated session."""
        mock_request = Mock(spec=Request)
        mock_request.session = {"user": "admin"}
        
        result = get_current_user(mock_request)
        assert result == "admin"
    
    def test_get_current_user_not_authenticated(self):
        """Test get_current_user without authenticated session."""
        mock_request = Mock(spec=Request)
        mock_request.session = {}
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_request)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authenticated"


class TestLoginEndpoints:
    """Test login-related endpoints."""
    
    def test_login_page_get(self, client):
        """Test GET request to login page."""
        response = client.get("/login")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_login_post_valid_credentials(self, client):
        """Test POST login with valid credentials."""
        response = client.post("/login", data={"username": "admin", "password": "secret"})
        assert response.status_code == 200  
        assert response.url.path == "/"
    
    def test_login_post_invalid_credentials(self, client):
        """Test POST login with invalid credentials."""
        response = client.post("/login", data={"username": "admin", "password": "wrong"})
        assert response.status_code == 200
        assert "Invalid credentials" in response.text
    
    def test_logout(self, client):
        """Test logout functionality."""
        client.post("/login", data={"username": "admin", "password": "secret"})
        
        response = client.get("/logout")
        assert response.status_code == 200
        assert response.url.path == "/login"


class TestChatEndpoints:
    """Test chat-related endpoints."""
    
    def test_chat_page_authenticated(self, client):
        """Test accessing chat page when authenticated."""
        client.post("/login", data={"username": "admin", "password": "secret"})
        
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_chat_page_unauthenticated(self, client):
        """Test accessing chat page when not authenticated."""
        response = client.get("/")
        assert response.status_code == 401
    
    def test_chat_message_post_authenticated(self, client, mock_bedrock):
        """Test posting a chat message when authenticated."""
        client.post("/login", data={"username": "admin", "password": "secret"})
        
        response = client.post("/chat", data={"message": "Hello, chatbot!"})
        assert response.status_code == 200
        assert response.url.path == "/"
        
        mock_bedrock.converse.assert_called_once()
    
    def test_chat_message_post_unauthenticated(self, client):
        """Test posting a chat message when not authenticated."""
        response = client.post("/chat", data={"message": "Hello, chatbot!"})
        assert response.status_code == 401
    
    def test_chat_message_empty(self, client, mock_bedrock):
        """Test posting an empty chat message."""
        client.post("/login", data={"username": "admin", "password": "secret"})
        
        response = client.post("/chat", data={"message": "   "})  
        assert response.status_code == 200
        assert response.url.path == "/"
        
        mock_bedrock.converse.assert_not_called()
    
    def test_chat_bedrock_error_handling(self, client):
        """Test chat functionality when Bedrock API fails."""
        client.post("/login", data={"username": "admin", "password": "secret"})
        
        with patch('app.main.bedrock') as mock_bedrock:
            mock_bedrock.converse.side_effect = Exception("API Error")
            
            response = client.post("/chat", data={"message": "Hello, chatbot!"})
            assert response.status_code == 200
            assert response.url.path == "/"


class TestConversationRendering:
    """Test conversation rendering functionality."""
    
    def test_render_conversation_empty(self):
        """Test rendering an empty conversation."""
        result = render_conversation([])
        assert result == ""
    
    def test_render_conversation_single_user_message(self):
        """Test rendering a conversation with one user message."""
        turns = [{"role": "user", "text": "Hello"}]
        result = render_conversation(turns)
        
        assert "You:" in result
        assert "Hello" in result
        assert 'class="user"' in result
    
    def test_render_conversation_single_assistant_message(self):
        """Test rendering a conversation with one assistant message."""
        turns = [{"role": "assistant", "text": "Hi there!"}]
        result = render_conversation(turns)
        
        assert "Chatbot:" in result
        assert "Hi there!" in result
        assert 'class="assistant"' in result
    
    def test_render_conversation_multiple_turns(self):
        """Test rendering a conversation with multiple turns."""
        turns = [
            {"role": "user", "text": "Hello"},
            {"role": "assistant", "text": "Hi there!"},
            {"role": "user", "text": "How are you?"}
        ]
        result = render_conversation(turns)
        
        assert result.count("You:") == 2
        assert result.count("Chatbot:") == 1
        assert "Hello" in result
        assert "Hi there!" in result
        assert "How are you?" in result
    
    def test_render_conversation_html_escaping(self):
        """Test that HTML in messages is properly escaped."""
        turns = [{"role": "user", "text": "<script>alert('xss')</script>"}]
        result = render_conversation(turns)
        
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
        assert "&lt;/script&gt;" in result


class TestSessionManagement:
    """Test session-based conversation management."""
    
    def test_conversation_persistence_across_requests(self, client, mock_bedrock):
        """Test that conversation history persists across requests."""
        client.post("/login", data={"username": "admin", "password": "secret"})
        
        client.post("/chat", data={"message": "First message"})
        
        client.post("/chat", data={"message": "Second message"})
        
        assert mock_bedrock.converse.call_count == 2
        
        response = client.get("/")
        assert response.status_code == 200
        assert "First message" in response.text
        assert "Second message" in response.text


class TestEnvironmentConfiguration:
    """Test environment variable configuration."""
    
    def test_default_values(self):
        """Test that default values are used when environment variables are not set."""
        from app.main import REGION, SESSION_SECRET_KEY
        
        assert REGION is not None
        assert SESSION_SECRET_KEY is not None


if __name__ == "__main__":
    pytest.main([__file__])