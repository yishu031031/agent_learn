import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

# 首先加载环境变量
load_dotenv(override=True)

class LLMConfig:
    def __init__(self):
        '''
        __init__ 的 Docstring
        
        :param self: 说明
        model = ChatOpenAI(
            model="...",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # api_key="...",
            # base_url="...",
            # organization="...",
            # other params...
        )
        '''

        self.llm = ChatOpenAI(
            model = os.getenv("LLM_MODEL_ID","gpt-4o"),
            api_key = os.getenv("LLM_API_KEY"),
            base_url = os.getenv("LLM_BASE_URL","https://api.example-llm.com/v1"),
            temperature=0.7,
        )

        self.tavily_client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))
