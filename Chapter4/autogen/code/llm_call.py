import os
import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv(override=True)

def creat_client():
    '''
    creat_client 的 Docstring
    创建并返回一个 OpenAIChatCompletionClient 实例。
    '''

    return OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL_ID","gpt-4o"),
        base_url=os.getenv("LLM_BASE_URL","https://openrouter.ai/api/v1"),
        api_key=os.getenv("LLM_API_KEY", "your_api_key_here"),
    )

