# Claude Code OpenAI Wrapper - Development Instructions

This directory contains the OpenAI-compatible API wrapper for Claude Code. Follow these instructions when working on the wrapper implementation.

## WRAPPER OVERVIEW

This FastAPI server provides OpenAI API compatibility for Claude Code, enabling any OpenAI client to use Claude. The wrapper handles authentication, message format conversion, session management, and streaming responses.

## KEY COMPONENTS

### Core Files
- **`main.py`** - FastAPI application and endpoint definitions
- **`auth.py`** - Multi-provider authentication (CLI, API key, Bedrock, Vertex AI)
- **`claude_cli.py`** - Claude Code SDK integration layer
- **`message_adapter.py`** - OpenAI ↔ Claude message format conversion
- **`session_manager.py`** - Conversation continuity across requests
- **`models.py`** - Pydantic models for API request/response validation
- **`parameter_validator.py`** - Request parameter validation and defaults

### Test Files
- **`test_endpoints.py`** - Quick endpoint verification
- **`test_basic.py`** - Comprehensive functionality tests
- **`test_auth.py`** - Authentication system tests

## DEVELOPMENT WORKFLOW

### 1. Setup and Run
```bash
# Install dependencies
poetry install

# Run in development mode (auto-reload on changes)
poetry run uvicorn main:app --reload --port 8000

# Verify it's working
curl http://localhost:8000/health
```

### 2. Making Changes
**BEFORE any code changes:**
1. Understand the existing implementation
2. Run tests to ensure baseline functionality
3. Verify authentication is working

**DURING development:**
1. Keep the server running with --reload
2. Test changes immediately with curl or test scripts
3. Verify OpenAI compatibility is maintained

**AFTER changes:**
1. Run all tests: `poetry run pytest`
2. Run endpoint tests: `poetry run python test_endpoints.py`
3. Test with AutoGen: `cd ../autogen && python quickstart.py`
4. Format code: `poetry run black .`

## CRITICAL IMPLEMENTATION DETAILS

### Authentication Flow
```python
# Authentication priority order:
1. Check for API key in Authorization header
2. Try Claude CLI authentication (OAuth)
3. Fall back to ANTHROPIC_API_KEY
4. Try AWS Bedrock if configured
5. Try Google Vertex AI if configured
```

### Message Conversion
- **MUST** handle system messages correctly
- **MUST** preserve message order and roles
- **MUST** convert image placeholders appropriately
- **NEVER** lose message content during conversion

### Session Management
- Sessions expire after 1 hour of inactivity
- Session IDs are optional (stateless by default)
- Session history is maintained in memory
- **MUST** handle session cleanup properly

### Streaming Implementation
- Uses Server-Sent Events (SSE) format
- **MUST** handle connection drops gracefully
- **MUST** send proper OpenAI-formatted chunks
- **MUST** include usage data in final chunk

## TESTING REQUIREMENTS

### Unit Tests
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_auth.py

# Run with coverage
poetry run pytest --cov=.
```

### Integration Tests
```bash
# 1. Start the server
poetry run uvicorn main:app --port 8000

# 2. Run endpoint tests
poetry run python test_endpoints.py

# 3. Run basic functionality tests
poetry run python test_basic.py

# 4. Test with actual AutoGen
cd ../autogen && python quickstart.py
```

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test models endpoint
curl http://localhost:8000/v1/models

# Test chat completion
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## PERFORMANCE GUIDELINES

### Default Mode (Tools Disabled)
- Response time: < 500ms for simple queries
- No file system access or command execution
- Direct Claude API passthrough

### Tools Enabled Mode
- Activated by `extra_body={"enable_tools": True}`
- 5-10x slower due to tool execution
- Use only when file/command access needed

### Token Tracking
- **MUST** use actual SDK metadata for token counts
- **NEVER** estimate or calculate tokens manually
- Cost calculation: Use real token prices from SDK

## ERROR HANDLING

### Authentication Errors
- Return 401 with clear error message
- Include which auth method failed
- Suggest troubleshooting steps

### API Errors
- Return appropriate HTTP status codes
- Include Claude's error message if available
- Log full error details for debugging

### Streaming Errors
- Handle connection drops gracefully
- Clean up resources properly
- Send error in SSE format if possible

## COMMON ISSUES AND SOLUTIONS

### Issue: "Claude CLI not found"
```bash
# Verify Claude CLI is installed
which claude

