# Agent Framework Knowledge Base

This knowledge base contains documentation about the agent framework used in this project. It provides information about the different agent patterns, implementation details, and best practices.

## Agent Patterns

The framework supports multiple agent patterns that should be selected based on specific use cases:

1. **Single Agent Pattern**: Use for straightforward tasks with minimal complexity (e.g., summarization, Q&A).
2. **Tool Integration Pattern**: Use when agents need to access external data or functions via the `function_tool` decorator.
3. **Agent Routing Pattern**: Use when different query types require specialized handling by creating a router agent.
4. **Agent Handoff Pattern**: Use for complex workflows requiring multiple steps with different expertise areas.
5. **Voice Integration Pattern**: Use when audio input/output is required, implemented with `SingleAgentVoiceWorkflow`.

## OpenAI SDK and Agents SDK

This project uses both the OpenAI SDK and the OpenAI Agents SDK:

- **OpenAI SDK**: Provides access to OpenAI's models and APIs for general AI capabilities.
- **OpenAI Agents SDK**: Extends the OpenAI SDK with specialized functionality for building agent-based applications.

### Version Compatibility

When implementing projects that use OpenAI's APIs, it's important to use a Python version that matches OpenAI's supported versions (3.10/3.11) to avoid dependency compatibility issues, particularly with packages like aiohttp that may not work properly with newer Python versions like 3.12.

## Project Structure

The agent implementation is organized under:

```bash
src/backend/app/custom_agents/
```

This directory is used to implement reusable, composable agent logic based on the patterns described above.
