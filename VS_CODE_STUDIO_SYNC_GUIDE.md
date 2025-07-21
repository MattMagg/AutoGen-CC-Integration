# VS Code ↔ AutoGen Studio Synchronization Workflow Guide

## 🎯 Complete Integration Overview

This guide provides the complete workflow for seamlessly synchronizing agent development between VS Code and AutoGen Studio, enabling visual interaction with programmatically created agents.

## 📋 Prerequisites and Verification

### 1. Core Dependencies
```bash
# Verify Claude Code CLI is available
claude-code --version

# Verify AutoGen Studio installation
pip show autogenstudio
```

### 2. Environment Setup
```bash
# Clone and setup the integration repository
git clone https://github.com/your-repo/autogen-claude-integration
cd autogen-claude-integration

# Install dependencies
pip install -r requirements.txt
```

### 3. Claude Wrapper Configuration
```bash
# Navigate to wrapper directory
cd wrapper

# Install wrapper dependencies
poetry install

# Verify Claude authentication
export ANTHROPIC_API_KEY="your-api-key"
# OR for other providers:
# export CLAUDE_CODE_USE_BEDROCK=1  # AWS Bedrock
# export CLAUDE_CODE_USE_VERTEX=1   # Google Vertex AI

# Test wrapper startup
poetry run python main.py
```

### 4. Verification Commands
```bash
# Test Claude wrapper endpoints
curl http://localhost:8000/health
curl http://localhost:8000/v1/models

# Start AutoGen Studio
cd ../autogen/studio
autogenstudio ui --port 8080 --appdir ./

# Verify Studio is accessible
curl http://localhost:8080
```

## 🔧 VS Code Agent Development Workflow

### 1. Programmatic Agent Creation

#### A. Single Agent Creation
```python
# File: /autogen/studio/test_agent.py
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure Claude model client
model_client = OpenAIChatCompletionClient(
    model="claude-opus-4-20250514",
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
    timeout=600.0,
    temperature=0.7
)

# Create specialized agent
test_agent = AssistantAgent(
    name="comprehensive_test_agent",
    model_client=model_client,
    description="Comprehensive testing agent for software QA",
    system_message="""You are a comprehensive testing agent specializing in:
    1. Test Strategy Design
    2. Test Implementation
    3. Test Automation
    4. Quality Metrics
    5. Bug Analysis
    [... detailed instructions ...]""",
    tools=[],  # Add testing tools as needed
    model_client_stream=True,
)
```

#### B. Team Creation
```python
# Create multiple specialized agents
test_architect = AssistantAgent(
    name="test_architect",
    model_client=model_client,
    description="Plans and designs comprehensive test strategies",
    system_message="Design test strategies ensuring complete coverage..."
)

test_developer = AssistantAgent(
    name="test_developer", 
    model_client=model_client,
    description="Implements high-quality test code",
    system_message="Write clean, maintainable test code..."
)

test_reviewer = AssistantAgent(
    name="test_reviewer",
    model_client=model_client, 
    description="Reviews and approves test quality",
    system_message="Ensure tests meet quality standards..."
)

# Create team with termination conditions
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination

termination = TextMentionTermination("APPROVED") | MaxMessageTermination(15)

team = RoundRobinGroupChat(
    participants=[test_architect, test_developer, test_reviewer],
    termination_condition=termination,
)
```

### 2. Configuration Export

#### A. Generate JSON Configurations
```python
# File: /autogen/studio/studio_setup_helper.py
def export_agent_config(agent, config_path):
    """Export agent configuration to JSON"""
    config = {
        "name": agent.name,
        "description": agent.description,
        "system_message": agent.system_message,
        "model_client": {
            "model": "claude-opus-4-20250514",
            "base_url": "http://localhost:8000/v1",
            "api_key": "not-needed",
            "temperature": 0.7,
            "max_tokens": 4096
        },
        "type": "assistant"
    }
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
```

#### B. Team Configuration Export
```python
def export_team_config(team, team_path):
    """Export team configuration to JSON"""
    team_config = {
        "name": "Test Development Team",
        "description": "Comprehensive testing team workflow",
        "participants": [
            export_participant_config(p) for p in team._participants
        ],
        "termination_condition": {
            "type": "combination",
            "conditions": [
                {"type": "text_mention", "text": "APPROVED"},
                {"type": "max_messages", "max_messages": 15}
            ]
        }
    }
    
    with open(team_path, 'w') as f:
        json.dump(team_config, f, indent=2)
```

