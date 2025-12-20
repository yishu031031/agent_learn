"""
多Agent协作的智能文档助手

使用两个SimpleAgent分工协作：
- Agent1：GitHub搜索专家
- Agent2：文档生成专家
"""

import os
from dotenv import load_dotenv
from hello_agents import SimpleAgent,HelloAgentsLLM