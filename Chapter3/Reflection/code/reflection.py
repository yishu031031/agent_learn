'''
在正式构建Reflection之前,需要知晓整个流程有多少个llm角色,根据Reflection的工作流程——执行 -> 反思 -> 优化：
1.首先需要一个初始执行的Prompt
2.其次需要一个根据执行结果,进行结果评审的Prompt
3.最后需要一个根据评审结果,进行优化结果的Prompt
构建结果放在prompt_template.py文件中
'''
from llm_call import AgentLLM
from memory import Memory
from prompt_template import INITIAL_PROMPT_TEMPLATE,REFLECT_PROMPT_TEMPLATE,REFINE_PROMPT_TEMPLATE

class ReflectionAgent:
    def __init__(self,llm_clent:AgentLLM,max_iteration:int = 3):
        '''
        初始化Reflection智能体

        参数：
        - llm_client (AgentLLM): 用于与LLM交互的客户端实例。
        - max_iteration (int, 可选): 最大迭代次数，默认值为3。
        '''
        self.llm_client = llm_clent
        self.max_iteration = max_iteration
        self.memory = Memory()

    def run(self,task:str):
        '''
        运行Reflection智能体,执行任务并进行反思优化
        '''
        print(f"\n---开始处理任务 ----\n任务描述：{task}")

        #1.初始执行
        print("\n---正在进行初始尝试----")
        initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=task)
        initial_message = [
            {"role":"user","content":initial_prompt}
        ]
        initial_code = self.llm_client.think(messages=initial_message)
        print(f"初始执行结果：{initial_code}")
        self.memory.add_record(record_type="execution",content=initial_code)


        #2.迭代循环，反思优化
        for i in range(self.max_iteration):
            print(f"\n---正在进行第{i+1}次迭代----")

            #2.1 反思
            print(f"\n正在进行反思")
            last_code = self.memory.get_last_execution()
            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(
                task=task,
                code=last_code,
            )
            reflect_message = [
                {"role":"user","content":reflect_prompt}
            ]
            feedback = self.llm_client.think(messages=reflect_message)
            print(f"\n反思结果：{feedback}\n")
            self.memory.add_record("reflection",feedback)

            if "无需改进" in feedback:
                print(f"\n反思认为代码已无需改进,任务完成")
                break#退出迭代


            #2.2 优化
            print(f"\n正在优化代码")
            
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                task=task,
                last_code_attempt=last_code,
                feedback=feedback,
            )
            refine_message = [
                {"role":"user","content":refine_prompt}
            ]
            refined_code = self.llm_client.think(messages=refine_message)
            print(f"\n优化后的代码：{refined_code}")
            self.memory.add_record("execution",refined_code)
        
        final_code = self.memory.get_last_execution()
        print(f"\n---任务完成---\n最终代码：{final_code}")
        return final_code
    
if __name__ == '__main__':
    llm_client = AgentLLM()
    reflectionagent = ReflectionAgent(llm_clent=llm_client)
    task = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)。"
    final_code = reflectionagent.run(task)

            



