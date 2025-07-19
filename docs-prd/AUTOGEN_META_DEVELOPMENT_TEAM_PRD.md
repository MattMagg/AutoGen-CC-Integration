# AUTOGEN-NATIVE META-DEVELOPMENT SYSTEM - HIGH-LEVEL SPECIFICATION

SPECIFICATION_TYPE: autogen_system_blueprint
VERSION: 2.0
COMPLIANCE: /Users/mac-main/.claude/CLAUDE.md
VALIDATION: mcp__autogen-docs__fetch_autogen_documentation

## SYSTEM_OBJECTIVE

```yaml
primary_objective:
  description: Build self-improving multi-agent system using AutoGen framework native capabilities
  implementation_principle: Leverage AutoGen native features with minimal custom integration
  validation: grep -r "from autogen" . | wc -l > 50
```

## CORE_PRINCIPLES

```yaml
principles:
  autogen_first:
    mandate: Use AutoGen's built-in features before any custom implementation
    validation: "! grep -r 'custom.*framework' ."
    
  high_level_only:
    mandate: Specify objectives and principles, not implementations
    validation: "! grep -r 'class.*implements' ."
    
  claude_md_compliance:
    mandate: All specifications must be agent-parseable with verification
    validation: grep -r "verification:" . | wc -l > 10
    
  documentation_driven:
    mandate: Use AutoGen MCP for all framework knowledge
    validation: mcp__autogen-docs__search_autogen_documentation query:"latest"
```

## AUTOGEN_NATIVE_FEATURES_TO_LEVERAGE

```yaml
coordination:
  feature: Group Chats (RoundRobinGroupChat, SelectorGroupChat)
  purpose: Multi-agent coordination without custom message buses
  verification: grep -r "GroupChat" .
  
agents:
  feature: Conversable Agents (AssistantAgent, UserProxyAgent)
  purpose: Task execution without custom agent frameworks
  verification: grep -r "AssistantAgent" .
  
memory:
  feature: Conversation History and Message Passing
  purpose: State management without custom memory systems
  verification: grep -r "messages.*history" .
  
tools:
  feature: Native Tool Integration
  purpose: Function calling without custom registries
  verification: grep -r "@tool" .
  
workflows:
  feature: Message-Driven Agent Interactions
  purpose: Workflow execution without custom engines
  verification: grep -r "send.*receive" .
  
prototyping:
  feature: AutoGen Studio
  purpose: Rapid testing without custom validation frameworks
  verification: ls -la autogen_studio/
  
event_driven:
  feature: CloudEvents-based Architecture
  purpose: Standardized event handling without custom protocols
  verification: grep -r "CloudEvents" .
  
distributed:
  feature: Actor Model with gRPC
  purpose: Cross-language agent communication
  verification: grep -r "Microsoft.Orleans\|gRPC" .
```

## SYSTEM_SCOPE

```yaml
in_scope:
  - agents_that_create_other_agents_using_autogen
  - group_chat_based_coordination
  - tool_integration_for_code_generation
  - autogen_studio_for_prototyping
  - parallel_agent_execution_via_task_tool
  - continuous_validation_against_autogen_docs
  
out_of_scope:
  - custom_message_protocols
  - custom_state_management
  - custom_orchestration_frameworks
  - implementation_details
  - human_centric_considerations
```

## MULTI_AGENT_DESIGN_PATTERNS

```yaml
pattern_categories:
  conversational:
    patterns:
      - RoundRobinGroupChat: Sequential turn-taking coordination
      - SelectorGroupChat: Dynamic agent selection based on context
    research_directive: mcp__autogen-docs__search_autogen_documentation query:"GroupChat"
    
  workflow_based:
    patterns:
      - Sequential Workflow: Linear task progression
      - Concurrent Agents: Parallel task execution
      - Handoffs: Explicit control transfer between agents
    research_directive: Agents must research specific implementations via AutoGen MCP
    
  collaborative:
    patterns:
      - Mixture of Agents: Ensemble decision making
      - Multi-Agent Debate: Consensus through discussion
      - Reflection: Self-improvement through introspection
    research_directive: mcp__autogen-docs__search_autogen_documentation query:"collaborative patterns"
    
  advanced_orchestration:
    patterns:
      - Swarm Group Chat: Dynamic agent spawning and coordination
      - Magentic One Group Chat: State-of-the-art implementation example
      - DiGraph Group Chat: Directed graph-based workflows
      - FSM Group Chat: Finite state machine coordination
      - Dynamic Group Chat: Runtime-adaptive agent composition
    research_directive: Study Magentic-One implementation via MCP
    
implementation_note:
  directive: Agents MUST research pattern specifics via AutoGen MCP
  rationale: Patterns evolve with framework updates
  validation: mcp__autogen-docs__fetch_autogen_documentation
```

