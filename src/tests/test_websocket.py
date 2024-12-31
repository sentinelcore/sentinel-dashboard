import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/logs"
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket Server")
            await websocket.send("Test message")
            response = await websocket.recv()
            print("📝 Received:", response)
    except Exception as e:
        print("❌ WebSocket Error:", e)

        

asyncio.run(test_websocket())
