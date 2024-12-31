from typing import Dict
from fastapi.websockets import WebSocket

# Store active WebSocket connections for broadcasting logs
active_connections: Dict[str, WebSocket] = {}

async def broadcast_log(message: str):
    """
    Broadcast a log message to all connected WebSocket clients.
    """
    disconnected_clients = []
    for agent_id, websocket in active_connections.items():
        try:
            await websocket.send_json({"type": "log", "message": message})
        except Exception as e:
            print(f"❌ Failed to send log to Agent '{agent_id}': {e}")
            disconnected_clients.append(agent_id)

    # Remove disconnected clients
    for agent_id in disconnected_clients:
        active_connections.pop(agent_id, None)
