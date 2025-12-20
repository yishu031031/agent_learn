import os
from dotenv import load_dotenv
from hello_agents import SimpleAgent,HelloAgentsLLM
from hello_agents.tools import MCPTool

#加载环境变量
load_dotenv(override=True)

#创建llm相关配置
api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
model = os.getenv("LLM_MODEL_ID")

agent = SimpleAgent(
    name="助手",
    llm=HelloAgentsLLM(api_key=api_key,base_url=base_url,model=model)
)

#无需任何配置，自动配置内置演示服务器
mcp_tool = MCPTool()

#展示有多少工具在mcp_tool中
result = mcp_tool.run({"action":"list_tools"})
'''
🔌 连接已断开
🧠 使用内存传输: HelloAgents-BuiltinServer
🔗 连接到 MCP 服务器...
✅ 连接成功！
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
🔌 连接已断开
找到 6 个工具:
- add: 加法计算器
- subtract: 减法计算器
- multiply: 乘法计算器
- divide: 除法计算器
- greet: 友好问候
- get_system_info: 获取系统信息

'''
#print(result)

#添加工具
agent.add_tool(mcp_tool)

#智能体可以直接使用展开后的工具
response = agent.run("计算 25 乘以 16")

print(response)
