import asyncio
import uuid
from typing import Dict, List, Optional
from datetime import datetime

# Sentinel Core Agent - Manages Global Agent Registry, Directives, and Health Monitoring

# ----------------------------
# Global Variables
# ----------------------------
AGENT_REGISTRY: Dict[str, Dict] = {}  # Stores all registered agents
directives_log: List[Dict] = []  # Stores all task directives

# Configurable Token Stake Parameters
BASE_STAKE = 10000
STAKE_INCREASE_PERCENTAGE = 5
STAKE_INCREASE_INTERVAL = 100

# ----------------------------
# Utility Functions
# ----------------------------

def calculate_stake(agent_count: int) -> int:
    """Dynamically calculate stake based on the number of agents deployed."""
    intervals = agent_count // STAKE_INCREASE_INTERVAL
    return int(BASE_STAKE * (1 + (STAKE_INCREASE_PERCENTAGE / 100) * intervals))

def generate_agent_id() -> str:
    """Generate a unique Agent ID."""
    return f"agent_{uuid.uuid4().hex[:8]}"

def current_time() -> str:
    """Return the current timestamp."""
    return datetime.utcnow().isoformat()

# ----------------------------
# Sentinel Core Agent Class
# ----------------------------

class SentinelCoreAgent:
    def __init__(self):
        self.agent_count = 0
        self.logs: List[str] = []
        print("✅ Sentinel Core Agent initialized.")
    
    async def register_agent(self, agent_name: str, agent_type: str, stake: int, metadata: Optional[Dict] = None) -> Dict:
        """Register a new agent with token validation."""
        required_stake = calculate_stake(self.agent_count)
        if stake < required_stake:
            return {"status": "error", "message": f"Insufficient stake. Required: {required_stake}"}
        
        agent_id = generate_agent_id()
        AGENT_REGISTRY[agent_id] = {
            "id": agent_id,
            "name": agent_name,
            "type": agent_type,
            "status": "active",
            "registered_at": current_time(),
            "metadata": metadata or {},
            "stake": stake
        }
        self.agent_count += 1
        self.logs.append(f"Agent {agent_name} ({agent_id}) registered successfully.")
        print(f"🔗 Agent {agent_name} registered with ID {agent_id}.")
        return {"status": "success", "agent_id": agent_id}
    
    async def list_agents(self) -> List[Dict]:
        """List all registered agents."""
        return list(AGENT_REGISTRY.values())
    
    async def send_directive(self, agent_id: str, directive: str, payload: Optional[Dict] = None) -> Dict:
        """Send a directive to a specific agent."""
        if agent_id not in AGENT_REGISTRY:
            return {"status": "error", "message": "Agent not found."}
        
        directive_entry = {
            "agent_id": agent_id,
            "directive": directive,
            "payload": payload or {},
            "timestamp": current_time(),
            "status": "in-progress"
        }
        directives_log.append(directive_entry)
        self.logs.append(f"Directive sent to Agent {agent_id}: {directive}")
        print(f"📨 Directive sent to Agent {agent_id}: {directive}")
        return {"status": "success", "message": "Directive dispatched successfully."}
    
    async def get_agent_logs(self) -> List[str]:
        """Retrieve logs from Sentinel Core Agent."""
        return self.logs

# ----------------------------
# Test the Sentinel Core Agent
# ----------------------------

async def main():
    sentinel = SentinelCoreAgent()
    
    # Registering agents
    print("\n--- Registering Agents ---")
    result_1 = await sentinel.register_agent("ComputeAgent", "compute", 10000)
    print(result_1)
    result_2 = await sentinel.register_agent("StorageAgent", "storage", 10500)
    print(result_2)
    
    # Listing agents
    print("\n--- Listing Agents ---")
    agents = await sentinel.list_agents()
    print(agents)
    
    # Sending a directive
    print("\n--- Sending Directive ---")
    if agents:
        directive_result = await sentinel.send_directive(agents[0]['id'], "Optimize GPU usage", {"priority": "high"})
        print(directive_result)
    
    # Fetching logs
    print("\n--- Sentinel Logs ---")
    logs = await sentinel.get_agent_logs()
    for log in logs:
        print(log)

if __name__ == '__main__':
    asyncio.run(main())
