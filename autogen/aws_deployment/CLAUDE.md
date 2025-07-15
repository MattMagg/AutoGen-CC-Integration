# AWS Deployment Configuration - Technical Reference

This directory contains AWS deployment configurations for production deployment of the Claude Code wrapper and AutoGen agents.

## DEPLOYMENT ARCHITECTURE

### Option 1: ECS + Lambda (Recommended)
- **Wrapper on ECS**: Persistent, scalable endpoint (~$50-100/month)
- **Agents on Lambda**: Pay-per-use execution (~$0.20 per 1000 requests)

### Option 2: Everything on ECS
- Single deployment for wrapper + AutoGen
- Better for long-running workflows (~$100-200/month)

### Option 3: EC2 Instance
- Full control, fixed costs (~$50-150/month)
- Good for development environments

## CONFIGURATION FILES

### ecs_deployment.yaml
CloudFormation template for ECS/Fargate deployment.

**Required Parameters:**
- `ClaudeAuthToken`: OAuth token from Claude CLI
- `DockerImage`: ECR image URI
- `VpcId`: Target VPC
- `SubnetIds`: At least 2 subnets for ALB

**Deploy Command:**
```bash
aws cloudformation create-stack \
  --stack-name claude-wrapper \
  --template-body file://ecs_deployment.yaml \
  --parameters \
    ParameterKey=ClaudeAuthToken,ParameterValue=your-token \
    ParameterKey=DockerImage,ParameterValue=your-ecr-image \
    ParameterKey=VpcId,ParameterValue=vpc-xxxx \
    ParameterKey=SubnetIds,ParameterValue="subnet-xxx,subnet-yyy" \
  --capabilities CAPABILITY_IAM
```

### lambda_autogen.py
Lambda function for serverless AutoGen execution.

**Environment Variables:**
- `CLAUDE_WRAPPER_URL`: ECS wrapper endpoint
- `CLAUDE_AUTH_SECRET`: Secrets Manager secret name

**Event Format:**
```json
{
  "action": "single_agent",
  "task": "Your task description",
  "agent_type": "assistant"
}
```

### serverless.yml
Serverless Framework configuration for Lambda deployment.

**Features:**
- Multiple endpoints (single/multi agent, async)
- API Gateway with throttling
- SQS for async processing
- DynamoDB for job tracking
- S3 for result storage

**Deploy:**
```bash
serverless deploy --stage prod --region us-east-1
```

## DEPLOYMENT PREREQUISITES

### 1. ECR Repository Setup
```bash
aws ecr create-repository --repository-name claude-wrapper
```

### 2. Docker Image Build & Push
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t claude-wrapper .
docker tag claude-wrapper:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/claude-wrapper:latest

# Push
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/claude-wrapper:latest
```

### 3. Secrets Configuration
```bash
# Store OAuth token
aws secretsmanager create-secret \
  --name /autogen/claude-auth \
  --secret-string '{"token":"your-claude-oauth-token"}'

# Store wrapper URL
aws ssm put-parameter \
  --name /autogen/claude-wrapper-url \
  --value "https://your-alb-url.us-east-1.elb.amazonaws.com" \
  --type String
```

## SECURITY REQUIREMENTS

### Network Security
- VPC with private subnets for ECS tasks
- Security groups with minimal required access
- VPC endpoints for AWS services
- Enable VPC Flow Logs

### Secrets Management
- Store all credentials in AWS Secrets Manager
- Use IAM roles, not access keys
- Rotate tokens regularly
- Enable audit logging

### API Security
- API Gateway with API keys
- Rate limiting configuration
- AWS WAF for DDoS protection
- CloudWatch monitoring

## COST BREAKDOWN

### Monthly Estimates
- **ECS/Fargate**: ~$70 (2 tasks, 1 vCPU, 2GB RAM)
- **ALB**: ~$20
- **Lambda**: ~$6 (1000 req/day, 5s avg)
- **API Gateway**: ~$3.50
- **Storage/Logs**: ~$11
- **Total**: ~$121/month

## MONITORING & DEBUGGING

### CloudWatch Integration
- ECS task logs in CloudWatch Logs
- Lambda function logs auto-created
- Custom metrics for performance tracking
- Alarms for error rates and latency

### Health Checks
- ECS: `/health` endpoint monitoring
- Lambda: CloudWatch synthetic monitoring
- API Gateway: Built-in metrics

### Troubleshooting
1. Check CloudWatch Logs for errors
2. Review CloudFormation stack events
3. Monitor ECS service events
4. Verify IAM permissions
5. Check network connectivity

## DEPLOYMENT CHECKLIST

1. **Local Testing**: Verify everything works locally
2. **AWS Setup**: Configure VPC, subnets, security groups
3. **Build & Push**: Docker image to ECR
4. **Secrets**: Store auth tokens in Secrets Manager
5. **Deploy Infrastructure**: CloudFormation stack
6. **Deploy Functions**: Serverless framework
7. **Update Config**: Point AutoGen to AWS endpoints
8. **Test**: Verify end-to-end functionality
9. **Monitor**: Set up alarms and dashboards

Remember: Test thoroughly in development before deploying to production. AWS deployments involve costs even during testing.