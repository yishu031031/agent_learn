from hello_agents import SimpleAgent, HelloAgentsLLM, ReActAgent, ToolRegistry
from hello_agents.tools.builtin.calculator import CalculatorTool
from dotenv import load_dotenv

load_dotenv(override=True)

llm = HelloAgentsLLM()

'''
    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None
    ):
        super().__init__(name, llm, system_prompt, config)
'''    

# ========== 示例1: SimpleAgent - 不支持工具调用 ==========
print("=" * 50)
print("示例1: SimpleAgent (不支持工具调用)")
print("=" * 50)
simple_agent = SimpleAgent(
    name="testAgent",
    llm=llm,
    system_prompt="你是一个有用的AI助手",
)

# 基础对话
response = simple_agent.run("你好,请介绍一下你自己")
print(response)
print()

# 注意：SimpleAgent 无法调用工具，即使创建了 calculator 也不会使用
# calculator = CalculatorTool()  # 创建了但无法使用
response = simple_agent.run("计算一下1+2*3等于多少")
print(f"SimpleAgent 的回复: {response}")
print(f"历史消息数量: {len(simple_agent._history)}")
print()

# ========== 示例2: ReActAgent - 支持工具调用 ==========
print("=" * 50)
print("示例2: ReActAgent (支持工具调用)")
print("=" * 50)

# 创建工具注册表
tool_registry = ToolRegistry()

# 注册计算器工具
calculator = CalculatorTool()
tool_registry.register_tool(calculator)

# 创建 ReActAgent（需要传入 tool_registry）
react_agent = ReActAgent(
    name="calculatorAgent",
    llm=llm,
    tool_registry=tool_registry,
    system_prompt="你是一个擅长计算的AI助手",
)

# 现在可以调用工具进行计算
response = react_agent.run("计算一下1+2*3等于多少")
print(f"\n最终答案: {response}")
print(f"历史消息数量: {len(react_agent._history)}")

