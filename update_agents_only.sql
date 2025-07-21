-- Update Existing Agents with AutoGen Configuration
-- Generated on 2025-07-21

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

-- Update the newly added agents with proper capabilities
UPDATE agents 
SET capabilities = '["UserProxyAgent", "human_input_mode", "termination_conditions", "intervention_management", "user_interaction"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-8';

UPDATE agents 
SET capabilities = '["error_recovery", "timeout_handling", "reconnection_logic", "health_checks", "system_monitoring"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-9';

UPDATE agents 
SET capabilities = '["CloudEvents", "MessageContext", "publish_subscribe", "event_streaming", "message_analysis"]'
WHERE id = 'worker-swarm-1753072259174-yjdkiusc3-10';

-- Update swarm metadata
UPDATE swarms 
SET updated_at = datetime('now')
WHERE id = 'swarm-1753072259174-yjdkiusc3';