# MULTI-AGENT ORCHESTRATION SYSTEM - TECHNICAL SPECIFICATION

DOCUMENT_TYPE: agent_parseable_specification
SPECIFICATION_VERSION: 2.0
LAST_VERIFIED: 2025-07-18T22:40:00Z
VERIFICATION_COMMAND: cd /Users/mac-main/autogen-claude-integration && python autogen/quickstart.py

## SYSTEM_IDENTIFICATION

SYSTEM_NAME: multi_agent_orchestration
PRIMARY_FUNCTION: translate_openai_to_claude_for_autogen
ARCHITECTURE_PATTERN: wrapper_based_integration
CURRENT_STATE: partially_implemented

## VERSION_INFORMATION

```yaml
autogen_version:
  current_stable: "0.6.X"
  migration_guide: "https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/migration-guide.html"
  legacy_support: 
    v0.2: "pip install autogen-agentchat~=0.2"
    note: "v0.2 no longer under Microsoft control since 0.2.34"
  
architecture_changes:
  v0.4_rewrite: "From-the-ground-up rewrite with async, event-driven architecture"
  publish_subscribe: "Based on CloudEvents specification"
  layered_design:
    - core_api: "Event-driven actor framework"
    - agentchat_api: "Task-driven high-level framework"
    - extensions_api: "First and third-party extensions"
```

## CURRENT_SYSTEM_STATE

```yaml
components:
  wrapper:
    status: OPERATIONAL
    location: /Users/mac-main/autogen-claude-integration/wrapper/
    entry_point: main.py
    health_check: curl -s http://localhost:8000/health
    expected_response: '{"status":"healthy","service":"claude-code-openai-wrapper"}'
    
  autogen_integration:
    status: PARTIALLY_OPERATIONAL
    location: /Users/mac-main/autogen-claude-integration/autogen/
    working_features:
      - single_agent_conversations
      - basic_multi_agent_setup
      - oauth_authentication
      - token_tracking
    incomplete_features:
      - multi_agent_examples
      - comprehensive_error_handling
      - integration_test_suite
      
  studio_integration:
    status: CONFIGURED
    database: /autogen/studio/autogen04202.db
    config_files:
      - studio/configs/test_agent_config.json
      - studio/configs/test_workflow.json
      - studio/team.json
```

## TECHNICAL_CONSTRAINTS

```yaml
authentication_constraints:
  type: OAuth
  storage: macOS_Keychain
  scope: machine_specific
  limitation: NO_DOCKER_SUPPORT
  reason: keychain_access_restricted_to_host
  
deployment_constraints:
  execution: LOCAL_ONLY
  port: 8000
  protocol: HTTP
  sharing: SINGLE_USER
  
model_constraints:
  supported_models:
    - claude-opus-4-20250514
    - claude-sonnet-4-20250514
  api_format: OpenAI_v1
  endpoint: /v1/chat/completions
  
dependency_constraints:
  python_version: ">=3.9"
  autogen_version: ">=0.6.4"
  critical_features:
    - CancellationToken
    - TextMessage
    - async_support
    - model_client_architecture
    - CloudEvents_specification
    - Protocol_Buffers_for_distributed
```

## COMPONENT_SPECIFICATIONS

### COMPONENT_1: claude_code_wrapper
```yaml
component_id: claude_code_wrapper
location: /wrapper/
entry_point: main.py
port: 8000
framework: FastAPI

endpoints:
  health:
    path: /health
    method: GET
    response: {"status": "healthy", "service": "claude-code-openai-wrapper"}
    
  models:
    path: /v1/models
    method: GET
    response_type: OpenAI_models_format
    
  chat_completions:
    path: /v1/chat/completions
    method: POST
    request_schema: OpenAI_ChatCompletionRequest
    response_schema: OpenAI_ChatCompletionResponse
    
dependencies:
  - fastapi==0.68.0
  - claude-code-sdk>=0.1.0
  - pydantic>=1.8.0
  - httpx>=0.24.0
  
verification_commands:
  - curl -s http://localhost:8000/health | jq '.status'
  - curl -s http://localhost:8000/v1/models | jq '.data[0].id'
```