## AUTOGEN_STUDIO_INTEGRATION

```yaml
studio_capabilities:
  gui_prototyping:
    purpose: No-code agent creation and testing
    command: autogenstudio ui --port 8080 --appdir ./my-app
    verification: ps aux | grep "autogenstudio"
    
  workflow_export:
    purpose: Export GUI-created workflows as code
    research_required: mcp__autogen-docs__search_autogen_documentation query:"workflow export"
    
  visual_debugging:
    purpose: Real-time agent interaction visualization
    benefit: Rapid iteration without code changes
    
  team_composition:
    purpose: Drag-and-drop multi-agent team creation
    validation: Test agent interactions before code generation
    
integration_workflow:
  step_1: Prototype agents in Studio GUI
  step_2: Test multi-agent interactions visually
  step_3: Export working configuration as code
  step_4: Integrate exported code into meta-system
```

## PERFORMANCE_VALIDATION_WITH_AUTOGEN_BENCH

```yaml
benchmarking_framework:
  tool: AutoGen Bench (agbench)
  purpose: Quantitative agent performance evaluation
  
benchmark_suites:
  code_generation:
    benchmark: HumanEval
    purpose: Evaluate code generation capabilities
    research: mcp__autogen-docs__search_autogen_documentation query:"HumanEval agbench"
    
  assistant_capabilities:
    benchmark: AssistantBench
    purpose: General assistant task performance
    research: mcp__autogen-docs__search_autogen_documentation query:"AssistantBench"
    
  custom_benchmarks:
    directive: Create domain-specific benchmarks
    validation: Docker-based consistent execution
    
evaluation_protocol:
  setup:
    command: pip install agbench
    environment: Docker containers for reproducibility
    
  execution:
    frequency: After each major agent iteration
    metrics: Success rate, token efficiency, execution time
    
  continuous_improvement:
    threshold: Maintain >80% on relevant benchmarks
    action: Iterate on underperforming agents
```

## HIGH_LEVEL_AGENT_ROLES

```yaml
agent_categories:
  coordinators:
    purpose: Use AutoGen group chats to coordinate agent teams
    autogen_feature: GroupChat classes
    
  builders:
    purpose: Create new agents using AutoGen's AssistantAgent
    autogen_feature: Conversable agent customization
    
  validators:
    purpose: Ensure compliance with latest AutoGen capabilities
    autogen_feature: Tool integration with MCP
    
  executors:
    purpose: Run parallel tasks using Task tool
    autogen_feature: Async agent execution
```

## RESOURCE_UTILIZATION_DIRECTIVES

```yaml
mcp_usage:
  autogen_docs:
    priority: PRIMARY
    purpose: Single source of truth for AutoGen capabilities
    usage: Continuous validation and knowledge updates
    
  sequential_thinking:
    priority: SECONDARY
    purpose: Complex problem decomposition
    usage: When agents need structured reasoning
    
  graphiti_memory:
    priority: TERTIARY
    purpose: Pattern storage across sessions
    usage: Store successful agent configurations
    
parallel_execution:
  mechanism: Task tool with agent batching
  directive: Maximum parallelization for independent operations
  validation: ps aux | grep -c "python.*agent"
```

## WORKFLOW_PRINCIPLES

```yaml
validation_first:
  step_1: Always check latest AutoGen documentation
  step_2: Validate approach against native capabilities
  step_3: Only then proceed with implementation
  
leverage_native:
  group_chats: For all multi-agent coordination
  message_passing: For all inter-agent communication
  conversation_history: For all state management
  tool_calling: For all external integrations
  event_system: CloudEvents for standardized communication
  studio_first: Prototype in GUI before coding
  
incremental_development:
  start: Minimal working AutoGen agents
  prototype: Use AutoGen Studio for rapid testing
  iterate: Add capabilities using native features
  validate: Test with AutoGen Bench
  export: Convert Studio workflows to code
  
pattern_application:
  research_first: Study native patterns via MCP
  select_pattern: Choose from 13+ native patterns
  implement_native: Use AutoGen's implementation
  avoid_custom: Never recreate provided patterns
```

## VERIFICATION_FRAMEWORK

