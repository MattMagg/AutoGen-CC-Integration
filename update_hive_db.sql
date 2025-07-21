-- Update Hive-Mind Database for AutoGen Configuration
-- Generated on 2025-07-21

-- First, let's add new agents to reach 12 total (currently have 9 including queen)
-- We need to add 3 more specialized agents

INSERT INTO agents (id, swarm_id, name, type, role, capabilities, status)
VALUES 
  ('worker-swarm-1753072259174-yjdkiusc3-8', 'swarm-1753072259174-yjdkiusc3', 'Human Loop Handler', 'specialist', 'worker', '["UserProxyAgent", "human_input_mode", "termination_conditions", "intervention_management"]', 'active'),
  ('worker-swarm-1753072259174-yjdkiusc3-9', 'swarm-1753072259174-yjdkiusc3', 'Health Monitor', 'monitor', 'worker', '["error_recovery", "timeout_handling", "reconnection_logic", "health_checks"]', 'active'),
  ('worker-swarm-1753072259174-yjdkiusc3-10', 'swarm-1753072259174-yjdkiusc3', 'Message Flow Analyst', 'analyst', 'worker', '["CloudEvents", "MessageContext", "publish_subscribe", "event_streaming"]', 'active');

-- Now update existing agents with AutoGen-specific capabilities

-- Update Queen Coordinator
UPDATE agents 
SET capabilities = '["orchestration", "delegation", "consensus", "swarm_management", "task_distribution", "adaptive_learning"]'
WHERE id = 'queen-swarm-1753072259174-yjdkiusc3';

-- Update Researcher Worker 1 to Runtime Orchestrator
UPDATE agents 
SET name = 'Runtime Orchestrator',
    type = 'architect',
    capabilities = '["SingleThreadedAgentRuntime", "GrpcWorkerAgentRuntime", "runtime_management", "process_orchestration"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-0';

-- Update Coder Worker 2 to Routing Specialist
UPDATE agents 
SET name = 'Routing Specialist',
    capabilities = '["RoutedAgent", "TypeSubscription", "TopicPubSub", "message_routing", "event_handling"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-1';

-- Update Analyst Worker 3 to Chat Orchestrator
UPDATE agents 
SET name = 'Chat Orchestrator',
    type = 'architect',
    capabilities = '["RoundRobinGroupChat", "SelectorGroupChat", "Swarm", "conversation_management", "agent_selection"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-2';

-- Update Tester Worker 4 to Integration Tester
UPDATE agents 
SET name = 'Integration Tester',
    capabilities = '["runtime_testing", "message_validation", "handoff_verification", "integration_testing", "e2e_testing"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-3';

-- Update Architect Worker 5 to Tool Builder
UPDATE agents 
SET name = 'Tool Builder',
    type = 'coder',
    capabilities = '["FunctionTool", "BaseTool", "tool_decorator", "custom_tool_creation", "tool_integration"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-4';

-- Update Reviewer Worker 6 to Agent Factory
UPDATE agents 
SET name = 'Agent Factory',
    type = 'coder',
    capabilities = '["AssistantAgent", "ConversableAgent", "UserProxyAgent", "agent_creation", "agent_configuration"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-5';

-- Update Optimizer Worker 7 to Performance Tuner
UPDATE agents 
SET name = 'Performance Tuner',
    capabilities = '["async_operations", "batch_processing", "token_optimization", "latency_reduction", "throughput_optimization"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-6';

-- Update Documenter Worker 8 to Knowledge Keeper
UPDATE agents 
SET name = 'Knowledge Keeper',
    capabilities = '["memory_persistence", "context_management", "session_tracking", "knowledge_graph", "information_retrieval"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-7';

