import asyncio
import sys
import os

# Add core folder to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

from sentinel_core_agent import SentinelCoreAgent

async def test_register_agent():
    sentinel = SentinelCoreAgent()
    result = await sentinel.register_agent("TestAgent", "test", 10000)
    assert result["status"] == "success"
    print("✅ Agent Registration Test Passed")

async def test_list_agents():
    sentinel = SentinelCoreAgent()
    await sentinel.register_agent("TestAgent", "test", 10000)
    agents = await sentinel.list_agents()
    assert len(agents) > 0
    print("✅ Agent Listing Test Passed")

async def test_send_directive():
    sentinel = SentinelCoreAgent()
    result = await sentinel.register_agent("TestAgent", "test", 10000)
    agent_id = result["agent_id"]
    directive_result = await sentinel.send_directive(agent_id, "TestDirective")
    assert directive_result["status"] == "success"
    print("✅ Directive Dispatch Test Passed")

async def main():
    await test_register_agent()
    await test_list_agents()
    await test_send_directive()

if __name__ == '__main__':
    asyncio.run(main())