```yaml
continuous_verification:
  autogen_compliance:
    command: mcp__autogen-docs__search_autogen_documentation query:"AssistantAgent"
    frequency: every_agent_creation
    
  native_feature_usage:
    command: grep -r "autogen\." . | wc -l
    threshold: "> 100"
    
  custom_code_minimization:
    command: "! grep -r 'custom.*framework\\|custom.*protocol' ."
    expected: no_matches
    
  parallel_execution:
    command: ps aux | grep -E "Task.*agent" | wc -l
    expected: "> 5"
    
  studio_validation:
    command: "autogenstudio ui --port 8080 --dry-run"
    expected: successful_startup
    
  benchmark_performance:
    command: "agbench run --suite relevant_benchmarks"
    threshold: "> 80% success rate"
    
  pattern_compliance:
    command: grep -r "RoundRobin\|Selector\|Sequential" .
    expected: using_native_patterns
```

## DOWNSTREAM_AGENT_DIRECTIVES

```yaml
for_all_agents:
  primary_directive: Use AutoGen native features for ALL functionality
  validation_source: mcp__autogen-docs
  implementation_guidance: Let AutoGen handle coordination, memory, and workflows
  pattern_usage: Select from 13+ native design patterns
  
research_mandate:
  before_implementation: Research AutoGen capabilities via MCP
  pattern_selection: Study all 13 design patterns before choosing
  during_implementation: Validate against latest docs
  after_implementation: Test with AutoGen Studio AND Bench
  
prohibited_actions:
  - creating_custom_message_buses
  - implementing_custom_state_management
  - building_custom_coordination_layers
  - writing_framework_code_that_autogen_provides
  - reimplementing_any_of_13_native_patterns
  - creating_custom_event_systems_over_cloudevents
  - building_gui_tools_over_autogen_studio
  
mandatory_practices:
  - prototype_in_autogen_studio_first
  - benchmark_with_agbench_regularly
  - use_native_patterns_exclusively
  - leverage_cloudevents_architecture
```

## BOOTSTRAP_PROCESS

```yaml
initialization:
  step_1:
    action: Validate AutoGen installation
    command: pip show autogen-agentchat autogen-core autogen-ext
    
  step_2:
    action: Create first coordinator using GroupChat
    validation: python -c "from autogen import GroupChat"
    
  step_3:
    action: Spawn builders using AssistantAgent
    validation: python -c "from autogen import AssistantAgent"
    
  step_4:
    action: Begin continuous improvement loop
    validation: Check agent creation rate
```

## SUCCESS_METRICS

```yaml
metrics:
  autogen_feature_coverage:
    target: Maximum utilization of native AutoGen capabilities
    measurement: Verified use of framework features over custom implementations
    
  agent_creation_velocity:
    target: New agents created using native features
    measurement: git log --grep="AssistantAgent"
    
  parallel_efficiency:
    target: Multiple agents via Task tool
    measurement: concurrent process count
    
  documentation_compliance:
    target: 100% validated against latest docs
    measurement: MCP validation success rate
    
  pattern_utilization:
    target: 100% native pattern usage
    measurement: grep -c "custom.*pattern" should be 0
    
  studio_adoption:
    target: All agents prototyped in Studio first
    measurement: studio export files in repo
    
  benchmark_performance:
    target: >80% on relevant benchmarks
    measurement: agbench result tracking
    
  event_architecture:
    target: 100% CloudEvents compliance
    measurement: grep -r "CloudEvents" | wc -l
```

## NATIVE_ARCHITECTURE_ALIGNMENT

```yaml
event_driven_foundation:
  architecture: CloudEvents publish-subscribe model
  benefit: Industry-standard event handling
  research: mcp__autogen-docs__search_autogen_documentation query:"CloudEvents"
  
actor_model:
  framework: Microsoft Orleans for distributed agents
  benefit: Cross-language agent communication
  languages: Python and .NET seamless integration
  
runtime_options:
  in_memory: Single process for development
  distributed: Multi-process with gRPC for production
  selection: Based on scale requirements
```

END_OF_SPECIFICATION

CRITICAL_NOTE: This PRD provides HIGH-LEVEL objectives and principles only. Downstream agents must use mcp__autogen-docs to research specific implementations. The PRD intentionally avoids implementation details to empower agents to leverage AutoGen's full capabilities through proper research.

ENHANCED_FOR_V0.6.X: This specification now includes:
- All 13+ multi-agent design patterns (research specifics via MCP)
- AutoGen Studio integration for no-code prototyping
- AutoGen Bench for performance validation
- CloudEvents architecture alignment
- Distributed agent capabilities with Orleans
- Magentic-One as reference implementation