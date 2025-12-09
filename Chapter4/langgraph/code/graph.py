import sys
from langchain_core.messages import HumanMessage
from state_creat import SearchState
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver
from node import NodeConfig

def creat_search_assistant_graph()->StateGraph:
    '''
    创建一个基于状态图的搜索助手智能体
    '''
    workflow = StateGraph(SearchState)

    node_config = NodeConfig()

    workflow.add_node("understand",node_config.understand_query_node)
    workflow.add_node("search",node_config.tavily_search_node)
    workflow.add_node("generate",node_config.generate_answer_node)

    #设置线性流程
    workflow.add_edge(START,"understand")
    workflow.add_edge("understand","search")
    workflow.add_edge("search","generate")
    workflow.add_edge("generate",END)

    memory = InMemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app

if __name__ == "__main__":
    # 1. 初始化智能体
    print("🔍 智能搜索助手启动！")
    print("我会使用Tavily API为您搜索最新、最准确的信息")
    print("支持各种问题：新闻、技术、知识问答等")
    print("(输入 'quit' 退出)")
    
    try:
        app = creat_search_assistant_graph()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
    # 配置线程ID（用于记忆上下文）
    config = {"configurable": {"thread_id": "session_1"}}
    print(f"智能体流程图:\n{app.get_graph().draw_ascii()}")
    while True:
        # 2. 获取用户输入
        try:
            user_input = input("\n🤔 您想了解什么: ")
        except KeyboardInterrupt:
            print("\n程序中断")
            break

        if not user_input.strip():
            continue
            
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 再见！")
            break

        print("\n" + "="*60)

        # 构造初始状态
        input_state = {
            "messages": [HumanMessage(content=user_input)]
        }

        # 3. 核心部分：流式运行图 (Streaming)
        # app.stream 会返回一个生成器，每当一个节点运行完，就会产生一个 event
        try:
            for event in app.stream(input_state, config=config):
                
                # --- 阶段 1: 理解节点完成 ---
                if "understand" in event:
                    # 获取 understand 节点返回的消息
                    last_msg = event["understand"]["messages"][-1]
                    content = last_msg.content
                    # 简单处理一下换行，让显示更紧凑
                    display_content = content.replace('\n', ' ').strip()
                    print(f"🧠 理解阶段: {display_content}")
                    
                    # 模拟一下“正在搜索”的动态效果（根据理解的内容）
                    # 实际搜索词通常包含在 content 里
                    print(f"🔍 正在搜索: {user_input[:10]}...") 

                # --- 阶段 2: 搜索节点完成 ---
                elif "search" in event:
                    # search 节点通常返回 ToolMessage 或更新后的状态
                    # 这里我们只需要提示用户搜索完成了
                    print("🔍 搜索阶段: ✅ 搜索完成！找到了相关信息，正在为您整理答案...")

                # --- 阶段 3: 生成回答节点完成 ---
                elif "generate" in event:
                    # 获取最终生成的回答
                    final_answer = event["generate"]["messages"][-1].content
                    print(f"\n💡 最终回答:\n{final_answer}")

        except Exception as e:
            print(f"❌ 运行过程中发生错误: {e}")

        print("\n" + "="*60)
