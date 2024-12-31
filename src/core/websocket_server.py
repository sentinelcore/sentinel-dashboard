from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
import asyncio
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
from core.agent_manager import AgentManager
from core.directive_engine import DirectiveEngine
from core.logger import active_connections, broadcast_log
from pydantic import BaseModel
from core.broadcast_utils import active_connections
import uuid
from core.broadcast_utils import broadcast_directive_update



class DirectiveRequest(BaseModel):
    task: str

app = FastAPI(title="Sentinel WebSocket Server", version="0.1.0")
agent_manager = AgentManager()
directive_engine = DirectiveEngine()
router = APIRouter()
# Enable Prometheus Instrumentation
Instrumentator().instrument(app).expose(app)

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

# Store active WebSocket connections
active_connections = {}


@app.websocket("/ws/logs")
async def websocket_logs_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for log streaming.
    """
    await websocket.accept()
    print("✅ Dashboard connected to Logs WebSocket.")

    try:
        while True:
            # Send simulated log messages every 10 seconds
            await websocket.send_json({"type": "log", "message": f"📝 Log Entry {uuid.uuid4()}: Simulated log message."})
            await asyncio.sleep(10)  # Changed from 1 second to 10 seconds
    except WebSocketDisconnect:
        print("🔌 Dashboard disconnected from Logs WebSocket.")



MINIMUM_STAKE = 10000
agent_stakes = {}  # Example storage for agent stakes

@app.websocket("/ws/agent/{agent_id}")
async def websocket_agent_endpoint(websocket: WebSocket, agent_id: str):
    agent_id = agent_id.strip()
    await websocket.accept()
    active_connections[agent_id] = websocket
    print(f"📡 Agent '{agent_id}' connected via WebSocket.")
    await broadcast_log(f"📡 Agent '{agent_id}' connected.")

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "register":
                metadata = data.get("metadata", {})
                stake = metadata.get("stake", 0)

                if stake < MINIMUM_STAKE:
                    await websocket.send_json({"status": "error", "message": f"❌ Insufficient token stake! Minimum required: {MINIMUM_STAKE}"})
                    print(f"❌ Insufficient token stake for '{agent_id}'. Provided: {stake}")
                    continue

                agent_stakes[agent_id] = stake
                print(f"✅ Agent '{agent_id}' registered with stake: {stake}")
                await websocket.send_json({"status": "success", "message": f"✅ Agent '{agent_id}' registered successfully with stake {stake}."})
            
            
            elif action == "directive_response":
                directive_id = data.get("directive_id")
                directive_status = data.get("status")
                if directive_id and directive_status:
                    print(f"✅ Directive '{directive_id}' status updated to '{directive_status}'")
                    await broadcast_log(f"✅ Directive '{directive_id}' updated to '{directive_status}'")
                    
                    # Ensure broadcast directive_update to frontend
                    await broadcast_directive_update({
                        "id": directive_id,
                        "agent_id": agent_id,
                        "task": "optimize_cpu",  # Use the correct task from the directive
                        "status": directive_status
                    })
                else:
                    await websocket.send_json({"status": "error", "message": "❌ Invalid directive response."})


    except WebSocketDisconnect:
        print(f"🔌 Agent '{agent_id}' disconnected.")
        active_connections.pop(agent_id, None)
        agent_stakes.pop(agent_id, None)
        await broadcast_log(f"🔌 Agent '{agent_id}' disconnected.")





@app.post("/api/send_directive/{agent_id}")
async def send_directive(agent_id: str, directive: dict):
    """
    API Endpoint to send a directive to a specific agent via WebSocket.
    """
    agent_id = agent_id.strip()
    
    print(f"DEBUG: Active Connections: {list(active_connections.keys())}")
    print(f"DEBUG: Sending directive to Agent '{agent_id}'")
    
    if agent_id not in active_connections:
        print(f"❌ DEBUG: Agent '{agent_id}' not found in active connections.")
        return {"status": "error", "message": f"❌ Agent '{agent_id}' is not connected."}

    # Create a directive
    directive_id = directive_engine.create_directive(agent_id, directive)
    
    # Send the directive via WebSocket
    await active_connections[agent_id].send_json({
        "action": "directive",
        "directive_id": directive_id,
        "directive": directive
    })
    
    print(f"📨 DEBUG: Directive '{directive_id}' sent to Agent '{agent_id}'")
    
    # Broadcast the directive to all connected clients
    await broadcast_log(f"📨 Directive '{directive_id}' sent to Agent '{agent_id}' with task '{directive.get('task')}'")
    
    return {"status": "success", "message": f"📨 Directive '{directive_id}' sent to Agent '{agent_id}'."}


@app.get("/test_directive_broadcast")
async def test_directive_broadcast():
    directive = {
        "id": "test-uuid",
        "agent_id": "agent-001",
        "task": "test_task1",
        "status": "completed"
    }
    print(f"📡 Broadcasting Directive Update: {directive}")
    await broadcast_directive_update(directive)
    return {"status": "success", "message": "✅ Test directive broadcast sent."}



@app.websocket("/ws/directives")
async def websocket_directives(websocket: WebSocket):
    await websocket.accept()
    agent_id = "agent-dashboard"
    active_connections[agent_id] = websocket
    print(f"📡 Directive WebSocket connected: {agent_id}")
    
    try:
        while True:
            data = await websocket.receive_json()
            print(f"📝 Directive WebSocket Data: {data}")
    except WebSocketDisconnect:
        print(f"🔌 Directive WebSocket disconnected: {agent_id}")
        active_connections.pop(agent_id, None)


async def broadcast_directive_update(directive):
    """
    Broadcast directive updates to all connected clients.
    """
    print(f"📡 Broadcasting Directive Update: {directive['id']}, Status: {directive['status']}")
    disconnected_clients = []
    for agent_id, connection in active_connections.items():
        try:
            await connection.send_json({
                "type": "directive_update",
                "directive": directive
            })
        except Exception as e:
            print(f"❌ Failed to send directive to {agent_id}: {e}")
            disconnected_clients.append(agent_id)


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
        await asyncio.sleep(15)  # Broadcast every 5 seconds

# Start the log generation
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_logs())


@app.get("/tests")
def test_route():
    return {"message": "✅ API is working!"}

@app.get("/cleanup_connections")
async def cleanup_connections():
    active_connections.clear()
    print("🧹 Cleared all active agent connections.")
    return {"status": "success", "message": "🧹 Cleared all active agent connections."}
