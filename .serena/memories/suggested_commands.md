# Essential Development Commands

## System Verification
```bash
# 1. Verify AutoGen installation and versions
pip show autogen-agentchat autogen-core autogen-ext | grep Version

# 2. Test AutoGen native imports (critical for v0.6.X)
python -c "from autogen_agentchat.teams import RoundRobinGroupChat; print('Groups: OK')"
python -c "from autogen_agentchat.agents import AssistantAgent; print('Agents: OK')"
python -c "from autogen_core import CancellationToken; print('Core: OK')"

# 3. Check Claude wrapper health
curl -s http://localhost:8000/health | jq '.status'  # Expected: "healthy"

# 4. Verify Claude CLI OAuth authentication
claude --print "test" 2>&1 | grep -q "test" && echo "OAuth: PASS"

# 5. Verify model availability
curl -s http://localhost:8000/v1/models | jq '.data[0].id'
```

## Wrapper Development (FastAPI)
```bash
# Start wrapper in development mode (from /wrapper directory)
cd wrapper
poetry install
poetry run uvicorn main:app --reload --port 8000

# Run wrapper tests
poetry run pytest
poetry run python test_endpoints.py
poetry run python test_basic.py

# Code formatting
poetry run black .
```

## AutoGen Development
```bash
# Basic AutoGen test
cd autogen
python quickstart.py

# Run single agent example
python examples/single_agent_example.py

# Run multi-agent examples (when implemented)
python examples/multi_agent_examples.py
```

## AutoGen Studio
```bash
# Start AutoGen Studio GUI
autogenstudio ui --port 8080 --appdir ./my-app

# Check Studio database
sqlite3 autogen/studio/autogen04202.db ".tables"
```

## AutoGen Bench (Performance Testing)
```bash
# Install and run benchmarks
pip install agbench
agbench run --suite relevant_benchmarks
```

## Verification Protocol (Pre-Development)
```bash
# Always run before starting development:
curl http://localhost:8000/health          # Wrapper health
claude auth status                         # OAuth status  
cd autogen && python quickstart.py        # Basic integration
```

## MCP Research Commands
```bash
# Research AutoGen capabilities (CRITICAL for v0.6.X)
mcp__autogen-docs__fetch_autogen_documentation
mcp__autogen-docs__search_autogen_documentation query:"GroupChat"
mcp__autogen-docs__search_autogen_documentation query:"AssistantAgent"
```

## System Monitoring
```bash
# Check running processes
ps aux | grep "uvicorn\|autogen"

# Monitor memory usage  
ps aux | grep uvicorn | awk '{print $6}'  # Should be <500MB

# Check port usage
lsof -i:8000  # Wrapper
lsof -i:8080  # Studio
```