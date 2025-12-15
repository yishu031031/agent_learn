import os
from typing import Optional
from openai import OpenAI
from hello_agents import HelloAgentsLLM

'''
通过继承HelloAgentsLLM,从而增加对ModelScope平台的支持
学会扩展框架，不仅仅是使用框架
'''

class QhLLM(HelloAgentsLLM):
    '''
    一个自定义的LLM客户端,通过继承增加对ModelScope的支持
    首先重写__init__方法,我们的目标是：当用户传入 provider="modelscope" 时，
    执行我们自定义的逻辑；否则，就调用父类 HelloAgentsLLM 的原始逻辑，使其能够继续支持 OpenAI 等其他内置的供应商。
    这段代码展示了“重写”的思想：
    我们拦截了 provider="modelscope" 的情况并进行了特殊处理，对于其他所有情况，则通过 super().__init__(...) 交还给父类，保留了原有框架的全部功能
    '''
    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider: Optional[str] = "auto", 
        #Optional[str] 表示该参数可以是 str 或 None
        #调用时不传 provider 时，默认使用 "auto"
        **kwargs,
        ):

        #检查provider是否为'modelscope'
        if provider == "modelscope":
            print("正在使用自定义的ModelScope Provider")

            #解析ModelScope的凭证
            self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY")
            self.base_url = base_url or "https://api-inference.modelscope.cn/v1/"

            if not self.api_key:
                raise ValueError("ModelScope API Key 未配置，请检查环境变量 MODELSCOPE_API_KEY")

            #设置默认模型和其他参数
            self.model = model or os.getenv("LLM_MODEL_ID") or "Qwen/Qwen2.5-VL-72B-Instruct"
            self.temperature = kwargs.get('temperature', 0.7)
            self.max_tokens = kwargs.get('max_tokens', 500)
            self.timeout = kwargs.get('timeout', 60)

            #使用获取的参数创建OpenAI客户端

            self._client = OpenAI(api_key=self.api_key,base_url=self.base_url,timeout=self.timeout)#这里无需传递model，是在创建连接
            '''
            调用代码：
            response = self._client.chat.completions.create(
                model=self.model,  # ← model 在这里传入！
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens']}
            )
            '''
        else:
            super().__init__(model,api_key,base_url,provider,**kwargs)
            # - self._client 已创建
            # - self.model 已设置
            # - self.api_key 已设置
            # - 所有父类的功能都可以使用

