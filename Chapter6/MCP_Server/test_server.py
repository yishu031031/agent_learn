"""
测试天气查询 MCP 服务器

该脚本用于测试 MCP 服务器的功能，验证工具是否正常工作。
"""

import asyncio
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from hello_agents.tools import MCPTool
except ImportError:
    print("警告: 无法导入 hello_agents，将使用直接测试方式")
    MCPTool = None


def test_direct():
    """直接测试天气查询函数"""
    print("=" * 50)
    print("直接测试天气查询函数")
    print("=" * 50)
    
    from weather_server import get_weather, get_weather_detailed
    
    # 测试基本天气查询
    print("\n1. 测试基本天气查询")
    print("-" * 50)
    cities = ["北京", "Shanghai", "New York"]
    for city in cities:
        result = get_weather(city)
        print(f"{city}: {result}")
    
    # 测试详细天气查询
    print("\n2. 测试详细天气查询")
    print("-" * 50)
    result = get_weather_detailed("北京")
    print(result)


async def test_mcp_tool():
    """使用 MCPTool 测试服务器"""
    print("=" * 50)
    print("使用 MCPTool 测试 MCP 服务器")
    print("=" * 50)
    
    # 创建 MCP 工具
    weather_tool = MCPTool(
        name="weather_server",
        description="天气查询 MCP 服务器",
        server_command=["python", "weather_server.py"]
    )
    
    try:
        # 1. 列出可用工具
        print("\n1. 列出可用工具")
        print("-" * 50)
        result = weather_tool.run({"action": "list_tools"})
        print(f"可用工具: {result}")
        
        # 2. 调用 get_weather 工具
        print("\n2. 调用 get_weather 工具")
        print("-" * 50)
        cities = ["北京", "Shanghai", "Tokyo"]
        for city in cities:
            result = weather_tool.run({
                "action": "call_tool",
                "tool_name": "get_weather",
                "arguments": {"city": city}
            })
            print(f"{city}: {result}")
        
        # 3. 调用 get_weather_detailed 工具
        print("\n3. 调用 get_weather_detailed 工具")
        print("-" * 50)
        result = weather_tool.run({
            "action": "call_tool",
            "tool_name": "get_weather_detailed",
            "arguments": {"city": "北京"}
        })
        print(result)
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """主测试函数"""
    print("\n" + "=" * 50)
    print("天气查询 MCP 服务器测试")
    print("=" * 50)
    
    # 首先进行直接测试
    test_direct()
    
    # 如果可用，进行 MCP 工具测试
    if MCPTool:
        print("\n")
        try:
            await test_mcp_tool()
        except Exception as e:
            print(f"\nMCP 工具测试失败: {e}")
            print("提示: 确保已安装 hello_agents 包")
    else:
        print("\n跳过 MCP 工具测试（hello_agents 不可用）")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())

