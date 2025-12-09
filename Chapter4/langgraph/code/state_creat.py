from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages

class SearchState(TypedDict):
    messages: Annotated[list, add_messages]
    '''
    在标准的 Python 语法中，Annotated 的定义结构是： Annotated[T, x]
    
    T (类型): 这是真正的变量类型（例如 list, int, str）。静态类型检查工具（如 MyPy）只会看这里，把变量当作 T 处理。

    x (元数据): 这是附加的“元数据”（Metadata）。Python 本身通常会忽略它，但是，第三方框架（比如 LangGraph, FastAPI）可以在代码运行时读取这个“元数据”来执行特殊的逻辑
    
    在这个例子中，messages 被定义为一个 list 类型的变量（T 是 list），但是它还附加了一个元数据 add_messages。这意味着：
    - 静态类型检查工具会把 messages 当作一个普通的 list 来处理
    - LangGraph 会在运行时自动处理 messages 的添加、删除、合并等操作，确保状态的一致性
    '''
    user_query:str   # 经过LLM理解后的用户需求总结
    search_query:str  # 优化后用于Tavily API的搜索查询
    search_results:str # Tavily搜索返回的结果
    final_answer:str  # 最终生成的答案
    step:str  # 标记当前步骤

    '''
    我们创建了 SearchState 这个 TypedDict，为状态对象定义了一个清晰的数据模式（Schema）。
    一个关键的设计是同时包含了 user_query 和 search_query 字段。
    这允许智能体先将用户的自然语言提问，优化成更适合搜索引擎的精炼关键词，从而显著提升搜索结果的质量。
    '''