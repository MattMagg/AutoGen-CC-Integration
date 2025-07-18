# AutoGen Studio Integration Guide

## Overview

This directory contains test agents and configurations for AutoGen Studio UI integration.

## Created Files

### 1. Agent Configurations
- **`team.json`** - Complete team configuration with 3 specialized testing agents
- **`configs/test_agent_config.json`** - Individual comprehensive test agent
- **`configs/test_workflow.json`** - Testing workflow configuration
- **`configs/test_skills.json`** - Custom testing skills/functions

### 2. Python Scripts
- **`test_agent.py`** - Programmatic agent creation and team setup
- **`demo_test_agent.py`** - Demo script to test configurations

## How to Use in AutoGen Studio UI

### Step 1: Ensure Services are Running
```bash
# Claude wrapper must be running
curl http://localhost:8000/health

# AutoGen Studio should be running
# http://localhost:8080
```

### Step 2: Refresh AutoGen Studio
1. Go to http://localhost:8080 in your browser
2. You may need to restart AutoGen Studio to pick up new configurations:
   ```bash
   # Stop current instance (Ctrl+C)
   # Restart
   autogenstudio ui --port 8080 --appdir ./myapp
   ```

### Step 3: Find Your Agents
1. Navigate to the **Agents** section in the UI
2. Look for:
   - `comprehensive_test_agent` - Individual testing agent
   - `test_architect` - Test strategy planner
   - `test_developer` - Test implementation specialist
   - `test_reviewer` - Test quality reviewer

### Step 4: Find Your Teams
1. Navigate to the **Teams** section
2. Look for:
   - `Test Development Team` - Complete testing team workflow

### Step 5: Create a New Session
1. Click "New Session" or "New Chat"
2. Select either:
   - An individual agent (e.g., `comprehensive_test_agent`)
   - A team (e.g., `Test Development Team`)
3. Start interacting!

## Example Prompts to Try

### For Individual Test Agent:
- "Create unit tests for a user authentication function"
- "Design a test strategy for an e-commerce checkout flow"
- "Write integration tests for a REST API endpoint"

### For Test Team:
- "Create a comprehensive test suite for a todo list application"
- "Design and implement tests for a payment processing system"
- "Develop a testing strategy for a microservices architecture"

## Testing the Configuration

Run the demo script to verify everything is set up correctly:
```bash
cd myapp
python demo_test_agent.py
```

## Troubleshooting

### Agents Don't Appear in UI
1. Restart AutoGen Studio
2. Check that JSON files are valid:
   ```bash
   python -m json.tool team.json
   python -m json.tool configs/test_agent_config.json
   ```
3. Verify the wrapper is accessible:
   ```bash
   curl http://localhost:8000/v1/models
   ```

### Connection Errors
1. Ensure Claude wrapper is running on port 8000
2. Check that model name matches: `claude-opus-4-20250514`
3. Verify base_url in configs: `http://localhost:8000/v1`

### Database Issues
If you see database errors, you can reset:
```bash
rm autogen04202.db
# Restart AutoGen Studio
```

## Architecture

```
AutoGen Studio UI (port 8080)
         ↓
   Team/Agent Configs
         ↓
  OpenAI-Compatible API
         ↓
Claude Wrapper (port 8000)
         ↓
    Claude Opus 4
```

## Best Practices

1. **Temperature Settings**:
   - Architect/Planning: 0.7 (creative)
   - Implementation: 0.3 (precise)
   - Review: 0.5 (balanced)

2. **System Messages**:
   - Be specific about agent roles
   - Include clear instructions
   - Define output formats

3. **Termination Conditions**:
   - Use text mentions for approval workflows
   - Set reasonable message limits
   - Combine conditions with OR logic

4. **Team Composition**:
   - 3-5 agents per team optimal
   - Clear role separation
   - Sequential (RoundRobin) or dynamic (Selector) flow

## Next Steps

1. Experiment with different team compositions
2. Add custom tools/skills to agents
3. Create domain-specific testing agents
4. Integrate with actual test frameworks
5. Build workflows for your specific needs

Remember: AutoGen Studio provides a visual way to interact with your agents, but you can also use them programmatically with the scripts provided!