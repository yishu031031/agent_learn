import os
import re
# 假设 AgentLLM 在同级目录下，如果是文件夹里，请确保路径正确
from llm_call import AgentLLM 
# 【修改点1】去掉相对导入的点
from tool.tool_excute import ToolExecutor
from tool.search_tool import search, __dec__ as search_description

REACT_PROMPT_TEMPLATE = """
你是一个可以调用外部工具的智能助手。请一步步思考并解决用户的问题。

【可用工具】
{tools}

【回答格式】
请严格按照以下格式进行回应（不要通过 Markdown 代码块包裹）：

Thought: 思考当前的情况，分析需要做什么。
Action: 工具名称[工具参数]
Observation: (这一步由工具返回结果，你不需要生成)
... (重复上述过程)
Thought: 我已经有了最终答案。
Action: Finish[最终的回答内容]

【示例演示】
Question: 100美元现在可以兑换多少人民币？
Thought: 我需要查询实时的汇率信息，应该使用搜索工具。
Action: Search[100美元兑换人民币汇率]
Observation: 1美元 ≈ 7.24人民币，100美元 ≈ 724元。
Thought: 我已经获取了汇率信息，可以计算并回答用户了。
Action: Finish[根据最新汇率，100美元大约可以兑换724人民币。]

【开始任务】
Question: {question}
History:
{history}
"""

class ReactAgent:
    def __init__(self, llm_client: AgentLLM, tool_executor: ToolExecutor, max_steps: int = 10):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = [] 

        # 添加 Search 工具
        try:
            # 确保 search_description 是字符串
            desc = search_description.__doc__ if callable(search_description) else str(search_description)
            self.add_tool("Search", desc, search)
        except Exception as e:
            print(f"添加工具 Search 失败，错误信息：{e}")

    def add_tool(self, name: str, description: str, func: callable):
        if not all([name, description, func]):
            return f"工具{name}信息不足，添加失败"
        self.tool_executor.register_tool(
            name=name,
            description=description,
            func=func,
        )

    def _parse_output(self, text: str):
        """解析 LLM 的输出，提取 Thought 和 Action。"""
        # 使用 DOTALL 模式，防止 Thought 换行导致匹配失败
        thought_match = re.search(r"Thought: (.*)", text, re.DOTALL)
        action_match = re.search(r"Action: (.*)", text)
        
        # 简单的文本切割清洗，防止提取过多内容
        thought = thought_match.group(1).strip() if thought_match else None
        if thought and "Action:" in thought:
            thought = thought.split("Action:")[0].strip()
            
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析 Action 字符串，提取工具名称和输入。"""
        # 兼容 Action: Search[华为] 这种格式
        match = re.match(r"(\w+)\[(.*)\]", action_text)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def run(self, query: str):
        self.history = [] 
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n🚀 第 {current_step} 轮思考...")

            # 1. 格式化提示词
            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc,
                question=query,
                history=history_str
            )

            # 2. 调用 LLM
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)

            if not response_text:
                print("LLM 返回空响应，结束思考")
                break

            thought, action = self._parse_output(response_text)

            if thought:
                print(f"💡 思考: {thought}")
            
            if not action:
                print("⚠️ 警告: LLM 未返回有效 Action，尝试继续或结束")
                # 这里可以根据情况决定是 break 还是 continue，通常如果没有 action 只有 thought，可能需要把 thought 加入历史继续
                self.history.append(f"Thought: {thought}")
                continue 

            # 检查终止条件 Finish[答案]
            if action.startswith("Finish"):
                final_answer_match = re.match(r"Finish\[(.*)\]", action)
                final_answer = final_answer_match.group(1) if final_answer_match else action
                print(f"🎉 最终答案: {final_answer}")
                return final_answer
            
            # 解析工具调用
            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                print(f"❌ 无法解析 Action 格式: {action}")
                self.history.append(f"Thought: {thought}\nInvalid Action format: {action}")
                continue

            print(f"🎬 执行工具: {tool_name} 参数: [{tool_input}]")

            # 执行工具
            tool_function = self.tool_executor.get_tool(tool_name)
            if not tool_function:
                observation = f"错误: 未找到名为 {tool_name} 的工具"
            else:
                observation = tool_function(tool_input)
            
            print(f"👀 观察结果: {observation}")

            # 将本轮交互添加到历史
            self.history.append(f"Thought: {thought}\nAction: {action}\nObservation: {observation}")
            
        # 【修改点2】这一段必须在 while 循环外面
        print("❌ 已达到最大步数，流程终止。")
        return None

# 测试代码
if __name__ == "__main__":
    # 1. 实例化依赖组件
    llm = AgentLLM()            # 确保 llm_call.py 里有这个类
    executor = ToolExecutor()   # 确保 ToolExecutor 类没问题

    # 2. 【修改点3】传入参数实例化 Agent
    agent = ReactAgent(llm_client=llm, tool_executor=executor)
    
    query = "请告诉我英伟达目前最新的GPU型号，并告诉我它的价格"
    result = agent.run(query)
    
    if result:
        print("\n最终结果获取成功！")
    else:
        print("\n回答失败")