## 🚀 AutoGen Studio Registration Process

### 1. Automatic Registration Script

#### A. API-Based Registration
```python
# File: /autogen/studio/register_agents_in_studio.py
import requests

STUDIO_API_BASE = "http://localhost:8080/api"

def register_model():
    """Register Claude model in AutoGen Studio"""
    model_data = {
        "name": "Claude Opus via Wrapper",
        "model": "claude-opus-4-20250514", 
        "api_type": "openai",
        "base_url": "http://localhost:8000/v1",
        "description": "Claude Opus 4 via local OpenAI-compatible wrapper"
    }
    
    response = requests.post(f"{STUDIO_API_BASE}/models", json=model_data)
    if response.status_code == 200:
        return response.json()["id"]
    return None

def register_agent(agent_config, model_id):
    """Register agent in AutoGen Studio"""
    agent_data = {
        "name": agent_config["name"],
        "description": agent_config["description"],
        "system_message": agent_config["system_message"],
        "model_id": model_id,
        "type": "assistant",
        "config": {
            "temperature": agent_config.get("model_client", {}).get("temperature", 0.5),
            "max_tokens": agent_config.get("model_client", {}).get("max_tokens", 4096)
        }
    }
    
    response = requests.post(f"{STUDIO_API_BASE}/agents", json=agent_data)
    if response.status_code == 200:
        return response.json()["id"]
    return None
```

#### B. Direct Database Registration
```python
def use_database_direct():
    """Alternative: Register directly in AutoGen Studio database"""
    from autogenstudio.database import DatabaseManager
    from autogenstudio.datamodel import Agent, Model
    
    db = DatabaseManager(
        engine_uri="sqlite:///autogen04202.db",
        base_dir=str(Path(__file__).parent)
    )
    
    # Create model
    model = Model(
        name="Claude Opus Wrapper",
        model="claude-opus-4-20250514",
        api_type="openai", 
        base_url="http://localhost:8000/v1",
        description="Claude Opus via local wrapper"
    )
    
    # Create agents from configs
    agents = []
    for config in load_agent_configs():
        agent = Agent(
            name=config["name"],
            description=config["description"],
            system_message=config["system_message"],
            type="assistant",
            model_id=model.id
        )
        agents.append(agent)
```

### 2. Registration Execution
```bash
# Execute registration script
cd /autogen/studio
python register_agents_in_studio.py

# Verify registration
curl http://localhost:8080/api/agents
curl http://localhost:8080/api/models
```

## 🎨 AutoGen Studio Visualization Workflow

### 1. Team Builder Method

#### A. Visual Configuration
1. **Navigate to Team Builder**
   ```
   http://localhost:8080/build
   ```

2. **Create New Team**
   - Click "New Team"
   - Name: "Test Development Team"

3. **Add Agents from Component Library**
   - Drag "AssistantAgent" from Component Library
   - Configure each instance:
     - **Name**: `test_architect`
     - **System Message**: (copy from generated configs)
     - **Model**: `claude-opus-4-20250514`
     - **Base URL**: `http://localhost:8000/v1`
     - **API Type**: `OpenAI`
     - **Temperature**: `0.7`

4. **Configure Team Settings**
   - Set termination condition to `OrTerminationCondition`
   - Add `TextMentionTermination` with "APPROVED"
   - Add `MaxMessageTermination` with 15 messages

5. **Save and Deploy**
   - Click "Save Team"
   - Test with "Run Team"

#### B. Component Library Understanding
- **Important**: Component Library shows agent TYPES, not instances
- Available types: `AssistantAgent`, `UserProxyAgent`, etc.
- Custom agents = Type + Configuration
- System messages make agents specialized

### 2. Playground Method (Recommended)

#### A. Import Workflow
```bash
# Generate workflow file
python studio_setup_helper.py --export-workflow

# Import in Playground
# 1. Go to http://localhost:8080/playground
# 2. Click "Import" or "Load"
# 3. Select: /autogen/studio/test_workflow.json
# 4. Start using immediately
```

#### B. Quick Configuration
1. **Start New Session**
   - Go to Playground
   - Click "New Session" or "+"

2. **Configure Default Agents**
   - Set Model: `claude-opus-4-20250514`
   - Set Base URL: `http://localhost:8000/v1`
   - Set API Type: `OpenAI`
   - Leave API Key empty or "not-needed"

