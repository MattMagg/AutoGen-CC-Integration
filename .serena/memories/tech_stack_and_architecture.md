# Technology Stack and Architecture

## Core Framework
- **AutoGen v0.6.X** - Microsoft's multi-agent framework with async, event-driven architecture
- **Python >=3.9** - Primary development language
- **FastAPI** - Wrapper service for Claude API compatibility
- **Poetry** - Dependency management for wrapper component

## AutoGen Architecture (v0.6.X)
- **Core Layer**: Event-driven actor framework, CloudEvents specification
- **AgentChat Layer**: High-level conversational API (RoundRobinGroupChat, SelectorGroupChat)
- **Extensions Layer**: LLM clients, tools, memory integrations

## Key AutoGen Components
- `autogen-agentchat>=0.6.4` - Conversational agents and teams
- `autogen-core>=0.6.4` - Event-driven runtime with CancellationToken
- `autogen-ext>=0.6.4` - Extensions and integrations
- `OpenAIChatCompletionClient` - Model client for LLM interactions
- `AssistantAgent` - Base agent implementation
- `GroupChat` patterns - Multi-agent coordination

## Integration Stack
- **Claude Models**: claude-opus-4-20250514, claude-sonnet-4-20250514
- **Authentication**: OAuth via macOS Keychain (local only, no Docker support)
- **Communication**: HTTP/HTTPS with OpenAI v1 API compatibility
- **Distributed Runtime**: gRPC with Protocol Buffers, Microsoft Orleans support
- **Event System**: CloudEvents for standardized messaging

## Development Tools
- **AutoGen Studio**: No-code GUI for agent prototyping (port 8080)
- **AutoGen Bench (agbench)**: Performance benchmarking with Docker
- **MCP Servers**: AutoGen docs, Sequential thinking, Graphiti memory
- **VSCode**: Primary development environment

## File Structure
```
/wrapper/          # FastAPI service (Poetry managed)
/autogen/          # AutoGen integration and examples
/docs-prd/         # System specifications
/autogen/studio/   # Studio configuration and database
/.claude/Hooks/    # Sequential-Graphiti integration
```