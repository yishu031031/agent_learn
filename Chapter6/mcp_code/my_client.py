# 文件名: agent.py
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# 导入 MCP 核心库
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv(override=True)

async def run_agent():
    # ==========================================
    # 1. 配置连接：告诉 Agent 去哪里找 server.py
    # ==========================================
    server_params = StdioServerParameters(
        command="python", # 使用 python 命令
        args=["my_server.py"], # 执行 server.py 脚本
        env=None
    )

    # ==========================================
    # 2. 建立连接 (Context Manager)
    # ==========================================
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # --- 步骤 A: 初始化并获取工具列表 ---
            await session.initialize()
            
            # 从服务端获取可用工具
            tools_list = await session.list_tools()
            print(f"🔌 已连接 MCP 服务，发现工具: {[t.name for t in tools_list.tools]}")

            # --- 步骤 B: 将 MCP 工具转换为 LLM 可理解的格式 ---
            # 我们需要把 MCP 的 schema 转换成 OpenAI 的 tool schema
            formatted_tools = []
            for tool in tools_list.tools:
                formatted_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })

            # --- 步骤 C: 初始化 LLM 并绑定工具 ---
            llm = ChatOpenAI(
                model = os.getenv("LLM_MODEL_ID","gpt-4o"),
                api_key = os.getenv("LLM_API_KEY"),
                base_url = os.getenv("LLM_BASE_URL","https://api.example-llm.com/v1"),
                temperature=0.7,
            )
            llm_with_tools = llm.bind_tools(formatted_tools)

            # --- 步骤 D: 发送用户查询 ---
            query = "请帮我计算 123 加 456 是多少？然后再分析一下字符串 'Hello MCP World' 的长度。"
            print(f"\n🤔 用户提问: {query}")
            
            messages = [HumanMessage(content=query)]
            ai_response = await llm_with_tools.ainvoke(messages)
            
            messages.append(ai_response) # 把 AI 的思考加入历史

            # --- 步骤 E: 处理工具调用 (Tool Call) ---
            if ai_response.tool_calls:
                for tool_call in ai_response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    
                    print(f"🛠️ Agent 决定调用工具: {tool_name} 参数: {tool_args}")

                    # !!! 关键点：Agent 通过 Session 调用远端 MCP Server !!!
                    result = await session.call_tool(tool_name, tool_args)
                    
                    # 获取结果文本
                    tool_output = result.content[0].text
                    print(f"✅ 工具返回结果: {tool_output}")

                    # 将结果构造为 ToolMessage 传回给 LLM
                    messages.append(ToolMessage(
                        content=tool_output,
                        tool_call_id=tool_call["id"]
                    ))

                # --- 步骤 F: 生成最终回答 ---
                final_response = await llm_with_tools.ainvoke(messages)
                print(f"\n💡 最终回答: {final_response.content}")

if __name__ == "__main__":
    asyncio.run(run_agent())