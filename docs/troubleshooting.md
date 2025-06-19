# Troubleshooting Guide

## Common Issues and Solutions

### Authentication Issues

#### Problem: "Not authenticated" error when accessing chat
**Symptoms:**
- Redirected to login page repeatedly
- 401 Unauthorized errors

**Solutions:**
1. Check session configuration:
   ```python
   # Verify SESSION_SECRET_KEY is set
   echo $SESSION_SECRET_KEY
   ```

2. Clear browser cookies and try again

3. Check application logs for session errors:
   ```bash
   tail -f app.log | grep -i session
   ```

#### Problem: Invalid credentials error with correct username/password
**Symptoms:**
- Login form shows "Invalid credentials"
- Correct credentials don't work

**Solutions:**
1. Verify user database configuration:
   ```python
   # Check USERS dictionary in main.py
   USERS = {
       "admin": "secret",
       "user": "password"
   }
   ```

2. Check for case sensitivity in username

3. Review authentication logs:
   ```bash
   grep "Failed login attempt" app.log
   ```

### AWS Bedrock Issues

#### Problem: "AWS credentials not found" error
**Symptoms:**
- Application fails to start
- ValueError about missing credentials

**Solutions:**
1. Set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your-key
   export AWS_SECRET_ACCESS_KEY=your-secret
   ```

2. Check .env file configuration:
   ```bash
   cat .env | grep AWS
   ```

3. Verify AWS credentials are valid:
   ```bash
   aws sts get-caller-identity
   ```

#### Problem: Bedrock API errors in chat responses
**Symptoms:**
- Chat responses show "Sorry, I encountered an error"
- Bedrock API errors in logs

**Solutions:**
1. Verify Bedrock model ARN:
   ```bash
   aws bedrock list-foundation-models --region us-east-2
   ```

2. Check IAM permissions:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "bedrock:InvokeModel",
                   "bedrock:InvokeModelWithResponseStream"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

3. Test Bedrock connectivity:
   ```python
   import boto3
   client = boto3.client('bedrock-runtime', region_name='us-east-2')
   response = client.list_foundation_models()
   print(response)
   ```

### Application Startup Issues

#### Problem: "ModuleNotFoundError" when starting application
**Symptoms:**
- Import errors for FastAPI or other dependencies
- Application won't start

**Solutions:**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Check Python version:
   ```bash
   python --version  # Should be 3.11+
   ```

3. Verify virtual environment:
   ```bash
   which python
   pip list
   ```

#### Problem: "Address already in use" error
**Symptoms:**
- Port 8000 is already occupied
- Cannot bind to address

**Solutions:**
1. Find process using port:
   ```bash
   # Linux/Mac
   lsof -i :8000
   
   # Windows
   netstat -ano | findstr :8000
   ```

2. Kill existing process or use different port:
   ```bash
   uvicorn app.main:app --port 8001
   ```

### Template and Static File Issues

#### Problem: Template not found errors
**Symptoms:**
- TemplateNotFound exceptions
- 500 Internal Server Error

**Solutions:**
1. Verify template directory structure:
   ```
   app/
   ├── main.py
   └── templates/
       ├── index.html
       └── login.html
   ```

2. Check template path configuration:
   ```python
   templates = Jinja2Templates(directory="app/templates")
   ```

3. Ensure templates exist and are readable:
   ```bash
   ls -la app/templates/
   ```

### Performance Issues

#### Problem: Slow response times
**Symptoms:**
- Long delays in chat responses
- Timeout errors

**Solutions:**
1. Check Bedrock API latency:
   ```bash
   grep "Bedrock API" app.log | tail -10
   ```

2. Monitor system resources:
   ```bash
   top
   htop
   ```

3. Consider async implementation:
   ```python
   # Use aioboto3 for async AWS calls
   import aioboto3
   ```

#### Problem: High memory usage
**Symptoms:**
- Application consuming excessive RAM
- Out of memory errors

**Solutions:**
1. Monitor session storage:
   ```python
   # Implement session cleanup
   @app.middleware("http")
   async def cleanup_sessions(request, call_next):
       # Add session cleanup logic
       pass
   ```

2. Limit conversation history:
   ```python
   # Keep only last N messages
   conversation = conversation[-10:]
   ```

### Database and Session Issues

#### Problem: Session data lost between requests
**Symptoms:**
- Users logged out unexpectedly
- Conversation history disappears

**Solutions:**
1. Check session middleware configuration:
   ```python
   app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)
   ```

2. Verify session secret key consistency:
   ```bash
   echo $SESSION_SECRET_KEY
   ```

3. Consider external session storage for production:
   ```python
   # Use Redis for session storage
   import redis
   ```

### Logging and Debugging

#### Problem: No logs appearing
**Symptoms:**
- Empty app.log file
- No console output

**Solutions:**
1. Check logging configuration:
   ```python
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('app.log'),
           logging.StreamHandler()
       ]
   )
   ```

2. Verify file permissions:
   ```bash
   ls -la app.log
   touch app.log  # Create if doesn't exist
   ```

3. Check log level settings:
   ```python
   logger.setLevel(logging.DEBUG)
   ```

## Diagnostic Commands

### Health Check Script
```python
#!/usr/bin/env python3
import requests
import boto3
import os

def check_application():
    try:
        response = requests.get('http://localhost:8000/login')
        print(f"✅ Application responding: {response.status_code}")
    except Exception as e:
        print(f"❌ Application not responding: {e}")

def check_aws_credentials():
    try:
        client = boto3.client('sts')
        response = client.get_caller_identity()
        print(f"✅ AWS credentials valid: {response['Arn']}")
    except Exception as e:
        print(f"❌ AWS credentials invalid: {e}")

def check_bedrock():
    try:
        client = boto3.client('bedrock-runtime', region_name='us-east-2')
        # Test with a simple call
        print("✅ Bedrock client initialized")
    except Exception as e:
        print(f"❌ Bedrock client error: {e}")

if __name__ == "__main__":
    check_application()
    check_aws_credentials()
    check_bedrock()
```

### Log Analysis
```bash
# Check for errors
grep -i error app.log | tail -20

# Check authentication attempts
grep -i "login" app.log | tail -10

# Check Bedrock API calls
grep -i "bedrock" app.log | tail -10

# Monitor real-time logs
tail -f app.log
```

## Getting Help

### Debug Mode
Enable debug mode for detailed error information:
```python
# In main.py
app = FastAPI(debug=True)
```

### Verbose Logging
Increase logging verbosity:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Support Checklist
When reporting issues, include:
- [ ] Application logs (app.log)
- [ ] Environment configuration (without secrets)
- [ ] Python version and dependencies
- [ ] Operating system information
- [ ] Steps to reproduce the issue
- [ ] Expected vs actual behavior