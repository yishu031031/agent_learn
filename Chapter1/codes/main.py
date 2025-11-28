import re
import os
from llm import LLM
from tools.get_weather import get_weather
from tools.search_attraction import get_attraction
from dotenv import load_dotenv

#加载环境变量
load_dotenv(override=True)

#--- 1.配置LLM参数 ---
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_API_BASE_URL","https://api.openai.com/v1")
MODEL_ID = 'gpt-5'
TAVILY_API_KEY = "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"
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
print(f"使用的LLM模型: {MODEL_ID}，api_key: {API_KEY}，API地址: {BASE_URL}")
llm = LLM(model=MODEL_ID,api_key=API_KEY,base_url=BASE_URL)

# 将所有工具函数放入一个字典，方便后续调用
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

#--- 2.初始化 ---
user_prompt = "你好，请帮我查一下南京今日的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_hiustory = [f"用户请求:{user_prompt}"]


print("用户输入:{user_prompt}\n" + '='*40)

#--- 3.运行主循环 ---
for i in range(5):
    print(f"=== 循环{i+1}次 ===")

    #3.1 构建Prompt
    full_prompt = "\n".join(prompt_hiustory) #\n会将列表每一项之间添加，这样层次性更强
    AGENT_SYSTEM_PROMPT = """
        你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

        # 可用工具:
        - `get_weather(city: str)`: 查询指定城市的实时天气。
        - `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

        # 行动格式:
        你的回答必须严格遵循以下格式。首先是你的思考过程，然后是你要执行的具体行动，每次回复只输出一对Thought-Action：
        Thought: [这里是你的思考过程和下一步计划]
        Action: [这里是你要调用的工具，格式为 function_name(arg_name="arg_value")]

        # 任务完成:
        当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `finish(answer="...")` 来输出最终答案。

        请开始吧！
    """
    #3.2 调用LLM
    llm_output = llm.generate_text(full_prompt,system_prompt=AGENT_SYSTEM_PROMPT)
    #模型可能输出多余的Thought-Action，需要截断：
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("注意:截断了多余的LLM输出内容。")
    print(f"LLM输出:\n{llm_output}\n" + '-'*40)
    prompt_hiustory.append(llm_output)

    # 3.3 解析LLM输出并执行行动
    action_match = re.search(r"Action:(.*)",llm_output,re.DOTALL)
    if not action_match:
        print("错误:未找到LLM输出中的Action部分，终止循环。")
        break
    action_str = action_match.group(1).strip()

    if action_str.startswith("finish"):
        #提取最终答案并输出
        final_answer = re.search(r'finish\(answer="(.*)"\)', action_str).group(1)
        print(f"最终答案:\n{final_answer}\n" + '='*40)
        break

    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误: 未知工具 '{tool_name}'"

    # 3.4 将观察结果添加到对话历史
    observation_str = f"Observation: {observation}"
    print(f"工具观察结果:\n{observation_str}\n" + '-'*40)
    prompt_hiustory.append(observation_str)



