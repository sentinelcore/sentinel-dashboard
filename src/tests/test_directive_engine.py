import asyncio
import sys
import os

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.directive_engine import DirectiveEngine

async def test_validate_directive():
    print("🔄 Running: test_validate_directive")
    engine = DirectiveEngine()
    valid_directive = {
        "agent_id": "agent_1234",
        "task": "Optimize GPU",
        "payload": {"priority": "high"}
    }
    invalid_directive = {
        "task": "Missing Agent ID"
    }
    assert await engine.validate_directive(valid_directive) == True
    assert await engine.validate_directive(invalid_directive) == False
    print("✅ Directive Validation Test Passed")

async def test_dispatch_directive():
    print("🔄 Running: test_dispatch_directive")
    engine = DirectiveEngine()
    result = await engine.dispatch_directive("agent_1234", "Optimize GPU", {"priority": "high"})
    assert result["status"] == "success"
    print("✅ Directive Dispatch Test Passed")

async def test_list_directives():
    print("🔄 Running: test_list_directives")
    engine = DirectiveEngine()
    await engine.dispatch_directive("agent_1234", "Optimize GPU", {"priority": "high"})
    directives = await engine.list_directives()
    assert len(directives) > 0
    print("✅ Directive Listing Test Passed")

async def test_logs():
    print("🔄 Running: test_logs")
    engine = DirectiveEngine()
    await engine.dispatch_directive("agent_1234", "Optimize GPU", {"priority": "high"})
    logs = await engine.get_logs()
    assert len(logs) > 0
    print("✅ Directive Logs Test Passed")

async def main():
    print("\n=== 🚀 Running Directive Engine Tests ===")
    await test_validate_directive()
    await test_dispatch_directive()
    await test_list_directives()
    await test_logs()
    print("\n🎯 All tests passed successfully!")

if __name__ == '__main__':
    asyncio.run(main())