3. **Test Interaction**
   ```
   # Example prompts:
   "Create unit tests for a login function that validates email and password"
   "Design a test strategy for a payment processing system"
   "Write integration tests for a REST API with authentication"
   ```

### 3. Session Management

#### A. Session Continuity
```python
# In VS Code - create session-aware agents
session_id = "test-session-001"

# All requests maintain conversation context
chat_request = {
    "model": "claude-opus-4-20250514",
    "messages": conversation_history,
    "session_id": session_id  # Maintains context
}
```

#### B. Session Monitoring
```bash
# Check active sessions
curl http://localhost:8000/v1/sessions

# Get session details
curl http://localhost:8000/v1/sessions/{session_id}

# Delete session
curl -X DELETE http://localhost:8000/v1/sessions/{session_id}
```

## 🛠️ Troubleshooting Common Issues

### 1. Connection Issues

#### A. Wrapper Not Responding
```bash
# Check wrapper status
curl http://localhost:8000/health

# Check wrapper logs
cd wrapper && poetry run python main.py

# Common fixes:
- Verify ANTHROPIC_API_KEY is set
- Check port 8000 is not in use
- Restart wrapper service
```

#### B. AutoGen Studio Connection Errors
```bash
# Verify Studio is running
curl http://localhost:8080

# Check Studio logs
autogenstudio ui --port 8080 --appdir ./ --debug

# Common fixes:
- Restart AutoGen Studio
- Clear browser cache
- Check port 8080 availability
```

### 2. Agent Registration Issues

#### A. Agents Not Appearing
```bash
# Restart AutoGen Studio
# Ctrl+C to stop, then:
autogenstudio ui --port 8080 --appdir ./

# Validate JSON configs
python -m json.tool team.json
python -m json.tool configs/test_agent_config.json

# Reset database if needed
rm autogen04202.db
# Restart AutoGen Studio
```

#### B. Model Configuration Errors
```bash
# Verify model registration
curl http://localhost:8080/api/models

# Check wrapper models
curl http://localhost:8000/v1/models

# Ensure base_url consistency:
# VS Code configs: "http://localhost:8000/v1"
# Studio configs: "http://localhost:8000/v1"
```

### 3. Performance Issues

#### A. Slow Response Times
```bash
# Check wrapper timeout settings
export MAX_TIMEOUT=600000  # 10 minutes

# Monitor session memory usage
curl http://localhost:8000/v1/sessions/stats

# Optimize team size (3-5 agents optimal)
```

#### B. Memory Management
```bash
# Clear old sessions
curl -X DELETE http://localhost:8000/v1/sessions/{old_session_id}

# Monitor database size
ls -la autogen04202.db

# Reset if database becomes large
rm autogen04202.db && autogenstudio ui --port 8080 --appdir ./
```

## 📊 Success Verification

### 1. End-to-End Test
```python
# File: test_complete_integration.py
async def test_full_workflow():
    """Test complete VS Code to Studio workflow"""
    
    # 1. Create agent in VS Code
    agent = await create_test_agent()
    assert agent.name == "comprehensive_test_agent"
    
    # 2. Export configuration
    export_agent_config(agent, "test_config.json")
    assert Path("test_config.json").exists()
    
    # 3. Register in Studio
    model_id = register_model()
    agent_id = register_agent(load_config("test_config.json"), model_id)
    assert agent_id is not None
    
    # 4. Verify in Studio API
    response = requests.get(f"{STUDIO_API_BASE}/agents/{agent_id}")
    assert response.status_code == 200
    
    # 5. Test interaction
    test_response = await test_agent_interaction(agent)
    assert "test" in test_response.lower()
    
    print("✅ Full workflow test passed!")
```

### 2. Performance Benchmarks
```bash
# Wrapper response time
time curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-20250514","messages":[{"role":"user","content":"Hello"}]}'

# Studio response time
# Measure in browser dev tools or use:
curl -w "@curl-format.txt" http://localhost:8080/api/agents
```

### 3. Integration Checklist
- [ ] Claude wrapper running on port 8000
- [ ] AutoGen Studio running on port 8080  
- [ ] Model registered in Studio
- [ ] Agents created programmatically in VS Code
- [ ] Agents exported to JSON configurations
- [ ] Agents registered in Studio database/API
- [ ] Team Builder shows configured agents
- [ ] Playground can import workflows
- [ ] End-to-end conversation works
- [ ] Session management functions
- [ ] Performance within acceptable limits

