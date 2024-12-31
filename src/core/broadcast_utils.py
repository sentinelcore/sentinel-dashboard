import asyncio

# Store active connections globally
active_connections = {}

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
            print(f"✅ Sent directive_update to {agent_id}")
        except Exception as e:
            print(f"❌ Failed to send directive to {agent_id}: {e}")
            disconnected_clients.append(agent_id)


