
### Agent Patterns

1. **Single Agent Workflow**

    - Used for simple tasks with one agent handling the entire process
    - Example: `hello_world.py` - Basic query-response pattern

2. **Tool Integration**

    - Agents can use function calling to access external tools
    - Example: `tools.py` - Weather and search tools

3. **Agent Routing**

    - Direct queries to specialized agents based on content type
    - Example: `routing.py` - Language and query type routing

4. **Agent Handoffs**

    - Transfer conversations between agents with different capabilities
    - Example: `message_filter.py` - Multi-agent interactions

5. **Voice Integration**
    - Process audio input and generate audio output
    - Example: `voice/static/main.py` - Audio processing workflow
