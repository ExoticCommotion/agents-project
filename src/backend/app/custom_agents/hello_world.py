"""
Single Agent Pattern Example

This module demonstrates a simple single agent pattern implementation
using the OpenAI Agents SDK.
"""

from openai import OpenAI
from openai_agents import Agent, AgentState, Message, SingleAgentWorkflow  # type: ignore

client = OpenAI()


class HelloWorldAgent(Agent):  # type: ignore
    """A simple hello world agent that responds to user messages."""

    def __init__(self) -> None:
        """Initialize the HelloWorldAgent."""
        super().__init__()

    async def run(self, state: AgentState) -> AgentState:
        """
        Process the user's message and generate a response.

        Args:
            state: The current state of the agent conversation.

        Returns:
            The updated agent state with the agent's response.
        """
        latest_message = state.messages[-1]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": latest_message.content},
            ],
        )

        state.messages.append(
            Message(role="assistant", content=response.choices[0].message.content)
        )

        return state


def create_hello_world_workflow() -> SingleAgentWorkflow:
    """
    Create a single agent workflow with the HelloWorldAgent.

    Returns:
        A configured SingleAgentWorkflow instance.
    """
    agent = HelloWorldAgent()
    return SingleAgentWorkflow(agent=agent)
