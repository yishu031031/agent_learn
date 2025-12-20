from hello_agents.tools import MCPTool, ANPTool, A2ATool

# === 1 .测试MCP访问工具 ===
mcp_tool = MCPTool()
#列出所有可用MCP工具
available_tools = mcp_tool.run({"action": "list_tools"})

'''
🧠 使用内存传输: HelloAgents-BuiltinServer
🔗 连接到 MCP 服务器...
✅ 连接成功！
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
🔌 连接已断开
🧠 使用内存传输: HelloAgents-BuiltinServer
🔗 连接到 MCP 服务器...
✅ 连接成功！
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
🔌 连接已断开

可用MCP工具:
找到 6 个工具:
- add: 加法计算器
- subtract: 减法计算器
- multiply: 乘法计算器
- divide: 除法计算器
- greet: 友好问候
- get_system_info: 获取系统信息
'''

#print(f"\n可用MCP工具:\n{available_tools}")

result = mcp_tool.run({"action":"call_tool","tool_name":"get_system_info","arguments":{}})
'''
🧠 使用内存传输: HelloAgents-BuiltinServer
🔗 连接到 MCP 服务器...
✅ 连接成功！
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
🔌 连接已断开
🧠 使用内存传输: HelloAgents-BuiltinServer
🔗 连接到 MCP 服务器...
✅ 连接成功！
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
🔌 连接已断开
🧠 使用内存传输: HelloAgents-BuiltinServer
🔗 连接到 MCP 服务器...
✅ 连接成功！
INFO:mcp.server.lowlevel.server:Processing request of type CallToolRequest
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
🔌 连接已断开

系统信息:
工具 'get_system_info' 执行结果:
{"platform":"Windows","python_version":"3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:05:38) [MSC v.1929 64 bit (AMD64)]","server_name":"HelloAgents-BuiltinServer","tools_count":6}
'''

#print(f"\n系统信息:\n{result}")

# 2. ANP：服务发现
anp_tool = ANPTool()
anp_tool.run({
    "action": "register_service",
    "service_id": "calculator",
    "service_type": "math",
    "endpoint": "http://localhost:8080"
})
services = anp_tool.run({"action": "discover_services"})
print(f"发现的服务: {services}")

# 3. A2A：智能体通信
a2a_tool = A2ATool("http://localhost:5000")
print("A2A工具创建成功")