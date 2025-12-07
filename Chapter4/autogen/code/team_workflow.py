from autogen_agentchat.teams import RoundRobinGroupChat  #RoundRobinGroupChat (轮询群聊)
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from role import create_product_manager, create_engineer,create_code_reviewer,create_user_proxy
from llm_call import creat_client

class TeamWorkflow:
    def __init__(self):
        self.model_client = creat_client()
        self.product_manager = create_product_manager(self.model_client)
        self.engineer = create_engineer(self.model_client)
        self.code_reviewer = create_code_reviewer(self.model_client)
        self.user_proxy = create_user_proxy()

    def creat_teamchat(self):
        '''
        参与者顺序: participants 列表的顺序决定了智能体发言的先后次序。
        终止条件: termination_condition 是控制协作流程何时结束的关键。这里我们设定，当任何消息中包含关键词 "TERMINATE" 时，对话便结束。在我们的设计中，这个指令由 UserProxy 在完成最终测试后发出。
        最大轮次: max_turns 是一个安全阀，用于防止对话陷入无限循环，避免不必要的资源消耗。
        '''

        team_chat = RoundRobinGroupChat(
        participants=[
            self.product_manager,
            self.engineer,
            self.code_reviewer,
            self.user_proxy
        ],
            termination_condition=TextMentionTermination("TERMINATE"),
            max_turns=20,
        )
        return team_chat

async def main(team_chat):
    # ... 初始化客户端和智能体 ...
    
    # 定义任务描述
    task = """我们需要开发一个比特币价格显示应用，具体要求如下：
            核心功能：
            - 实时显示比特币当前价格（USD）
            - 显示24小时价格变化趋势（涨跌幅和涨跌额）
            - 提供价格刷新功能

            技术要求：
            - 使用 Streamlit 框架创建 Web 应用
            - 界面简洁美观，用户友好
            - 添加适当的错误处理和加载状态

            请团队协作完成这个任务，从需求分析到最终实现。"""
    
    # 异步执行团队协作，并流式输出对话过程
    result = await Console(team_chat.run_stream(task=task))
    return result


# 测试代码
if __name__ == '__main__':
    team_workflow = TeamWorkflow()
    team_chat = team_workflow.creat_teamchat()
    import asyncio
    result = asyncio.run(main(team_chat))
    print(result)
    