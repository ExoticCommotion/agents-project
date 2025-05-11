"""
Tool Integration Pattern Example

This module demonstrates how to create an agent that can use tools
via the function_tool decorator from the OpenAI Agents SDK.
"""

import asyncio

from agents import Agent, Runner, function_tool
from pydantic import BaseModel


class Weather(BaseModel):
    """Weather information model."""

    location: str
    temperature: int
    unit: str
    forecast: list[str]


class TimeInfo(BaseModel):
    """Time information model."""

    timezone: str
    time: str
    date: str


@function_tool
def get_current_weather(location: str, unit: str = "celsius") -> Weather:
    """
    Get the current weather in a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: The temperature unit to use. Either "celsius" or "fahrenheit".

    Returns:
        A Weather object containing the weather information.
    """
    print(f"[debug] Getting weather for {location} in {unit}")  # pragma: no cover
    return Weather(
        location=location,
        temperature=22 if unit == "celsius" else 72,
        unit=unit,
        forecast=["sunny", "windy"],
    )


@function_tool
def get_current_time(timezone: str = "UTC") -> TimeInfo:
    """
    Get the current time in a given timezone.

    Args:
        timezone: The timezone to get the time for, e.g. "UTC", "America/New_York"

    Returns:
        A TimeInfo object containing the current time information.
    """
    print(f"[debug] Getting time for timezone {timezone}")  # pragma: no cover
    return TimeInfo(timezone=timezone, time="12:00 PM", date="2025-05-11")


def create_tool_using_agent() -> Agent:
    """
    Create an agent that can use tools to perform tasks.

    Returns:
        A configured Agent instance with tools.
    """
    return Agent(
        name="ToolUsingAgent",
        instructions="You are a helpful assistant with access to tools for checking weather and time.",
        tools=[get_current_weather, get_current_time],
    )


async def run_tool_using_agent(user_input: str) -> str:
    """
    Run the tool-using agent with the given user input.

    Args:
        user_input: The user's message.

    Returns:
        The agent's response.
    """
    agent = create_tool_using_agent()
    result = await Runner.run(agent, input=user_input)
    return str(result.final_output)


def run_tool_using_sync(user_input: str) -> str:
    """
    Run the tool-using agent synchronously with the given user input.

    Args:
        user_input: The user's message.

    Returns:
        The agent's response.
    """
    return str(Runner.run_sync(create_tool_using_agent(), input=user_input).final_output)


async def main() -> None:  # pragma: no cover
    """Run the tool-using agent with sample inputs."""
    response1 = await run_tool_using_agent("What's the weather in San Francisco?")
    print(f"Weather response: {response1}")

    response2 = await run_tool_using_agent("What time is it in New York?")
    print(f"Time response: {response2}")

    sync_response = run_tool_using_sync("What's the current time?")
    print(f"Sync response: {sync_response}")


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
