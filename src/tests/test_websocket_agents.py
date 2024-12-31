import asyncio
import websockets
import json

async def test_agent_websocket():
    uri = "ws://127.0.0.1:8000/ws/agent/agent-123"
    async with websockets.connect(uri) as websocket:
        print("✅ Connected to WebSocket Server as Agent-123")

        # Test Registration
        await websocket.send(json.dumps({
            "action": "register",
            "metadata": {
                "name": "Test Agent",
                "type": "sub-agent",
                "token_stake": 12000,
                "capabilities": ["monitor_cpu", "optimize_gpu"]
            }
        }))
        response = await websocket.recv()
        print(f"📝 Registration Response: {response}")

        # Test Status Update
        await websocket.send(json.dumps({
            "action": "update_status",
            "status": "active"
        }))
        response = await websocket.recv()
        print(f"📝 Status Update Response: {response}")

        # Test Heartbeat
        await websocket.send(json.dumps({
            "action": "heartbeat"
        }))
        response = await websocket.recv()
        print(f"📝 Heartbeat Response: {response}")

# Run the test
asyncio.run(test_agent_websocket())
