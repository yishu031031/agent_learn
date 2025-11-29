import os
import re
from planner import Planner
from executor import Executor
from llm_call import AgentLLM

class PlanAndSolveAgent:
    def __init__(self,llm_client:AgentLLM):
        self.llm_client = llm_client
        self.planner = Planner(llm_client)
        self.executor = Executor(llm_client)

    def run(self,query:str):
        '''
        运行智能体的完整流程：先规划，后执行
        '''
        print(f"\n----开始处理问题----\n问题:{query}")


        #1.首先调用Planner生成plan
        plan = self.planner.plan(query)

        #对输出进行检验
        if plan is None:
            print("\n-----任务终止，规划失败-----\n")
            return
        
        #2.调用Executor执行plan
        final_answer = self.executor.execute(query=query,plan=plan)
        if final_answer:
            print(f"\n----任务完成----\n最终答案:{final_answer}")
        else:
            print(f"任务失败")


if __name__ == "__main__":
    llm_client = AgentLLM(
        model="gpt-4o"
    )
    plan_and_solve = PlanAndSolveAgent(llm_client=llm_client)
    query = "小明5次月考总分分别为:630,640,620,590,620,而武大华科分数线是630，请帮我分析一下小明考上武大华科的概率,最好用数字来表示考上概率大小。"
    plan_and_solve.run(query)

        