### COMPONENT_2: autogen_integration
```yaml
component_id: autogen_integration
location: /autogen/
config_module: config.py
autogen_version: ">=0.6.4"

functions:
  get_model_client:
    file: config.py
    signature: "def get_model_client(temperature: float = 0.7) -> OpenAIChatCompletionClient"
    returns: configured_client_instance
    async_cleanup_required: "await model_client.close()"
    
  ensure_health:
    file: config.py
    signature: "def ensure_health() -> None"
    raises: ConnectionError
    
v0.6_specific_features:
  model_client_pattern: "All LLM interactions through model clients"
  async_architecture: "Event-driven with CancellationToken support"
  message_types:
    - TextMessage
    - ToolCallRequestEvent
    - ToolCallExecutionEvent
    
required_imports:
  - from autogen_agentchat.agents import AssistantAgent
  - from autogen_agentchat.messages import TextMessage
  - from autogen_core import CancellationToken
  - from autogen_ext.models.openai import OpenAIChatCompletionClient
  - from autogen_core.models import ChatCompletionClient
  
verification_script: |
  cd /Users/mac-main/autogen-claude-integration/autogen
  python -c "from config import get_model_client; client = get_model_client(); print('SUCCESS')"
  python -c "import autogen_agentchat; print(f'Version: {autogen_agentchat.__version__}')"
```

### COMPONENT_3: orchestration_patterns
```yaml
component_id: orchestration_patterns
location: /autogen/examples/

implemented_patterns:
  sequential_chat:
    file: multi_agent_examples.py
    function: sequential_chat_example
    status: PARTIALLY_IMPLEMENTED
    agents: [researcher, analyst, writer]
    
  group_chat:
    file: multi_agent_examples.py  
    function: group_chat_example
    status: NOT_IMPLEMENTED
    required_imports:
      - from autogen_agentchat.teams import RoundRobinGroupChat
      - from autogen_agentchat.teams import SelectorGroupChat
      
  nested_chat:
    file: multi_agent_examples.py
    function: nested_chat_example  
    status: NOT_IMPLEMENTED
    
verification_commands:
  - grep -n "async def sequential_chat_example" autogen/examples/multi_agent_examples.py
  - grep -n "async def group_chat_example" autogen/examples/multi_agent_examples.py || echo "NOT_FOUND"
```

### COMPONENT_4: studio_integration
```yaml
component_id: studio_integration
location: /autogen/studio/
database: autogen04202.db

config_files:
  agents:
    - path: configs/test_agent_config.json
      content_type: autogen_agent_definition
      
  workflows:
    - path: configs/test_workflow.json
      content_type: workflow_configuration
      
  teams:
    - path: team.json
      content_type: team_composition
      
helper_scripts:
  setup: studio_setup_helper.py
  registration: register_agents_in_studio.py
  
required_settings:
  model: "claude-opus-4-20250514"
  base_url: "http://localhost:8000/v1"
  api_type: "openai"
  
validation_command: |
  python -m json.tool autogen/studio/team.json > /dev/null && echo "VALID_JSON"
```

### COMPONENT_5: sequential_graphiti_integration
```yaml
component_id: sequential_graphiti_integration
location: /.claude/Hooks/

core_files:
  hook_script:
    path: sequential-synthesis-hook.sh
    type: bash_script
    triggers_on: mcp__sequential-thinking__process_thought
    
  output_directory:
    path: synthesis_output/
    file_pattern: ready_for_synthesis_*.json
    
  command:
    path: .claude/commands/graphiti.sh
    invocation: /graphiti
    
hook_logic: |
  if [[ "$next_thought_needed" == "false" ]] && [[ $thought_count -ge 3 ]]; then
    create_synthesis_file
  fi
  
verification_commands:
  - ls -la .claude/Hooks/sequential-synthesis-hook.sh
  - ls -la .claude/Hooks/synthesis_output/
```

## MODEL_CLIENT_INTEGRATION

