import os
from dotenv import load_dotenv
from hello_agents import SimpleAgent,HelloAgentsLLM,ReActAgent
from hello_agents.tools import MCPTool

#加载环境变量
load_dotenv(override=True)

#创建llm相关配置
api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
model = os.getenv("LLM_MODEL_ID")

agent = SimpleAgent(name="文件助手", llm=HelloAgentsLLM(api_key=api_key,base_url=base_url,model=model))

# 示例1：连接到社区提供的文件系统服务器
fs_tool = MCPTool(
    name="filesystem",  # 指定唯一名称
    description="访问本地文件系统",
    server_command=["npx", "-y", "@modelcontextprotocol/server-filesystem", "../.."]
)
agent.add_tool(fs_tool)


# Agent现在可以自动使用这些工具！
response = agent.run("请先列举一下当前目录下的所有文件和目录，随后告诉我当前目录下有哪些文件和目，随后创建一个名为test.txt的文件，并写入内容：hello,world!")
print(response)
