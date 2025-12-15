from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM,ToolRegistry
from hello_agents.tools.builtin.calculator import CalculatorTool
from my_simpleagent import MysimpleAgent

load_dotenv(override=True)

llm = HelloAgentsLLM()

#测试1：无工具调用，基础对话Agent
print("\n === 测试1：无工具调用，基础对话Agent ===")

basic_agent = MysimpleAgent(
    name="BasicAgent",
    llm=llm,
    system_prompt="你是一个有用的AI助手，请根据用户的问题给出回答。",
    )

user_input = "您好，请介绍一下你自己"
response = basic_agent.run(user_input)

#print(f"BasicAgent回答:\n{response}")

#测试2：有工具调用，使用计算器工具
print("\n === 测试2：有工具调用，使用计算器工具 ===")

tool_registry = ToolRegistry()
calculator = CalculatorTool()
tool_registry.register_tool(calculator)

enhanced_agent = MysimpleAgent(
    name="增强助手",
    llm=llm,
    system_prompt="你是一个有用的AI助手，可以使用工具来帮助用户",
    tool_registry=tool_registry,
    enable_tool_calling=True,
)

response = enhanced_agent.run("请计算15 * 8 + 20 * 8")
#print(f"增强助手回答:\n{response}")


#测试三：动态添加工具
print("\n === 测试三：动态添加工具 ===")
print(f"\n添加工具前basic_agent的工具列表为:{basic_agent.list_tools()}")
#添加计算器工具
basic_agent.add_tool(calculator)
print(f"添加工具后: {basic_agent.has_tool()}")
print(f"可用工具: {basic_agent.list_tools()}")

# 查看对话历史
print(f"\n对话历史: {len(basic_agent.get_history())} 条消息")

