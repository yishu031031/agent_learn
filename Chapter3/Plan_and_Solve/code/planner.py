from typing import List, Dict
import ast
from llm_call import AgentLLM

# 1. 修改 Prompt：使用标准的 Markdown 反引号 (```) 作为示例
Planner_prompt_template = """
# Role
你是一个系统性的AI任务规划师。

# Task
分析用户的问题: "{question}"
请先在内心思考解决这个问题的最佳路径，识别潜在的依赖关系，然后生成一个详细的步骤列表。

# Constraints
1. 列表必须是合法的Python List[str]。
2. 步骤描述需要包含动词，具有可执行性（如“搜索...”、“计算...”、“生成...”）。
3. **输出中严禁包含除Python代码块以外的任何文字。**

# Output Format
```python
["Step 1", "Step 2", ...]
"""

class Planner: 
    def __init__(self, llm_client: AgentLLM): 
        self.llm_client = llm_client

    def plan(self, query: str) -> List[str]:
        '''
        根据用户的问题，生成一个解决问题的步骤列表
        '''
        prompt = Planner_prompt_template.format(question=query)

        message = [
            {"role": "user", "content": prompt},
        ]

        print("正在生成计划...")
        
        response = self.llm_client.think(messages=message)

        print(f"✅ 计划已生成:\n{response}")

        # 2. 增强解析逻辑：兼容多种输出格式
        try:
            plan_str = ""
            # 情况 A: 标准 Markdown 代码块 (```python ... ```)
            if "```python" in response:
                plan_str = response.split("```python")[1].split("```")[0].strip()
            # 情况 B: 通用代码块 (``` ... ```) - 防止模型忘了写 python
            elif "```" in response:
                plan_str = response.split("```")[1].split("```")[0].strip()
            # 情况 C: 裸文本 (直接输出了列表)
            else:
                plan_str = response.strip()

            # 3. 安全转换：Text -> List
            plan = ast.literal_eval(plan_str)

            # 4. 类型检查：确保得到的是列表
            if isinstance(plan, list):
                return plan
            else:
                print(f"❌ 解析错误: 得到的类型是 {type(plan)}，而不是 list")
                return []

        except (ValueError, SyntaxError) as e:
            print(f"❌ 格式错误 (无法解析为List): {e}")
            print(f"提取到的内容: {plan_str}")
            return []
        except IndexError as e:
            print(f"❌ 提取错误 (找不到代码块标记): {e}")
            print(f"原始响应: {response}")
            return []
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return []