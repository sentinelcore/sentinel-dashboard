import asyncio
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from core.websocket_server import broadcast_log

# Directive Engine - Handles Directive Parsing, Validation, and Execution

# ----------------------------
# Global Variables
# ----------------------------
DIRECTIVES_LOG: List[Dict] = []  # Stores all task directives

# Configurable Parameters
DIRECTIVE_TIMEOUT = 60  # Time in seconds for directive timeout

# ----------------------------
# Utility Functions
# ----------------------------

def generate_directive_id() -> str:
    """Generate a unique Directive ID."""
    return f"directive_{uuid.uuid4().hex[:8]}"

def current_time() -> str:
    """Return the current timestamp."""
    return datetime.utcnow().isoformat()

# ----------------------------
# Directive Engine Class
# ----------------------------

class DirectiveEngine:
    def __init__(self):
        self.directives: Dict[str, Dict] = {}
        self.logs: List[str] = []
        print("✅ Directive Engine initialized.")
    
    async def validate_directive(self, directive: Dict) -> bool:
        """Validate the directive payload."""
        required_keys = ["agent_id", "task", "payload"]
        for key in required_keys:
            if key not in directive:
                self.logs.append(f"❌ Validation failed: Missing {key} in directive.")
                return False
        return True
    
    async def dispatch_directive(self, agent_id: str, task: str, payload: Optional[Dict] = None) -> Dict:
        """Dispatch a directive to the specified agent."""
        directive_id = generate_directive_id()
        directive_entry = {
            "id": directive_id,
            "agent_id": agent_id,
            "task": task,
            "payload": payload or {},
            "timestamp": current_time(),
            "status": "in-progress"
        }
        
        if not await self.validate_directive(directive_entry):
            return {"status": "error", "message": "Directive validation failed."}
        
        self.directives[directive_id] = directive_entry
        DIRECTIVES_LOG.append(directive_entry)
        self.logs.append(f"📨 Directive {directive_id} dispatched to Agent {agent_id}: {task}")
        print(f"📨 Directive {directive_id} dispatched to Agent {agent_id}: {task}")
        
        # Simulate directive execution
        await asyncio.sleep(1)
        directive_entry["status"] = "completed"
        self.logs.append(f"✅ Directive {directive_id} completed successfully.")
        print(f"✅ Directive {directive_id} completed successfully.")
        
        return {"status": "success", "directive_id": directive_id}
    
    async def list_directives(self) -> List[Dict]:
        """List all dispatched directives."""
        return list(self.directives.values())
    
    async def get_logs(self) -> List[str]:
        """Retrieve logs from Directive Engine."""
        return self.logs
    
    #Websocket Server
    async def dispatch_directive(self, agent_id: str, task: str, payload: Optional[Dict] = None) -> Dict:
        directive_id = generate_directive_id()
        directive_entry = {
            "id": directive_id,
            "agent_id": agent_id,
            "task": task,
            "payload": payload or {},
            "timestamp": current_time(),
            "status": "in-progress"
        }
        self.directives[directive_id] = directive_entry
        DIRECTIVES_LOG.append(directive_entry)
        log_message = f"📨 Directive {directive_id} dispatched to Agent {agent_id}: {task}"
        await broadcast_log(log_message)
        print(log_message)
        
        await asyncio.sleep(1)
        directive_entry["status"] = "completed"
        log_message = f"✅ Directive {directive_id} completed successfully."
        await broadcast_log(log_message)
        print(log_message)
        
        return {"status": "success", "directive_id": directive_id}

# ----------------------------
# Test the Directive Engine
# ----------------------------

async def main():
    engine = DirectiveEngine()
    
    # Dispatching directives
    print("\n--- Dispatching Directives ---")
    result_1 = await engine.dispatch_directive("agent_1234", "Optimize GPU", {"priority": "high"})
    print(result_1)
    result_2 = await engine.dispatch_directive("agent_5678", "Clean Storage", {"priority": "medium"})
    print(result_2)
    
    # Listing directives
    print("\n--- Listing Directives ---")
    directives = await engine.list_directives()
    print(directives)
    
    # Fetching logs
    print("\n--- Directive Engine Logs ---")
    logs = await engine.get_logs()
    for log in logs:
        print(log)

if __name__ == '__main__':
    asyncio.run(main())
import asyncio
import uuid
from typing import Dict, List, Optional
from datetime import datetime

# Directive Engine - Handles Directive Parsing, Validation, and Execution

# ----------------------------
# Global Variables
# ----------------------------
DIRECTIVES_LOG: List[Dict] = []  # Stores all task directives

# Configurable Parameters
DIRECTIVE_TIMEOUT = 60  # Time in seconds for directive timeout

# ----------------------------
# Utility Functions
# ----------------------------

def generate_directive_id() -> str:
    """Generate a unique Directive ID."""
    return f"directive_{uuid.uuid4().hex[:8]}"

def current_time() -> str:
    """Return the current timestamp."""
    return datetime.utcnow().isoformat()

# ----------------------------
# Directive Engine Class
# ----------------------------

class DirectiveEngine:
    def __init__(self):
        self.directives: Dict[str, Dict] = {}
        self.logs: List[str] = []
        print("✅ Directive Engine initialized.")
    
    async def validate_directive(self, directive: Dict) -> bool:
        """Validate the directive payload."""
        required_keys = ["agent_id", "task", "payload"]
        for key in required_keys:
            if key not in directive:
                self.logs.append(f"❌ Validation failed: Missing {key} in directive.")
                return False
        return True
    
    async def dispatch_directive(self, agent_id: str, task: str, payload: Optional[Dict] = None) -> Dict:
        """Dispatch a directive to the specified agent."""
        directive_id = generate_directive_id()
        directive_entry = {
            "id": directive_id,
            "agent_id": agent_id,
            "task": task,
            "payload": payload or {},
            "timestamp": current_time(),
            "status": "in-progress"
        }
        
        if not await self.validate_directive(directive_entry):
            return {"status": "error", "message": "Directive validation failed."}
        
        self.directives[directive_id] = directive_entry
        DIRECTIVES_LOG.append(directive_entry)
        self.logs.append(f"📨 Directive {directive_id} dispatched to Agent {agent_id}: {task}")
        print(f"📨 Directive {directive_id} dispatched to Agent {agent_id}: {task}")
        
        # Simulate directive execution
        await asyncio.sleep(1)
        directive_entry["status"] = "completed"
        self.logs.append(f"✅ Directive {directive_id} completed successfully.")
        print(f"✅ Directive {directive_id} completed successfully.")
        
        return {"status": "success", "directive_id": directive_id}
    
    async def list_directives(self) -> List[Dict]:
        """List all dispatched directives."""
        return list(self.directives.values())
    
    async def get_logs(self) -> List[str]:
        """Retrieve logs from Directive Engine."""
        return self.logs

# ----------------------------
# Test the Directive Engine
# ----------------------------

async def main():
    engine = DirectiveEngine()
    
    # Dispatching directives
    print("\n--- Dispatching Directives ---")
    result_1 = await engine.dispatch_directive("agent_1234", "Optimize GPU", {"priority": "high"})
    print(result_1)
    result_2 = await engine.dispatch_directive("agent_5678", "Clean Storage", {"priority": "medium"})
    print(result_2)
    
    # Listing directives
    print("\n--- Listing Directives ---")
    directives = await engine.list_directives()
    print(directives)
    
    # Fetching logs
    print("\n--- Directive Engine Logs ---")
    logs = await engine.get_logs()
    for log in logs:
        print(log)

if __name__ == '__main__':
    asyncio.run(main())
