"""Basic test script for DetomoVanna"""

from src.detomo_vanna import DetomoVanna
import os
import shutil

def test_initialization():
    """Test DetomoVanna initialization"""
    print("Testing DetomoVanna initialization...")

    # Clean up any existing test vectordb
    if os.path.exists("./test_vectordb"):
        shutil.rmtree("./test_vectordb")

    vn = DetomoVanna(config={
        # ChromaDB settings
        "path": "./test_vectordb",
        "client": "persistent",

        # Claude Agent SDK settings
        "agent_endpoint": "http://localhost:8000/generate",
        "model": "claude-sonnet-4-5",
        "temperature": 0.1,
        "max_tokens": 2048
    })

    print("✓ DetomoVanna initialized successfully")

    # Test submit_prompt
    print("\nTesting submit_prompt...")
    response = vn.submit_prompt("Generate SQL to count rows in Customer table")
    print(f"Response: {response}")

    # Clean up
    print("\nCleaning up test files...")
    if os.path.exists("./test_vectordb"):
        shutil.rmtree("./test_vectordb")

    print("\n✓ All tests passed!")

if __name__ == "__main__":
    # Make sure Claude Agent endpoint is running
    import requests
    try:
        r = requests.get("http://localhost:8000/health")
        if r.status_code == 200:
            test_initialization()
        else:
            print("ERROR: Claude Agent endpoint not healthy")
    except Exception as e:
        print("ERROR: Claude Agent endpoint not running on http://localhost:8000")
        print(f"Error: {e}")
        print("Please start it with: python claude_agent_server.py")
