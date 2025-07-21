# Real-Time Multi-Agent Orchestration System - Project Overview

## Primary Purpose (from CLAUDE.md)
To build and manage a multi-agent system using the **Microsoft AutoGen framework's native capabilities exclusively**. The system's purpose is to create and continuously refine a multi-agent orchestration system capable of real-time collaboration, communication, and delegation between agents. It must support human-in-the-loop, allowing user interjection and collaboration, facilitated by streaming agent thoughts and responses. The system will also have full memory persistence for short, mid, and long-term context. This includes maintaining context within and between sessions, retrieving context from specific sessions, and building a contextual timeline for overall memory.

## Core Objectives
- **Real-time streaming multi-agent orchestration** with event-driven architecture
- **Human-in-the-loop support** for user interjection and collaboration
- **AutoGen-first approach** - leverage native features exclusively, avoid custom frameworks
- **Memory persistence** - short, mid, and long-term context maintenance
- **CloudEvents-based architecture** for industry-standard event handling
- **Continuous validation** against latest AutoGen documentation via MCP

## Key Components
1. **Claude Wrapper** - OpenAI API-compatible FastAPI service for Claude models
2. **AutoGen Integration** - Multi-agent coordination using native GroupChat patterns
3. **AutoGen Studio** - No-code GUI for agent prototyping and testing
4. **AutoGen Bench** - Performance validation and benchmarking
5. **Sequential-Graphiti Integration** - Knowledge capture and memory synthesis

## Current State
- **Wrapper**: OPERATIONAL (port 8000)
- **Single-agent integration**: OPERATIONAL
- **OAuth authentication**: OPERATIONAL
- **Multi-agent patterns**: PARTIALLY_IMPLEMENTED (sequential working, group/nested incomplete)
- **Studio integration**: CONFIGURED
- **Benchmarking**: PLANNED

## Architecture Pattern
Event-driven publish-subscribe model based on CloudEvents specification, using AutoGen's native coordination patterns (RoundRobinGroupChat, SelectorGroupChat) rather than custom message buses. All LLM interactions must go through the OpenAIChatCompletionClient.