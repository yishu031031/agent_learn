import os
from typing import Optional,List,Dict,Any
from hello_agents import ToolRegistry

class MyAdvancedSearch:
    def __init__(self,name:str="MyAdvancedSearch",description:str="一个高级搜索引擎，可以搜索互联网上的信息"):
        self.name = name
        self.description = description
        self.search_sources = []
        self._setup_search_sources()

    def _setup_search_sources(self):
        """设置可用的搜索源"""
        # 检查Tavily可用性
        if os.getenv("TAVILY_API_KEY"):
            try:
                from tavily import TavilyClient
                self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
                self.search_sources.append("tavily")
                print("✅ Tavily搜索源已启用")
            except ImportError:
                print("⚠️ Tavily库未安装")

        # 检查SerpApi可用性
        if os.getenv("SEARCH_API_KEY"):
            try:
                import serpapi
                self.search_sources.append("serpapi")
                print("✅ SerpApi搜索源已启用")
            except ImportError:
                print("⚠️ SerpApi库未安装")

        if self.search_sources:
            print(f"🔧 可用搜索源: {', '.join(self.search_sources)}")
        else:
            print("⚠️ 没有可用的搜索源，请配置API密钥")

    def search(self,query:str)->str:
        '''
        执行搜索操作，根据可用源选择最合适的搜索方式
        '''
        if not query.strip():
            return "错误：搜索查询不能为空"

        #检查是否有可用的搜索源
        if not self.search_sources:
            return "错误：没有可用的搜索源，请配置API密钥"

        print(f"正在执行搜索: {query}")

        for source in self.search_sources:
            if source == "tavily":
                result = self._search_with_tavily(query)
                if result and "未找到" not in result:
                    return f"📊 Tavily AI搜索结果:\n\n{result}"
            
            elif source == "serpapi":
                result = self._search_with_serpapi(query)
                if result and "未找到" not in result:
                    return f"🌐 SerpApi Google搜索结果:\n\n{result}"

        return "对不起，没有找到关于 '{query}' 的信息。"

    def _search_with_tavily(self, query: str) -> str:
            """使用Tavily搜索"""
            response = self.tavily_client.search(query=query, max_results=3)

            if response.get('answer'):
                result = f"💡 AI直接答案:{response['answer']}\n\n"
            else:
                result = ""

            result += "🔗 相关结果:\n"
            for i, item in enumerate(response.get('results', [])[:3], 1):
                result += f"[{i}] {item.get('title', '')}\n"
                result += f"    {item.get('content', '')[:150]}...\n\n"

            return result

    def _search_with_serpapi(self, query: str) -> str:
        """使用SerpApi搜索"""
        import serpapi

        search = serpapi.GoogleSearch({
            "q": query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 3
        })

        results = search.get_dict()

        result = "🔗 Google搜索结果:\n"
        if "organic_results" in results:
            for i, res in enumerate(results["organic_results"][:3], 1):
                result += f"[{i}] {res.get('title', '')}\n"
                result += f"    {res.get('snippet', '')}\n\n"

        return result


def create_advanced_search_registry():
    registry = ToolRegistry()
    search_tool = MyAdvancedSearch()
    registry.register_function(
        name=search_tool.name,
        description=search_tool.description,
        func=search_tool.search
    )
    return registry

    