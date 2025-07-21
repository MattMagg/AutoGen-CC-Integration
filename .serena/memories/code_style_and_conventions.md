# Code Style and Conventions

## AutoGen Framework Conventions (v0.6.X)
- **AutoGen-First Principle**: Use native AutoGen features exclusively, avoid custom frameworks
- **Async Architecture**: All agent operations use async/await patterns with CancellationToken
- **Native Patterns**: Use 13+ built-in design patterns (RoundRobinGroupChat, SelectorGroupChat, etc.)
- **CloudEvents Compliance**: Event-driven architecture following CloudEvents specification
- **Model Client Pattern**: All LLM interactions through OpenAIChatCompletionClient

## Python Code Style (Wrapper Component)
- **Formatter**: Black with line-length = 100
- **Python Version**: Target Python 3.10+
- **Type Hints**: Required for all functions and methods
- **Async Patterns**: Use async/await for all I/O operations
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes

## File Organization
```
/wrapper/          # FastAPI service (Poetry managed)
  main.py          # FastAPI application entry point
  auth.py          # Authentication system
  claude_cli.py    # Claude SDK integration
  message_adapter.py  # OpenAI ↔ Claude format conversion
  session_manager.py # Conversation continuity
  models.py        # Pydantic request/response models
  test_*.py        # Test files

/autogen/          # AutoGen integration
  config.py        # Model client configuration
  quickstart.py    # Basic integration test
  examples/        # Multi-agent pattern examples
  studio/          # AutoGen Studio configuration

/docs-prd/         # High-level specifications (agent-parseable)
```

## Naming Conventions
- **Functions**: snake_case with descriptive names
- **Classes**: PascalCase (AgentManager, MessageAdapter)
- **Constants**: UPPER_SNAKE_CASE
- **Files**: snake_case.py
- **AutoGen Agents**: Descriptive role names (ResearcherAgent, AnalystAgent)

## Documentation Standards
- **Docstrings**: Required for all public functions and classes
- **Type Hints**: Mandatory for function signatures
- **Comments**: Explain complex logic, especially async workflows
- **PRD Compliance**: All specifications must be agent-parseable with verification commands

## AutoGen Specific Conventions
- **Agent Creation**: Always use AssistantAgent or UserProxyAgent as base
- **Group Coordination**: Use native GroupChat classes, never custom message buses
- **Tool Integration**: Use AutoGen's native tool system with @tool decorator
- **Memory Management**: Leverage conversation history, avoid custom state systems
- **Research Pattern**: Always check AutoGen MCP documentation before implementation

## Security Conventions
- **API Keys**: Store in environment variables or macOS Keychain
- **Authentication**: OAuth-based with proper token management
- **Input Validation**: Pydantic models for all API requests
- **Error Messages**: Never expose sensitive information in responses

## Testing Standards
- **Test Framework**: pytest with pytest-asyncio for async tests
- **Coverage**: Aim for comprehensive endpoint and functionality coverage
- **Integration Tests**: Include real AutoGen and Claude API integration tests
- **Performance Tests**: Validate response times and memory usage