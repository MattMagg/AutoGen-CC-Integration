# CORRECTED PROJECT SCOPE

## PRIMARY OBJECTIVE (from CLAUDE.md)
To build and manage a multi-agent system using the **Microsoft AutoGen framework's native capabilities exclusively**. The system's purpose is to create and continuously refine a multi-agent orchestration system capable of real-time collaboration, communication, and delegation between agents. It must support human-in-the-loop, allowing user interjection and collaboration, facilitated by streaming agent thoughts and responses. The system will also have full memory persistence for short, mid, and long-term context. This includes maintaining context within and between sessions, retrieving context from specific sessions, and building a contextual timeline for overall memory.

## Foundation-First Development Philosophy
- **MINIMALISM**: Start with the smallest possible, verifiable implementation.
- **INCREMENTALISM**: Build upon existing, proven foundations. Add one verified layer at a time.
- **VERIFICATION**: Every change must be proven with executable commands. No theoretical success.
- **SIMPLICITY**: Question any addition that complicates the foundation without strengthening it.

## Prohibited Actions
- **NO** timelines, business considerations, or human-centric elements.
- **NO** claims of "production-ready" or "enterprise-grade."
- **NO** custom frameworks, message buses, or state management systems. Use AutoGen native features.
- **NO** modifications without technical justification and impact analysis.
- **NO** debugging artifacts in final implementations.

## Mandatory Requirements
- **ALWAYS** execute verification commands to prove implementation success
- **ALWAYS** show the exact command and its output, including the exit code (`echo $?`)
- **NEVER** claim success without executable proof
- **FAILURE HANDLING**: If a failure occurs, display the exact error, analyze the root cause, form a testable hypothesis, and execute diagnostic commands

## Reality Check Protocol
Before ANY implementation, answer with evidence:
1. Is the current implementation actually broken? (Verify with commands)
2. Will this change make the system simpler or more complex?
3. Can I demonstrate this working with real execution?
4. Am I adding this because it's needed or because I can?
5. Have I verified this works in isolation before integrating?

**If you cannot answer these convincingly with evidence, DO NOT PROCEED.**

## Current State Focus
**EARLY STAGE** - Focus on:
- Verifying what currently works
- Building incrementally on proven foundations  
- Executable verification at each step
- Minimal, working implementations first

## Anti-Patterns to Avoid
- Claims without executable verification
- Theoretical solutions without implementation
- Code modification without impact analysis
- Unnecessary "improvements"
- Complex solutions when simple ones suffice
- Adding features before core functionality is solid