# Update CLAUDE_CLI_PATH in .env if needed
echo "CLAUDE_CLI_PATH=$(which claude)" >> .env
```

### Issue: "Authentication failed"
```bash
# Test Claude CLI directly
claude --print --model claude-3-5-haiku-20241022 "test"

# Re-authenticate if needed
claude auth login
```

### Issue: "Port already in use"
```bash
# Find process using port
lsof -i:8000

# Kill the process or use different port
poetry run uvicorn main:app --port 8001
```

## IMPORTANT CONSTRAINTS

1. **OpenAI Compatibility**: Every response MUST be OpenAI-compatible
2. **No Breaking Changes**: Existing AutoGen code MUST continue working
3. **Authentication Security**: NEVER expose credentials in logs/responses
4. **Performance**: Default mode MUST remain fast (no tools)
5. **Error Messages**: MUST be helpful and actionable

## DEBUGGING TIPS

### Enable Debug Logging
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Specific Auth Methods
```bash
# Test with API key
ANTHROPIC_API_KEY=your-key poetry run uvicorn main:app

# Test with Bedrock
CLAUDE_CODE_USE_BEDROCK=true AWS_PROFILE=your-profile poetry run uvicorn main:app
```

### Monitor Requests
```bash
# Watch server logs
poetry run uvicorn main:app --log-level debug

# Monitor with curl verbose
curl -v http://localhost:8000/v1/chat/completions ...
```

## CODE STYLE

- Use type hints for all functions
- Follow PEP 8 (enforced by Black)
- Document complex logic with comments
- Keep functions focused and testable
- Use meaningful variable names

## SUPPORTED MODELS

The wrapper supports the following Claude models:
- `claude-sonnet-4-20250514` (Recommended - latest)
- `claude-opus-4-20250514`
- `claude-3-7-sonnet-20250219`
- `claude-3-5-sonnet-20241022`
- `claude-3-5-haiku-20241022` (Fastest for testing)

Model validation is performed on every request. Invalid models return appropriate error messages.

## DOCKER DEPLOYMENT

### Building the Image
```bash
# Build the Docker image
docker build -t claude-wrapper:latest .

# Verify the build
docker images | grep claude-wrapper
```

### Running the Container

**Production Mode:**
```bash
docker run -d -p 8000:8000 \
  -v ~/.claude:/root/.claude \
  --name claude-wrapper-container \
  claude-wrapper:latest
```

**Development Mode with Hot Reload:**
```bash
docker run -d -p 8000:8000 \
  -v ~/.claude:/root/.claude \
  -v $(pwd):/app \
  --name claude-wrapper-container \
  claude-wrapper:latest \
  poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Environment Variables
- `PORT=9000` - Changes internal listening port
- `MAX_TIMEOUT=600` - Request timeout in seconds
- `ANTHROPIC_API_KEY=sk-xxx` - Direct API key auth
- `CLAUDE_CODE_USE_VERTEX=true` - Google Vertex AI mode
- `CLAUDE_CODE_USE_BEDROCK=true` - AWS Bedrock mode
- `API_KEYS=key1,key2` - API key protection

### Container Management
```bash
# View logs
docker logs claude-wrapper-container -f

# Stop/restart
docker stop claude-wrapper-container
docker start claude-wrapper-container

# Remove container
docker rm claude-wrapper-container

# Cleanup
docker system prune
```

### Remote Deployment
1. Push to registry:
   ```bash
   docker tag claude-wrapper:latest yourusername/claude-wrapper:latest
   docker push yourusername/claude-wrapper:latest
   ```

2. On remote server:
   ```bash
   docker pull yourusername/claude-wrapper:latest
   docker run -d -p 8000:8000 -v /path/to/claude:/root/.claude yourusername/claude-wrapper:latest
   ```

Remember: This wrapper is the bridge between AutoGen and Claude. Every change must maintain compatibility with both systems.