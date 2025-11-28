import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List,Dict

#加载.env文件中的环境变量
load_dotenv(override=True)
llm_api_key = os.getenv("LLM_API_KEY")
llm_baseurl = os.getenv("LLM_API_BASE_URL","https://api.example-llm.com/v1")
print(f"使用的LLM API Key:{llm_api_key}，API地址: {llm_baseurl}")

#封装基础LLM调用函数
class AgentLLM:
    '''
    封装LLM交互逻辑
    它用于调用任何兼容OpenAI接口的服务
    '''
    def __init__(self,model:str=None,apiKey:str=None,baseurl:str=None,timeout:int=None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseurl = baseurl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_API_TIMEOUT",60))

        if not all([self.model,apiKey,baseurl]): #检查列表中是否有None或空值
            raise ValueError("缺少必要的LLM配置信息，请检查环境变量设置")
        
        self.client = OpenAI(api_key=apiKey,base_url=baseurl,timeout=timeout)

    def think(self,messages:List[Dict[str,str]],temperature:float=0):
        '''
        调用大语言模型并进行思考，返回响应
        '''
        print(f"正在调用{self.model}模型...")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,#流式响应，有输出就返回一个块
            )   
            '''
            流式响应输出示例：
            Chunk(
                id='chatcmpl-123',
                choices=[{
                    'delta': {'role': 'assistant'},  # 注意：这里没有 content，或者 content is None
                    'finish_reason': None
                }]
            )
            
            Chunk(
                id='chatcmpl-123',
                choices=[{
                    'delta': {'content': '你'},     # 注意：这里只有“你”，没有“好”
                    'finish_reason': None
                }]
            )
            '''
            #处理流失响应
            print("LLM响应:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or "" #字典提取
                if content:
                    #print(content,end="",flush=True)
                    collected_content.append(content)
            print() #流式输出结束后换行

            return "".join(collected_content)#最后把列表所有打印合并为整个输出
            
        except Exception as e:
            print(f"调用LLM模型时出错: {e}")
            return None
        

#测试代码
if __name__ == "__main__":
    try:
        llmClient = AgentLLM()

        messages = [
            {"role":"system","content":"you are a helpful assistant."},
            {"role":"user","content":"你好！请介绍一下你自己。"},
        ]
        print("LLM思考结果:")
        response = llmClient.think(messages)
        if response:
            print("LLM完整响应内容:")
            print(response)
    except ValueError as e:
        print(f"配置错误: {e}")


    