```yaml
primary_implementation:
  class: OpenAIChatCompletionClient
  module: autogen_ext.models.openai
  pattern: "All LLM interactions go through model clients"
  
async_requirements:
  creation: |
    model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="sk-xxx")
  cleanup: |
    await model_client.close()  # MANDATORY for async cleanup
    
component_config_system:
  usage: "Generic component configuration for model clients"
  example: |
    config = {
        "provider": "OpenAIChatCompletionClient",
        "config": {
            "model": "gpt-4o",
            "api_key": os.environ["API_KEY"]
        }
    }
    model_client = ChatCompletionClient.load_component(config)
    
wrapper_integration:
  base_url: "http://localhost:8000/v1"
  compatibility: "OpenAI v1 API format"
  model_mapping:
    claude-opus-4-20250514: "gpt-4o equivalent"
    claude-sonnet-4-20250514: "gpt-4o-mini equivalent"
```

## INTEGRATION_ARCHITECTURE

```yaml
data_flow:
  request_chain:
    - source: autogen_application
      protocol: HTTP_POST
      endpoint: http://localhost:8000/v1/chat/completions
      
    - processor: claude_wrapper
      transform: openai_to_claude_format
      auth: OAuth_from_keychain
      
    - destination: claude_api
      protocol: HTTPS
      auth: Bearer_token
      
  response_chain:
    - source: claude_api
      format: claude_response
      
    - processor: message_adapter
      transform: claude_to_openai_format
      
    - destination: autogen_application
      format: OpenAI_ChatCompletionResponse
      
integration_points:
  wrapper_to_sdk:
    module: claude_cli.py
    function: get_claude_client
    auth_source: macOS_Keychain
    
  autogen_to_wrapper:
    client: OpenAIChatCompletionClient
    base_url: http://localhost:8000/v1
    
  hook_to_graphiti:
    trigger: PostToolUse
    condition: next_thought_needed == false
```

## DISTRIBUTED_RUNTIME_ARCHITECTURE

```yaml
agent_worker_protocol:
  phases:
    - initialization: "Worker connects and registers agent types"
    - operation: "Message dispatch and agent activation"
    - termination: "Graceful shutdown and cleanup"
    
  message_flow:
    event_format: CloudEvents
    topic_id: 
      structure: "type:source"
      example: "GitHub_Issues:github.com/repo/issues/123"
    agent_id:
      structure: "type:key"
      example: "code_reviewer:default"
      
service_components:
  worker:
    function: "Hosts agents and client to Gateway"
    protocol: gRPC
    
  gateway:
    function: "RPC bridge between workers and Event Bus"
    responsibilities:
      - message_session_state
      - event_routing
      
  registry:
    function: "Track agent:subscription mappings"
    data: "{agents:agent_types}:{Subscription/Topics}"
    
  agent_state:
    function: "Persistent state for agents"
    
  routing:
    function: "Event delivery based on subscriptions"
    note: "All agents receive all channel messages"
    
backend_options:
  in_memory:
    description: "Same process communication"
    languages: ["python", ".NET"]
    
  distributed_grpc:
    description: "Cross-process communication"
    protocol: gRPC
    serialization: "Protocol Buffers"
    requirement: "Messages serializable as CloudEvents"
    
  microsoft_orleans:
    description: "Distributed actor system"
    features:
      - distributed_state
      - persistent_storage
      - cross_language_communication
```

## TECHNICAL_REQUIREMENTS

```yaml
protocol_buffers:
  requirement: MANDATORY
  purpose: "Message serialization for distributed runtime"
  verification: protoc --version
  
grpc_requirements:
  health_check: "gRPC service health monitoring"
  performance: "Sub-100ms message routing"
  
cloudevents_compliance:
  specification: "https://cloudevents.io/"
  required_fields:
    - type
    - source
    - id
    - time
    - data
```

## VERIFICATION_PROTOCOLS

