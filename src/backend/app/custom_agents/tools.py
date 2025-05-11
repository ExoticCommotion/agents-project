"""
Tool Integration Pattern Example

This module demonstrates how to create an agent that can use tools
via the function_tool decorator from the OpenAI Agents SDK.
"""

from typing import Any

from openai import OpenAI
from openai_agents import (  # type: ignore
    Agent,
    AgentState,
    Message,
    SingleAgentWorkflow,
    function_tool,
)

client = OpenAI()


class ToolUsingAgent(Agent):  # type: ignore
    """An agent that can use tools to perform tasks."""

    def __init__(self) -> None:
        """Initialize the ToolUsingAgent."""
        super().__init__()

    @function_tool  # type: ignore
    def get_current_weather(self, location: str, unit: str = "celsius") -> dict[str, Any]:
        """
        Get the current weather in a given location.

        Args:
            location: The city and state, e.g. San Francisco, CA
            unit: The temperature unit to use. Either "celsius" or "fahrenheit".

        Returns:
            A dictionary containing the weather information.
        """
        return {
            "location": location,
            "temperature": 22 if unit == "celsius" else 72,
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }

    @function_tool  # type: ignore
    def get_current_time(self, timezone: str = "UTC") -> dict[str, str]:
        """
        Get the current time in a given timezone.

        Args:
            timezone: The timezone to get the time for, e.g. "UTC", "America/New_York"

        Returns:
            A dictionary containing the current time information.
        """
        return {"timezone": timezone, "time": "12:00 PM", "date": "2025-05-11"}

    async def run(self, state: AgentState) -> AgentState:
        """
        Process the user's message and generate a response, potentially using tools.

        Args:
            state: The current state of the agent conversation.

        Returns:
            The updated agent state with the agent's response.
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant with access to tools."}
        ]

        for msg in state.messages:
            messages.append({"role": msg.role, "content": msg.content})

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use",
                            },
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Get the current time in a given timezone",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "description": "The timezone to get the time for",
                            }
                        },
                        "required": [],
                    },
                },
            },
        ]

        api_messages = []
        for msg in messages:
            api_messages.append({"role": msg["role"], "content": msg["content"]})

        response = client.chat.completions.create(  # type: ignore
            model="gpt-4o", messages=api_messages, tools=tools, tool_choice="auto"
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments

                if function_name == "get_current_weather":
                    import json

                    args = json.loads(function_args)
                    function_response = self.get_current_weather(**args)
                elif function_name == "get_current_time":
                    import json

                    args = json.loads(function_args)
                    function_response = self.get_current_time(**args)

                messages.append(
                    {
                        "role": "assistant",
                        "content": f"Using {function_name} with arguments {function_args}",
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(function_response),
                    }
                )

            second_api_messages = []
            for msg in messages:
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    second_api_messages.append({"role": msg["role"], "content": msg["content"]})

            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=second_api_messages,  # type: ignore
            )

            state.messages.append(
                Message(role="assistant", content=second_response.choices[0].message.content)
            )
        else:
            state.messages.append(Message(role="assistant", content=response_message.content))

        return state


def create_tool_using_workflow() -> SingleAgentWorkflow:
    """
    Create a single agent workflow with the ToolUsingAgent.

    Returns:
        A configured SingleAgentWorkflow instance.
    """
    agent = ToolUsingAgent()
    return SingleAgentWorkflow(agent=agent)
