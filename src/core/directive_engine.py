import uuid
from core.logger import broadcast_log
import asyncio
from core.broadcast_utils import broadcast_directive_update

class DirectiveEngine:
    """
    Manages creation, tracking, and updates of directives sent to agents.
    """
    def __init__(self):
        # Store directives with their unique IDs
        self.directives = {}

    def create_directive(self, agent_id: str, directive_data: dict) -> str:
        """
        Create a new directive for an agent.
        """
        directive_id = str(uuid.uuid4())
        directive = {
            "id": directive_id,
            "agent_id": agent_id,
            "task": directive_data.get("task", "No task specified"),
            "status": "pending"
        }
        self.directives[directive_id] = directive
        print(f"✅ Directive '{directive_id}' created for Agent '{agent_id}' with task '{directive['task']}'.")
        return directive_id

    def update_directive_status(self, directive_id: str, status: str):
        """
        Update the status of an existing directive and broadcast updates.
        """
        if directive_id in self.directives:
            self.directives[directive_id]['status'] = status
            print(f"🔄 Directive '{directive_id}' updated to '{status}'.")
            asyncio.create_task(broadcast_directive_update(self.directives[directive_id]))
        else:
            print(f"❌ Directive ID '{directive_id}' not found.")

    def get_directive(self, directive_id: str) -> dict:
        """
        Retrieve a specific directive by its ID.
        
        :param directive_id: The unique ID of the directive.
        :return: Dictionary containing directive details.
        """
        if directive_id in self.directives:
            print(f"🔍 Retrieved Directive '{directive_id}'.")
            return self.directives[directive_id]
        else:
            print(f"❌ Directive ID '{directive_id}' not found.")
            return {}

    def list_directives(self) -> dict:
        """
        List all current directives.
        
        :return: A dictionary of all directives.
        """
        print(f"📋 Listing all directives ({len(self.directives)} total).")
        return self.directives