```yaml
component_verification:
  wrapper_health:
    command: curl -s http://localhost:8000/health
    expected: '{"status":"healthy","service":"claude-code-openai-wrapper"}'
    failure_action: cd wrapper && poetry run uvicorn main:app --reload --port 8000
    
  autogen_basic:
    command: cd autogen && python quickstart.py
    success_indicator: "Success! Your AutoGen Claude integration is working!"
    timeout: 30s
    
  single_agent:
    command: cd autogen && python examples/single_agent_example.py
    expected_output_contains: "key principles of writing clean"
    
  oauth_status:
    command: claude --print "test" 2>&1
    success_indicator: "test"
    failure_indicator: "Error: Not authenticated"
    
  studio_database:
    command: sqlite3 autogen/studio/autogen04202.db ".tables"
    expected_tables: [agents, teams, workflows, sessions]
    
dependency_verification:
  python_version:
    command: python --version
    constraint: ">=3.9.0"
    
  autogen_version:
    command: python -c "import autogen_agentchat; print(autogen_agentchat.__version__)"
    constraint: ">=0.6.4"
    
  autogen_components:
    command: pip show autogen-agentchat autogen-core autogen-ext
    expected: "All three packages installed with matching versions"
    
  grpc_health:
    command: python -c "import grpc; print('gRPC available')"
    expected: "gRPC available"
    
  protobuf_validation:
    command: protoc --version || echo "Protocol Buffers not installed"
    note: "Required for distributed runtime"
    
  critical_imports:
    commands:
      - python -c "from autogen_core import CancellationToken"
      - python -c "from autogen_ext.models.openai import OpenAIChatCompletionClient"
      - python -c "from autogen_core.models import ChatCompletionClient"
```

## ERROR_HANDLING_MATRIX

```yaml
error_conditions:
  wrapper_connection_refused:
    detection: ConnectionError on port 8000
    cause: wrapper_not_running
    recovery:
      - cd wrapper
      - poetry run uvicorn main:app --reload --port 8000
      
  authentication_failure:
    detection: "Error: Not authenticated" in claude_code_sdk
    cause: OAuth_token_expired_or_missing
    recovery:
      - claude auth logout
      - claude auth login
      
  model_not_found:
    detection: KeyError on model name
    cause: incorrect_model_specification
    valid_models:
      - claude-opus-4-20250514
      - claude-sonnet-4-20250514
      
  import_error_cancellation_token:
    detection: ImportError: cannot import name 'CancellationToken'
    cause: autogen_version_mismatch
    recovery:
      - pip install --upgrade 'autogen-agentchat>=0.6.4'
      
  session_timeout:
    detection: asyncio.TimeoutError
    cause: long_running_conversation
    mitigation:
      - increase timeout in config.py
      - implement streaming responses
```

## PERFORMANCE_CONSTRAINTS

```yaml
measured_baselines:
  wrapper_response_time:
    measurement_command: |
      time curl -X POST http://localhost:8000/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{"model": "claude-opus-4-20250514", "messages": [{"role": "user", "content": "test"}]}'
    baseline: 450ms
    acceptable_range: 300-700ms
    
  token_throughput:
    measurement: tokens_per_second
    baseline: 150
    minimum_acceptable: 100
    
  memory_usage:
    measurement_command: ps aux | grep "uvicorn main:app" | awk '{print $6}'
    baseline: 250MB
    maximum_allowed: 500MB
    
  concurrent_sessions:
    maximum_tested: 10
    degradation_point: 15
    failure_point: 20
    
resource_limits:
  cpu_usage:
    wrapper_process: 30%
    autogen_process: 50%
    
  file_descriptors:
    wrapper: 1024
    reason: concurrent_http_connections
    
  port_allocation:
    wrapper: 8000
    studio: 8080
    conflict_resolution: manual_port_change
```

## DEPENDENCY_REQUIREMENTS

