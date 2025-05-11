"""
Single Agent Pattern Example

This module demonstrates a simple single agent pattern implementation
using the OpenAI Agents SDK.
"""

import asyncio

from agents import Agent, Runner


def create_hello_world_agent() -> Agent:
    """
    Create a simple hello world agent that responds to user messages.

    Returns:
        A configured Agent instance.
    """
    return Agent(
        name="HelloWorld",
        instructions="You are a helpful assistant. You only respond in haikus.",
    )


async def run_hello_world_agent(user_input: str) -> str:
    """
    Run the hello world agent with the given user input.

    Args:
        user_input: The user's message.

    Returns:
        The agent's response.
    """
    agent = create_hello_world_agent()
    result = await Runner.run(agent, input=user_input)
    return str(result.final_output)


def run_hello_world_sync(user_input: str) -> str:
    """
    Run the hello world agent synchronously with the given user input.

    Args:
        user_input: The user's message.

    Returns:
        The agent's response.
    """
    return str(Runner.run_sync(create_hello_world_agent(), input=user_input).final_output)


async def main() -> None:  # pragma: no cover
    """Run the hello world agent with a sample input."""
    response = await run_hello_world_agent("Tell me about artificial intelligence.")
    print(response)

    sync_response = run_hello_world_sync("Tell me about Python.")
    print(sync_response)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
