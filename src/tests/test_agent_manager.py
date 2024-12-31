import asyncio
import sys
import os

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.agent_manager import AgentManager

def test_agent_registration():
    manager = AgentManager()
    agent_metadata = {
        'name': 'Test Agent',
        'type': 'sub-agent',
        'capabilities': ['monitor_cpu', 'optimize_gpu'],
        'token_stake': 12000
    }
    
    manager.register_agent(agent_metadata)
    assert len(manager.list_agents()) == 1
    print("✅ Agent Registration Test Passed")

def test_agent_duplicate_registration():
    manager = AgentManager()
    agent_metadata = {
        'agent_id': 'agent-123',
        'name': 'Duplicate Agent',
        'token_stake': 15000
    }
    
    manager.register_agent(agent_metadata)
    try:
        manager.register_agent(agent_metadata)
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")

def test_agent_retrieval():
    manager = AgentManager()
    agent_metadata = {
        'agent_id': 'agent-456',
        'name': 'Retrieve Agent',
        'token_stake': 12000
    }
    manager.register_agent(agent_metadata)
    agent = manager.get_agent('agent-456')
    assert agent['name'] == 'Retrieve Agent'
    print("✅ Agent Retrieval Test Passed")

def test_agent_status_update():
    manager = AgentManager()
    agent_metadata = {
        'agent_id': 'agent-789',
        'name': 'Status Update Agent',
        'token_stake': 13000
    }
    manager.register_agent(agent_metadata)
    manager.update_agent_status('agent-789', 'inactive')
    agent = manager.get_agent('agent-789')
    assert agent['status'] == 'inactive'
    print("✅ Agent Status Update Test Passed")

if __name__ == "__main__":
    test_agent_registration()
    test_agent_duplicate_registration()
    test_agent_retrieval()
    test_agent_status_update()
    print("🎯 All Tests Passed Successfully!")
