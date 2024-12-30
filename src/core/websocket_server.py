from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List

app = FastAPI(title="Sentinel WebSocket Server", version="0.1.0")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected clients
connected_clients: List[WebSocket] = []

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("🔌 Client disconnected")

# Function to broadcast logs to all connected clients
async def broadcast_log(message: str):
    for client in connected_clients:
        try:
            await client.send_text(message)
        except Exception as e:
            print(f"❌ Failed to send log: {e}")
            connected_clients.remove(client)

# Example: Simulating log messages every few seconds
async def generate_logs():
    counter = 1
    while True:
        log_message = f"📝 Log Entry {counter}: Simulated log message."
        await broadcast_log(log_message)
        print(log_message)  # Print to the server console
        counter += 1
        await asyncio.sleep(5)  # Broadcast every 5 seconds

# Start the log generation
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_logs())


@app.get("/tests")
def test_route():
    return {"message": "✅ API is working!"}
