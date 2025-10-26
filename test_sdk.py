import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def test_sdk():
    """Test basic Claude Agent SDK functionality"""

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant.",
        model="claude-sonnet-4-5-20250929",
        max_turns=1,
        permission_mode="bypassPermissions"
    )

    print("Initializing Claude SDK Client...")

    try:
        async with ClaudeSDKClient(options=options) as client:
            print("Client initialized successfully!")

            prompt = "Say hello in one word"
            print(f"Sending query: {prompt}")

            await client.query(prompt)

            print("Waiting for response...")
            async for message in client.receive_response():
                print(f"Received message type: {type(message)}")
                print(f"Message: {message}")

        print("Test completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sdk())