-- Add configuration to collective_memory table
INSERT INTO collective_memory (id, swarm_id, key, value, type, created_at)
VALUES 
  ('config-autogen-' || hex(randomblob(8)), 'swarm-1753072259174-yjdkiusc3', 'autogen_config', '{"framework": "Microsoft AutoGen v0.6.X", "wrapperUrl": "http://localhost:8000", "models": ["claude-opus-4-20250514", "claude-sonnet-4-20250514"], "runtime": "SingleThreadedAgentRuntime", "patterns": ["RoundRobinGroupChat", "SelectorGroupChat", "Swarm"], "routing": "TypeSubscription"}', 'configuration', datetime('now')),
  ('config-human-' || hex(randomblob(8)), 'swarm-1753072259174-yjdkiusc3', 'human_in_loop_config', '{"enabled": true, "humanInputMode": "ALWAYS", "maxConsecutiveAutoReply": 5, "terminationConditions": {"keywords": ["TERMINATE", "EXIT", "STOP"], "maxIterations": 50, "timeLimit": 3600}, "interventionPoints": ["task_planning", "code_review", "deployment_approval"], "streamingEnabled": true}', 'configuration', datetime('now')),
  ('config-memory-' || hex(randomblob(8)), 'swarm-1753072259174-yjdkiusc3', 'memory_persistence_config', '{"enabled": true, "sessionTracking": true, "contextTypes": ["short_term", "mid_term", "long_term"], "retentionPolicy": {"short_term": "1_day", "mid_term": "7_days", "long_term": "permanent"}, "features": {"crossSessionContext": true, "contextTimeline": true, "autoSave": true, "compression": true}}', 'configuration', datetime('now')),
  ('pattern-roundrobin-' || hex(randomblob(8)), 'swarm-1753072259174-yjdkiusc3', 'roundrobin_pattern', '{"type": "RoundRobinGroupChat", "agents": ["Runtime Orchestrator", "Agent Factory", "Tool Builder", "Integration Tester"], "maxRounds": 10, "implementation": {"baseClass": "GroupChat", "selectionMethod": "round_robin", "messageProtocol": "CloudEvents"}}', 'pattern', datetime('now')),
  ('pattern-selector-' || hex(randomblob(8)), 'swarm-1753072259174-yjdkiusc3', 'selector_pattern', '{"type": "SelectorGroupChat", "agents": ["Chat Orchestrator", "Message Flow Analyst", "Routing Specialist"], "selectionCriteria": "task_requirements", "implementation": {"baseClass": "GroupChat", "selectionMethod": "llm_based", "contextWindow": 2048}}', 'pattern', datetime('now')),
  ('pattern-swarm-' || hex(randomblob(8)), 'swarm-1753072259174-yjdkiusc3', 'swarm_pattern', '{"type": "Swarm", "agents": ["Queen Coordinator", "Runtime Orchestrator", "Chat Orchestrator"], "handoffProtocol": "TypeSubscription", "implementation": {"baseClass": "SwarmAgent", "handoffMethod": "on_condition", "stateManagement": "distributed"}}', 'pattern', datetime('now')),
  ('pattern-routing-' || hex(randomblob(8)), 'swarm-1753072259174-yjdkiusc3', 'routing_pattern', '{"type": "TypeSubscription", "topics": ["agent_coordination", "task_execution", "error_handling", "human_input"], "implementation": {"baseClass": "RoutedAgent", "decorator": "@message_handler", "pubsubModel": "CloudEvents"}}', 'pattern', datetime('now'));

-- Update swarm metadata
UPDATE swarms 
SET updated_at = datetime('now')
WHERE id = 'swarm-1753072259174-yjdkiusc3';

-- Add session configuration
INSERT INTO sessions (id, swarm_id, swarm_name, objective, status, created_at, parent_pid, child_pids)
VALUES 
  ('session-autogen-config-' || strftime('%s', 'now'), 'swarm-1753072259174-yjdkiusc3', 'Autogen-Swarm-General-1', 'AutoGen multi-agent system configuration', 'configured', datetime('now'), NULL, '[]')
ON CONFLICT(id) DO NOTHING;