"""
SDK Worker - Runs Claude Agent SDK in a dedicated process
This script is called by the main server to execute SDK queries
"""
import asyncio
import sys
import json
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock


async def run_query(prompt: str, model: str):
    """Run a single query using Claude Agent SDK"""

    system_prompt = """You are a SQL expert. Generate accurate SQL queries based on the given context.

Rules:
- Generate ONLY the SQL query, no explanation
- Use proper SQL syntax
- Follow the database schema provided in the prompt
- Use similar examples as reference when provided"""

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        model=model,
        max_turns=1,
        permission_mode="bypassPermissions"
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)

        response_text = ""
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

        return response_text.strip()


if __name__ == "__main__":

    prompt = "Hello"
    model = "claude-haiku-4-5-20251001"

    # Run async query
    result = asyncio.run(run_query(prompt, model))

    # Output result as JSON
    output = {
        "text": result,
        "model": model
    }
    print(json.dumps(output))
