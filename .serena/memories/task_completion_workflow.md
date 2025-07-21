# Task Completion Workflow

## Pre-Development Checklist
1. **Verify System Health**
   ```bash
   curl -s http://localhost:8000/health | jq '.status'  # Must return "healthy"
   claude auth status  # Verify OAuth authentication
   cd autogen && python quickstart.py  # Basic integration test
   ```

2. **Research AutoGen Capabilities** (MANDATORY for v0.6.X)
   ```bash
   mcp__autogen-docs__fetch_autogen_documentation
   mcp__autogen-docs__search_autogen_documentation query:"[relevant_feature]"
   ```

3. **Validate Native Pattern Usage**
   - Confirm AutoGen provides the needed functionality natively
   - Avoid custom implementations of existing features
   - Use native GroupChat patterns for coordination

## During Development
1. **AutoGen-First Approach**
   - Use native features before considering custom code
   - Validate against latest documentation continuously
   - Prototype in AutoGen Studio when possible

2. **Incremental Testing**
   - Test wrapper health after changes: `curl http://localhost:8000/health`
   - Run basic AutoGen tests: `python quickstart.py`
   - Verify authentication: `claude --print "test"`

## Task Completion Validation
1. **Code Quality Checks**
   ```bash
   # Wrapper formatting
   cd wrapper && poetry run black .
   
   # Run wrapper tests
   poetry run pytest
   poetry run python test_endpoints.py
   ```

2. **Integration Testing**
   ```bash
   # Test single agent functionality
   cd autogen && python examples/single_agent_example.py
   
   # Test multi-agent patterns (when implemented)
   python examples/multi_agent_examples.py
   ```

3. **Performance Validation**
   ```bash
   # Response time check (should be <700ms)
   time curl -X POST http://localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model": "claude-opus-4-20250514", "messages": [{"role": "user", "content": "test"}]}'
   
   # Memory usage check (should be <500MB)
   ps aux | grep uvicorn | awk '{print $6}'
   ```

4. **AutoGen Compliance Verification**
   ```bash
   # Verify native feature usage
   grep -r "from autogen" . | wc -l  # Should be >50
   
   # Check for prohibited custom implementations
   ! grep -r 'custom.*framework\|custom.*protocol' .
   
   # Validate native pattern usage
   grep -r "RoundRobin\|Selector\|GroupChat" .
   ```

## Final Validation Protocol
1. **End-to-End Testing**
   - Start fresh wrapper instance
   - Run complete AutoGen integration test
   - Verify all agent patterns work correctly
   - Test with AutoGen Studio if applicable

2. **Performance Benchmarking** (when applicable)
   ```bash
   # Run AutoGen Bench for relevant capabilities
   agbench run --suite relevant_benchmarks
   # Target: >80% success rate
   ```

3. **Documentation Update**
   - Update memory files if workflow changes
   - Document any new patterns or capabilities discovered
   - Record performance baseline measurements

## Error Recovery Procedures
- **Wrapper Connection Refused**: `cd wrapper && poetry run uvicorn main:app --reload --port 8000`
- **Authentication Failure**: `claude auth logout && claude auth login`
- **AutoGen Import Errors**: `pip install --upgrade 'autogen-agentchat>=0.6.4'`
- **Model Not Found**: Verify model name matches supported models (claude-opus-4-20250514, claude-sonnet-4-20250514)

## Success Criteria
- ✅ All verification commands pass
- ✅ Wrapper responds within performance thresholds
- ✅ AutoGen integration tests successful
- ✅ Native pattern usage verified
- ✅ No custom framework implementations
- ✅ Authentication working
- ✅ Memory usage within limits
- ✅ Code formatted and tested