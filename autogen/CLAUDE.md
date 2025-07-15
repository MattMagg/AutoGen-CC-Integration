# AutoGen Claude Integration - Project Instructions

## PROJECT CONTEXT

This directory contains the AutoGen integration for Claude Opus 4 via Claude Code OpenAI wrapper. This setup uses:

- **Claude Code CLI OAuth tokens** (not API keys) from macOS Keychain
- **Native wrapper execution** on localhost:8000 (no Docker due to OAuth limitations)
- **Direct localhost connection** (no ngrok needed for local development)
- **Model**: claude-opus-4-20250514 with full capabilities

## MANDATORY PREREQUISITES

Before ANY AutoGen operations, verify:

```bash
# 1. Wrapper is running natively
curl http://localhost:8000/v1/models | jq '.data[].id'
# MUST return: "claude-opus-4-20250514" among others

# 2. Claude CLI authenticated
claude auth status
# MUST show authenticated status
```

If either fails, STOP and report:
```
LIMITATION IDENTIFIED: Claude wrapper not accessible
EVIDENCE: curl http://localhost:8000/v1/models returned [error]
IMPACT: Cannot proceed with AutoGen testing
```

## VERIFICATION COMMANDS

### Quick Health Check
```bash
python3 -c "from config import ensure_health; ensure_health()"
```

### Test Setup
```bash
# Direct localhost connection (no URL parameter needed)
python quickstart.py
```

### Verify Dependencies
```bash
python3 -c "import autogen_agentchat, autogen_ext, autogen_core; print('✅ AutoGen installed')"
```

## AUTOGEN-SPECIFIC PATTERNS

### Model Client Creation
```python
# ALWAYS use our config module
from config import get_model_client
client = get_model_client()  # Handles auth, retry, capabilities

# NEVER use direct OpenAI client with API keys
```

### Agent Communication Patterns
- **AssistantAgent**: Requires `CancellationToken()` in AutoGen v0.4+
- **RoundRobinGroupChat**: Use for sequential agent conversations
- **SelectorGroupChat**: Use for dynamic agent selection
- **TextMessage**: Use `TextMessage(content=msg, source="name")`
- **Termination**: Always set termination conditions to prevent infinite loops

### Error Handling
```python
# Use our retry decorator for all agent operations
from utils.helpers import async_retry

@async_retry(max_attempts=3)
async def agent_operation():
    return await agent.on_messages([...], CancellationToken())
```

## TESTING REQUIREMENTS

### MANDATORY: Real Execution Only
```bash
# ✅ CORRECT: Execute actual commands
python examples/single_agent_example.py
# Observe actual output, errors, token usage

# ❌ FORBIDDEN: Simulating results
"The example should work correctly"  # NEVER claim without execution
```

### Validation Must Include
1. **Import verification**: `python3 -c "from config import ..."`
2. **Health check**: `ensure_health()` must pass
3. **Actual agent execution**: Run examples, observe responses
4. **Token tracking**: Verify usage is logged

## COMMON COMMANDS

### Run Examples
```bash
# Single agent patterns
python examples/single_agent_example.py

# Multi-agent patterns  
python examples/multi_agent_examples.py
```

### Debug Connection Issues
```bash
# Check wrapper
curl -v http://localhost:8000/v1/models

# Check auth status
claude auth status

# Test with direct HTTP
python3 -c "import requests; print(requests.get('http://localhost:8000/v1/models').json())"
```

## ARCHITECTURAL NOTES

### Request Flow
```
AutoGen Agent → OpenAIChatCompletionClient → localhost:8000 → Native Wrapper → Claude Code SDK → Claude API
                     ↑                           ↑                    ↑
                 config.py                  Direct                OAuth from
                                        Connection            macOS Keychain
```

### Key Files
- `config.py`: Core configuration, auth, retry logic
- `quickstart.py`: Basic validation script
- `examples/`: Single and multi-agent patterns
- `utils/helpers.py`: Retry decorators, token tracking

## DEVELOPMENT WORKFLOW

1. **Start wrapper**: `cd /path/to/claude-code-openai-wrapper && poetry run uvicorn main:app --host 0.0.0.0 --port 8000`
2. **Test connection**: `python quickstart.py`
3. **Develop**: Make changes, test with examples
4. **Verify**: Always execute, never simulate

## CRITICAL REMINDERS

- **NO SIMULATED TESTS**: If you can't execute it, report as limitation
- **NO API KEYS**: This uses OAuth tokens from Claude Code CLI
- **WRAPPER REQUIRED**: Nothing works without the wrapper running natively
- **LOCALHOST ONLY**: Direct connection to localhost:8000 (no ngrok/docker)
- **REAL EXECUTION**: Every claim must be backed by command output

## TOKEN USAGE TRACKING

After any agent operation:
```python
from utils.helpers import TokenUsageTracker
tracker = TokenUsageTracker()
# ... agent operations ...
print(tracker.get_summary())
```

## ERROR REPORTING FORMAT

When operations fail:
```
OPERATION: [what was attempted]
COMMAND: [exact command executed]
OUTPUT: [complete error output]
DIAGNOSIS: [root cause analysis]
RESOLUTION: [how to fix, or why it can't be fixed]
```

Remember: This integration bridges AutoGen with Claude through native execution. Always verify the wrapper is running before claiming success.