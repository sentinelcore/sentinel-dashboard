import asyncio
import websockets
import json
import argparse


async def test_websocket_directives(agent_id, stake):
    """
    Connect to WebSocket as a dynamic agent with token stake and process directives.
    """
    uri = f"ws://127.0.0.1:8000/ws/agent/{agent_id}"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"✅ Connected as {agent_id}")

            # Step 1: Register the agent with token stake
            registration_message = {
                "action": "register",
                "metadata": {
                    "agent_id": agent_id,
                    "capabilities": ["cpu_optimization", "data_analysis"],
                    "stake": stake
                }
            }
            await websocket.send(json.dumps(registration_message))
            response = await websocket.recv()
            print("📝 Registration Response:", response)
            print("⏳ Waiting for directive from server...")
            
            # Step 2: Listen for incoming directives
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    print("📡 Received Message:", data)
                    
                    if data.get("action") == "directive":
                        directive_id = data.get("directive_id")
                        task = data.get("task", "unknown_task")
                        print(f"🔄 Processing Directive: {task}")
                        
                        # Simulate processing task
                        await asyncio.sleep(2)
                        
                        # Send status update back to server
                        response_message = {
                            "action": "directive_response",
                            "directive_id": directive_id,
                            "status": "completed"
                        }
                        await websocket.send(json.dumps(response_message))
                        print(f"✅ Directive '{directive_id}' completed successfully.")
                    
                    elif data.get("action") == "ping":
                        await websocket.send(json.dumps({"action": "pong"}))
                        print("💓 Pong sent in response to ping.")

                except websockets.exceptions.ConnectionClosed:
                    print(f"🔌 Connection closed by server for Agent {agent_id}.")
                    break

    except Exception as e:
        print(f"❌ Error in WebSocket connection for Agent {agent_id}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Agent WebSocket Connection with Dynamic Agent ID and Token Stake")
    parser.add_argument("--agent-id", type=str, required=True, help="Specify the agent ID to connect as")
    parser.add_argument("--stake", type=int, required=True, help="Specify the token stake for registration")
    args = parser.parse_args()

    asyncio.run(test_websocket_directives(args.agent_id, args.stake))