```yaml
system_dependencies:
  operating_system:
    required: macOS
    reason: Keychain_OAuth_storage
    version: ">=10.15"
    
  python:
    version: ">=3.9"
    verification: python --version
    
  poetry:
    required_for: wrapper_dependencies
    installation: curl -sSL https://install.python-poetry.org | python3 -
    
package_dependencies:
  wrapper:
    location: /wrapper/pyproject.toml
    key_packages:
      - fastapi==0.68.0
      - uvicorn[standard]
      - claude-code-sdk
      - pydantic>=1.8.0
      
  autogen:
    location: /autogen/requirements.txt
    key_packages:
      - autogen-agentchat>=0.6.4
      - autogen-core>=0.6.4
      - autogen-ext>=0.6.4
      
installation_sequence:
  1: cd wrapper && poetry install
  2: cd autogen && pip install -r requirements.txt
  3: claude auth login
  4: cd wrapper && poetry run uvicorn main:app --port 8000
```

## CONTINUATION_INSTRUCTIONS

```yaml
immediate_tasks:
  complete_multi_agent_examples:
    priority: CRITICAL
    location: /autogen/examples/multi_agent_examples.py
    missing_functions:
      - group_chat_example
      - nested_chat_example
    implementation_pattern: |
      async def group_chat_example():
          model_client = get_model_client()
          agents = [create_agent(name, role) for name, role in agent_specs]
          team = RoundRobinGroupChat(agents, max_rounds=3)
          response = await team.run(task="...")
          
  add_error_recovery:
    priority: HIGH
    location: /autogen/config.py
    requirements:
      - wrapper_reconnection_logic
      - timeout_handling
      - graceful_degradation
      
  create_integration_tests:
    priority: HIGH
    location: /autogen/tests/
    coverage_targets:
      - all_orchestration_patterns
      - error_conditions
      - performance_baselines
      
prerequisite_verification:
  before_starting:
    - curl http://localhost:8000/health
    - claude auth status
    - cd autogen && python quickstart.py
    
continuation_context:
  working_directory: /Users/mac-main/autogen-claude-integration
  active_branch: main
  last_commit: 70cb5b7
  incomplete_features:
    - multi_agent_examples
    - comprehensive_error_handling
    - integration_test_suite
```

## IMPLEMENTATION_STATUS

```yaml
completed_components:
  - component: wrapper
    verification: curl http://localhost:8000/health
    status: OPERATIONAL
    
  - component: single_agent_integration
    verification: python autogen/quickstart.py
    status: OPERATIONAL
    
  - component: oauth_authentication
    verification: claude --print "test"
    status: OPERATIONAL
    
  - component: studio_configuration
    verification: ls autogen/studio/team.json
    status: CONFIGURED
    
  - component: sequential_graphiti_hook
    verification: ls .claude/Hooks/sequential-synthesis-hook.sh
    status: OPERATIONAL
    
incomplete_components:
  - component: multi_agent_patterns
    blocking_issue: missing_implementation
    location: autogen/examples/multi_agent_examples.py
    
  - component: error_recovery
    blocking_issue: no_retry_logic_for_disconnections
    location: autogen/config.py
    
  - component: integration_tests
    blocking_issue: not_created
    location: autogen/tests/
```

## SYSTEM_VERIFICATION_CHECKLIST

```yaml
pre_operation_checks:
  - name: wrapper_health
    command: curl -s http://localhost:8000/health | jq '.status'
    expected: "healthy"
    
  - name: model_availability
    command: curl -s http://localhost:8000/v1/models | jq '.data[0].id'
    expected: "claude-opus-4-20250514"
    
  - name: oauth_authentication
    command: claude --print "authenticated" 2>&1 | grep -q "authenticated" && echo "PASS"
    expected: "PASS"
    
  - name: autogen_imports
    command: python -c "from autogen_core import CancellationToken; print('PASS')"
    expected: "PASS"
    
  - name: studio_database
    command: test -f autogen/studio/autogen04202.db && echo "EXISTS"
    expected: "EXISTS"
    
post_implementation_validation:
  - name: single_agent_test
    command: cd autogen && timeout 30 python examples/single_agent_example.py | grep -q "clean, maintainable code"
    
  - name: wrapper_performance
    command: time curl -X POST http://localhost:8000/v1/chat/completions -d '{...}' 2>&1 | grep real
    constraint: "<0.7s"
    
  - name: memory_check
    command: ps aux | grep uvicorn | awk '{print $6}' | head -1
    constraint: "<500000"
```

END_OF_SPECIFICATION