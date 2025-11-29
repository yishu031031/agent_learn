import os
import re
from llm_call import AgentLLM
from typing import List

EXECUTOR_PROMPT_TEMPLATE = """
# Role
你是一个精准的AI执行引擎。你的唯一职责是执行给定的【当前步骤】，并输出结果。

# Input Context
以下是任务的上下文信息：
=== 原始问题 ===
{question}

=== 完整计划 ===
{plan}

=== 已完成的历史步骤与结果 (Reference) ===
{history}
(注意：请利用历史结果中的数据或上下文，确保逻辑的连贯性。)

=== 当前步骤 (Task) ===
{current_step}

# Constraints
1. **直接输出结果**：不要包含“好的”、“经过计算”、“结果如下”等任何寒暄或解释性文字。
2. **格式自适应**：
   - 如果步骤要求写代码，直接输出代码块。
   - 如果步骤要求回答问题，直接输出答案文本。
3. **依赖引用**：如果当前步骤依赖前一步的输出（如变量名、文件路径），请严格保持一致。

# Output
请在此处直接输出【当前步骤】的执行结果：
"""

class Executor:
    def __init__(self,llm_client:AgentLLM):
        self.llm_client = llm_client
        self.history = [] #记录已完成的历史步骤与结果

    def execute(self,query:str,plan:list[str])->str:
        '''
        根据计划与问题，逐步执行并解决问题
        '''
        print("\n---正在执行计划---")

        final_answer = ""

        for i,step in enumerate(plan): #按序取出
            print(f"正在执行第{i+1}步: {step}，总步数为{len(plan)}")

            #构建prompt
            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=query,
                plan=plan,
                history="\n".join(self.history) if self.history else "无历史上下文",
                current_step=step,
            )

            message = [
                {"role":"user","content":prompt}
            ]
            response = self.llm_client.think(messages=message)
            final_answer = response
            self.history.append(f"第{i+1}步: {step}\n结果: {response}")

            print(f"✅ 步骤 {i+1} 已完成，结果: {response}")
        #循环结束后，最后一步的响应就为最终答案
        return self.history[-1]

        
