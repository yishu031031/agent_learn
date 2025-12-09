from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from state_creat import SearchState
from config import LLMConfig

class NodeConfig:
    def __init__(self):
        self.llm = LLMConfig().llm
        self.tavily_client = LLMConfig().tavily_client

    def understand_query_node(self,state:SearchState)->dict:
        '''
        步骤1：理解用户查询并生成搜索关键词
        该节点通过一个结构化的提示，要求 LLM 同时完成“意图理解”和“关键词生成”两个任务，并将解析出的专用搜索关键词更新到状态的 search_query 字段中，为下一步的精确搜索做好准备。
        '''
        user_message = state['messages'][-1].content  # 获取用户的最新消息内容

        understand_prompt = f"""你是一个智能助理。请阅读以下用户的查询，并将其优化为适合搜索引擎使用的关键词或短语。
            分析用户查询: "{user_message}"
            请根据用户查询完成以下两个任务：
            1.简洁总结用户想要了解什么
            2.生成最适合搜索引擎的关键词(中英文均可，需要准确)

            输出格式：
            理解:[用户需求总结]
            搜索词:[最佳搜索关键词]

            """
        '''
        Generate a response from the model:

        ```python
        messages = [
            (
                "system",
                "You are a helpful translator. Translate the user sentence to French.",
            ),
            ("human", "I love programming."),
        ]
        model.invoke(messages)
        ```
        '''
        #输出封装后的信息调试
        print(f"理解节点用户输入为:{[SystemMessage(content=understand_prompt)]}")
        response = self.llm.invoke([SystemMessage(content=understand_prompt)])
        print(f"理解节点LLM输出为:{response}")

        response_text = response.content

        # 解析输出并提取关键词
        search_query = ""
        if "搜索词" in response_text:
            try:
                search_query = response_text.split("搜索词:")[1].strip()
            except IndexError:
                search_query = ""
        if not search_query:
            search_query = user_message  # 回退到原始查询
        return {
            "user_query": response_text,
            "search_query": search_query,
            "step":"understand",
            "messages":[AIMessage(content=f"我将为您搜索:{search_query}")]
        }


    def tavily_search_node(self, state: SearchState) -> dict:
        """步骤2：使用Tavily API进行真实搜索"""
        # 确保 state 里有 search_query，如果没有则回退
        search_query = state.get('search_query', state['messages'][-1].content)
        
        try:
            print(f"正在搜索: {search_query}")
            
            # --- 修改开始 ---
            
            # 1. 初始化一个空列表，用来装所有的搜索结果条目
            all_results = [] 
            
            # 遍历每个关键词进行搜索
            for search_term in search_query.split(","):
                search_term = search_term.strip() # 去除可能存在的空格
                if not search_term: continue
                
                # 调用 API
                response = self.tavily_client.search(
                    query=search_term,
                    search_depth="basic",
                    max_results=3, # 稍微减少一点，避免合并后内容过长
                    include_answer=True,
                )
                
                # 获取本次搜索的 'results' 列表，并追加到总表中
                # response.get('results', []) 保证如果没搜到也不会报错
                results = response.get('results', [])
                if results:
                    all_results.extend(results)
            
            # 2. 现在 raw_content 是所有搜索结果的字符串表示
            raw_content = str(all_results)
            
            # --- 修改结束 ---

            search_process_prompt = f"""
            你是一个智能助理。以下是我从Tavily搜索引擎获取的与用户查询相关的信息：
            {raw_content}
            
            任务：
            请处理这些查询信息，提取出对用户最有帮助的内容，并生成一个简洁的总结。
            请直接输出总结内容。
            """

            # 3. 调用 LLM 进行总结
            search_process_response = self.llm.invoke(
                [SystemMessage(content=search_process_prompt)]
            )
            
            search_results = search_process_response.content.strip()
            
            if not search_results:
                search_results = "未能提取有用的信息。"

            return {
                "search_results": search_results, 
                "step": "searched",
                "messages": [AIMessage(content=f"✅ 搜索完成！相关信息提取完毕。")]
            }

        except Exception as e:
            print(f"搜索节点出错: {e}")
            import traceback
            traceback.print_exc() 
            return {
                "search_results": f"搜索时发生错误: {str(e)}",
                "step": "search failed",
                "messages": [AIMessage(content="❌ 搜索时发生错误。")]
            }
        
    def generate_answer_node(self,state:SearchState)->dict:
        '''
        步骤3：基于搜索结果生成最终答案
        '''
        if state['step'] == 'search failed':
            # 如果搜索失败，执行回退策略，基于LLM自身知识回答
            fallback_prompt = f"搜索API暂时不可用，请基于您的知识回答用户的问题：\n用户问题：{state['user_query']}"
            response = self.llm.invoke([SystemMessage(content=fallback_prompt)])
        else:
            answer_prompt = f"""
            基于以下搜索结果为用户提供完整、准确的答案：
                用户问题：{state['user_query']}
                搜索结果：\n{state['search_results']}
                请综合搜索结果，提供准确、有用的回答...
"""         
            response = self.llm.invoke([SystemMessage(content=answer_prompt)])

        return {
            "final_answer": response.content,
            "step": "completed",
            "messages": [AIMessage(content=response.content)]
        }




        
