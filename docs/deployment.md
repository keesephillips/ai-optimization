# Deployment Guide

## Production Deployment with AWS App Runner

This application is designed for production deployment using AWS App Runner, which provides a fully managed container application service.

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- GitHub repository with the application code

## Deployment Steps

### 1. Configure Environment Variables

Set up the following environment variables in AWS App Runner:

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

### 2. App Runner Configuration

The application includes an `apprunner.yaml` file that defines the build and runtime configuration:

```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies"
      - pip install -r requirements.txt
run:
  runtime-version: 3.11
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000
  network:
    port: 8000
    env: PORT
  env:
    - name: PORT
      value: "8000"
```

### 3. Deploy to App Runner

#### Option A: AWS Console
1. Navigate to AWS App Runner in the AWS Console
2. Click "Create service"
3. Choose "Source code repository"
4. Connect your GitHub repository
5. Select the branch to deploy
6. App Runner will automatically detect the `apprunner.yaml` configuration
7. Add environment variables in the configuration step
8. Review and create the service

#### Option B: AWS CLI
```bash
# Create App Runner service
aws apprunner create-service \
  --service-name ai-chatbot \
  --source-configuration '{
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/keesephillips/ai-optimization",
      "SourceCodeVersion": {
        "Type": "BRANCH",
        "Value": "main"
      },
      "CodeConfiguration": {
        "ConfigurationSource": "REPOSITORY"
      }
    },
    "AutoDeploymentsEnabled": true
  }'
```

## Features

- **Automatic Scaling**: App Runner automatically scales based on traffic
- **Load Balancing**: Built-in load balancing and health checks
- **HTTPS**: Automatic HTTPS certificate provisioning
- **Monitoring**: Integrated with CloudWatch for logs and metrics
- **Auto-deployment**: Automatic deployments on code changes

## Monitoring

App Runner provides built-in monitoring through CloudWatch:

- **Application Logs**: Available in CloudWatch Logs
- **Metrics**: CPU, memory, and request metrics
- **Health Checks**: Automatic health monitoring

## Security

- **Environment Variables**: Securely stored and encrypted
- **VPC Support**: Optional VPC connectivity
- **IAM Integration**: Fine-grained access control
- **HTTPS**: Automatic SSL/TLS termination

## Cost Optimization

- **Pay-per-use**: Only pay for compute time used
- **Automatic Scaling**: Scales to zero when not in use
- **No Infrastructure Management**: No EC2 instances to manage