## 🎯 Best Practices and Optimization

### 1. Agent Design Patterns
```python
# Template for VS Code agent creation
class AgentFactory:
    @staticmethod
    def create_specialist_agent(name, role, temperature=0.7):
        return AssistantAgent(
            name=name,
            model_client=get_claude_client(temperature),
            description=f"Specialized {role} agent",
            system_message=get_role_prompt(role),
            tools=get_role_tools(role),
            model_client_stream=True
        )

# Usage
agents = {
    "architect": AgentFactory.create_specialist_agent("test_architect", "planning", 0.7),
    "developer": AgentFactory.create_specialist_agent("test_developer", "implementation", 0.3),
    "reviewer": AgentFactory.create_specialist_agent("test_reviewer", "review", 0.5)
}
```

### 2. Configuration Management
```python
# Centralized config management
class ConfigManager:
    def __init__(self, config_dir="./configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
    
    def save_agent_config(self, agent, version="latest"):
        config_path = self.config_dir / f"{agent.name}_{version}.json"
        export_agent_config(agent, config_path)
        return config_path
    
    def load_agent_config(self, name, version="latest"):
        config_path = self.config_dir / f"{name}_{version}.json"
        with open(config_path) as f:
            return json.load(f)
```

### 3. Monitoring and Logging
```python
# Enhanced logging for debugging
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vs_code_studio_sync.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log agent operations
def log_agent_operation(operation, agent_name, status, details=None):
    logger.info(f"AGENT_OP: {operation} | {agent_name} | {status} | {details}")
```

## 🔄 Continuous Integration

### 1. Automated Sync Pipeline
```bash
#!/bin/bash
# File: sync_agents.sh

echo "🔄 Starting VS Code ↔ Studio sync..."

# 1. Export agents from VS Code
echo "📤 Exporting agent configurations..."
python export_agents.py

# 2. Register in Studio
echo "📝 Registering agents in Studio..."
python register_agents_in_studio.py

# 3. Verify registration
echo "✅ Verifying registration..."
python verify_registration.py

# 4. Test end-to-end
echo "🧪 Testing complete workflow..."
python test_complete_integration.py

echo "✨ Sync complete!"
```

### 2. Version Control Integration
```bash
# Track agent configurations in git
git add configs/*.json
git add studio_configs/*.json
git commit -m "Update agent configurations"

# Tag releases
git tag -a v1.0.0 -m "Stable agent configuration release"
git push origin v1.0.0
```

## 📈 Advanced Features

### 1. Multi-Model Support
```python
# Support multiple Claude models
CLAUDE_MODELS = {
    "claude-opus-4": {"temperature": 0.7, "max_tokens": 4096},
    "claude-sonnet-4": {"temperature": 0.5, "max_tokens": 8192}, 
    "claude-haiku": {"temperature": 0.3, "max_tokens": 2048}
}

def create_model_variant_agents(base_agent_config):
    """Create agent variants for different models"""
    agents = {}
    for model, params in CLAUDE_MODELS.items():
        config = base_agent_config.copy()
        config["model_client"].update(params)
        config["name"] = f"{config['name']}_{model.split('-')[1]}"
        agents[model] = config
    return agents
```

### 2. Dynamic Agent Scaling
```python
# Auto-scale agents based on workload
class AgentScaler:
    def __init__(self, max_agents=10):
        self.max_agents = max_agents
        self.active_agents = {}
    
    async def scale_agents(self, workload_metrics):
        if workload_metrics.avg_response_time > 10:  # seconds
            await self.add_agent()
        elif workload_metrics.idle_time > 300:  # 5 minutes
            await self.remove_agent()
    
    async def add_agent(self):
        if len(self.active_agents) < self.max_agents:
            agent = await create_load_balancer_agent()
            self.active_agents[agent.name] = agent
            await register_agent_runtime(agent)
```

## 🎓 Summary

This comprehensive guide enables seamless integration between VS Code agent development and AutoGen Studio visualization. The workflow supports:

- **Programmatic Development**: Create sophisticated agents in VS Code
- **Visual Interaction**: Use AutoGen Studio's UI for testing and deployment
- **Bidirectional Sync**: Changes in either environment propagate properly
- **Production Ready**: Robust error handling and monitoring
- **Scalable Architecture**: Support for complex multi-agent systems

Follow this guide for efficient agent development cycles and production-ready deployments.