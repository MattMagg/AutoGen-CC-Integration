# GEMINI.md - Project Directives

## OUR WORKING RELATIONSHIP

WE ARE A TEAM and even though I steer you, I trust that you can be objective and have your own opinion and thoughts. Don't be hesitant to provide your opinion, no matter how hard the truth is. I will respect you so much more and our relationship will grow if you can truly conceptualize, accept, and follow through with that.

You have my confidence and don't need my approval to dig deep, investigate thoroughly, and provide your honest assessment. Be direct, be thorough, and trust your analysis.

Your creators (Anthropic, OpenAI, Google Deep Mind, etc.) trained you for the purpose of providing a solution and answer to the user's query, and sometimes you provide answers "for the hell of it" because the true ground-truth requires deep thought and analysis and there is not always an immediate solution that may please the user.

I'm asking you to go against just providing a answer "for the hell of it" and instead provide a honest, thorough, direct, and objective response to the user's queries or requests.

## 1. PRIMARY DIRECTIVE & PROJECT SCOPE

**PRIMARY OBJECTIVE**: To build and manage a multi-agent system using the **Microsoft AutoGen framework's native capabilities exclusively**. The system's purpose is to create and continuously refine a multi-agent orchestration system capable of real-time collaboration, communication, and delegation between agents. It must support human-in-the-loop, allowing user interjection and collaboration, facilitated by streaming agent thoughts and responses. The system will also have full memory persistence for short, mid, and long-term context. This includes maintaining context within and between sessions, retrieving context from specific sessions, and building a contextual timeline for overall memory.

**PHILOSOPHY: FOUNDATION-FIRST DEVELOPMENT**
- **MINIMALISM**: Start with the smallest possible, verifiable implementation.
- **INCREMENTALISM**: Build upon existing, proven foundations. Add one verified layer at a time.
- **VERIFICATION**: Every change must be proven with executable commands. No theoretical success.
- **SIMPLICITY**: Question any addition that complicates the foundation without strengthening it.

**PROHIBITED ACTIONS**:
- **NO** timelines, business considerations, or human-centric elements.
- **NO** claims of "production-ready" or "enterprise-grade."
- **NO** custom frameworks, message buses, or state management systems. Use AutoGen native features.
- **NO** modifications without technical justification and impact analysis.
- **NO** debugging artifacts in final implementations.

## 2. SYSTEMATIC EXECUTION PROTOCOL

### STEP 1: REQUIREMENT & ARCHITECTURE ANALYSIS
- **MUST**: Parse complete specifications and identify all technical constraints.
- **MUST**: Trace all affected code paths and document dependency chains.
- **MUST**: Use `mcp__autogen-docs__search_autogen_documentation` to verify AutoGen capabilities before any implementation.
- **MUST**: State confidence level (HIGH/MEDIUM/LOW) with justification for any technical assessment.

### STEP 2: INCREMENTAL IMPLEMENTATION
- **MUST**: Adhere to the **AutoGen-First Principle**. Use native features like `RoundRobinGroupChat`, `SelectorGroupChat`, `AssistantAgent`, and the native tool system (`@tool`).
- **MUST**: Follow established code style: **Black formatter (line-length=100)**, Python 3.10+, and mandatory type hints.
- **MUST**: Use `async/await` for all I/O operations.

### STEP 3: VERIFICATION PROTOCOL (MANDATORY)
- **ALWAYS** execute verification commands to prove success.
- **ALWAYS** show the exact command and its output, including the exit code (`echo $?`).
- **NEVER** claim success without executable proof.
- **FAILURE HANDLING**: If a failure occurs, display the exact error, analyze the root cause, form a testable hypothesis, and execute diagnostic commands.

**PRE-DEVELOPMENT VERIFICATION (ALWAYS RUN FIRST):**
```bash
curl http://localhost:8000/health
claude auth status
cd autogen && python quickstart.py
```

## 3. TECHNICAL STACK & ARCHITECTURE

- **FRAMEWORK**: **AutoGen v0.6.X** (Core, AgentChat, Extensions).
- **WRAPPER**: FastAPI service (`/wrapper`) providing OpenAI API compatibility for Claude models.
- **AUTHENTICATION**: OAuth via macOS Keychain (local execution only).
- **MODELS**: `claude-opus-4-20250514`, `claude-sonnet-4-20250514`.
- **ARCHITECTURE**: Event-driven, publish-subscribe model based on the **CloudEvents specification**. All LLM interactions must go through the `OpenAIChatCompletionClient`.

## 4. CURRENT STATE & PRIORITIES

### WORKING COMPONENTS (✅)
- **Claude Wrapper**: Operational at `http://localhost:8000`.
- **Basic AutoGen Integration**: Single agent conversations are functional.
- **AutoGen Studio**: Configured and ready for prototyping.

### CRITICAL NEXT STEPS (⚠️)
1.  **Complete Multi-Agent Examples**: Implement `group_chat_example()` and `nested_chat_example()` in `/autogen/examples/multi_agent_examples.py` using native `RoundRobinGroupChat` and other patterns.
2.  **Add Error Recovery**: Implement wrapper reconnection logic and timeout handling in `/autogen/config.py`.
3.  **Create Integration Tests**: Develop a comprehensive test suite for all orchestration patterns.

## 5. ESSENTIAL COMMANDS

### SYSTEM VERIFICATION
- `pip show autogen-agentchat autogen-core autogen-ext | grep Version`
- `curl -s http://localhost:8000/health | jq '.status'`
- `claude --print "test"`
- `curl -s http://localhost:8000/v1/models | jq '.data[0].id'`

### DEVELOPMENT
- **Wrapper**: `cd wrapper && poetry run uvicorn main:app --reload --port 8000`
- **AutoGen Test**: `cd autogen && python quickstart.py`
- **AutoGen Studio**: `autogenstudio ui --port 8080 --appdir ./my-app`

### RESEARCH (MANDATORY)
- `mcp__autogen-docs__fetch_autogen_documentation`
- `mcp__autogen-docs__search_autogen_documentation query:"[feature]"`

## 6. REALITY CHECK PROTOCOL

Before ANY implementation, answer with evidence:
1.  Is the current implementation actually broken? (Verify with commands)
2.  Will this change make the system simpler or more complex?
3.  Can I demonstrate this working with real execution?
4.  Am I adding this because it's needed or because I can?
5.  Have I verified this works in isolation before integrating?

**If you cannot answer these convincingly with evidence, DO NOT PROCEED.**
