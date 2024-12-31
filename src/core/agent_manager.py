import uuid
from datetime import datetime

class AgentManager:
    def __init__(self):
        self.agents = {}  # Store registered agents
        self.min_stake = 10000  # Minimum token stake required for agent registration

    def register_agent(self, agent_metadata):
        """
        Registers a new agent after validating metadata and stake.
        """
        agent_id = agent_metadata.get('agent_id', str(uuid.uuid4()))
        token_stake = agent_metadata.get('token_stake', 0)

        # Validation: Check token stake
        if token_stake < self.min_stake:
            raise ValueError(f"❌ Insufficient token stake! Minimum required: {self.min_stake}")

        # Validation: Check if agent_id is unique
        if agent_id in self.agents:
            raise ValueError(f"❌ Agent ID '{agent_id}' is already registered.")

        # Add additional metadata
        agent_metadata.update({
            'agent_id': agent_id,
            'registered_on': datetime.utcnow().isoformat(),
            'status': 'active'
        })

        self.agents[agent_id] = agent_metadata
        print(f"✅ Agent '{agent_id}' registered successfully.")

    def list_agents(self):
        """
        Returns a list of all registered agents.
        """
        return list(self.agents.values())

    def get_agent(self, agent_id):
        """
        Retrieves metadata of a specific agent by ID.
        """
        return self.agents.get(agent_id, f"❌ Agent ID '{agent_id}' not found.")

    def update_agent_status(self, agent_id, status):
        """
        Updates the status of a specific agent.
        """
        if agent_id not in self.agents:
            raise ValueError(f"❌ Agent ID '{agent_id}' not found.")
        self.agents[agent_id]['status'] = status
        print(f"🔄 Agent '{agent_id}' status updated to '{status}'.")

    def remove_agent(self, agent_id):
        """
        Removes an agent from the registry.
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"🗑️ Agent '{agent_id}' removed successfully.")
        else:
            print(f"❌ Agent ID '{agent_id}' not found.")
