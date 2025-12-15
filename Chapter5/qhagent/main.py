from dotenv import load_dotenv
from llm import QhLLM

load_dotenv(override=True)

llm = QhLLM(model="Qwen/Qwen2.5-VL-72B-Instruct", provider="modelscope")

messages = [
    {"role": "user", "content": "你好，请介绍一下你自己"},
]

# ========== 方案1：使用 think 方法（流式，父类会自动打印）==========
print("=" * 50)
print("方案1：流式响应（父类自动打印）")
print("=" * 50)
reason_response = llm.think(messages)
# 只需要遍历来触发生成器执行，父类已经会自动打印
for chunk in reason_response:
    pass  # 父类已经打印了，这里不需要再次打印

