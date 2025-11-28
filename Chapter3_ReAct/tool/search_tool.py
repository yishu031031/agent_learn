from serpapi import SerpApiClient
import os
from dotenv import load_dotenv
import json

load_dotenv(override=True)


def _pretty_json(data):
    """
    将字典格式化为漂亮的 JSON 字符串并打印
    """
    pretty_str = json.dumps(
        data, 
        indent=4,              # 缩进4个空格，形成层级
        ensure_ascii=False,    # 关键！设为 False 才能正常显示中文，否则会显示 \u6771 这种乱码
        sort_keys=False        # 是否按键名排序，通常 False 保持原样更好读
    )
    return pretty_str

def __dec__():
    '''
    这里添加search工具的描述
    '''
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    return search_description

def search(query:str)->str:
    '''
    一个基于Serpapi的网页搜索引擎工具
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息
    '''
    print(f"正在执行[SerpApi]网页搜索: {query}")
    try:
        api_key = os.getenv("SEARCH_API_KEY")
        if not api_key:
            return "错误：缺少SEARCH_API_KEY环境变量，请检查配置"
        
        params = {
            "engine": "google",
            "q":query,
            "api_key":api_key,
            "gl":"cn",
            "hl":"zh-cn",
        }

        client = SerpApiClient(params)
        results = client.get_dict()
        #results = _pretty_json(results)
        #查看results的结构以确定如何提取信息
        #print(f"搜索结果获取成功，正在解析响应:{results}")
        #智能解析: 优先返回直接答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        
        return f"对不起，没有找到关于 '{query}' 的信息。"
        '''
        在上述代码中，首先会检查是否存在 answer_box（Google的答案摘要框）或 knowledge_graph（知识图谱）等信息，如果存在，就直接返回这些最精确的答案。如果不存在，它才会退而求其次，返回前三个常规搜索结果的摘要。这种“智能解析”能为LLM提供质量更高的信息输入。
        '''
    except Exception as e:
        return f"搜索时发生错误: {str(e)}"



#测试：
if __name__ == "__main__":
    query = "东南大学是985吗？"
    answer = search(query)
    #print(answer)


