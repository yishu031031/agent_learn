from openai import OpenAI

class LLM:
    '''
    LLM 的 Docstring
    ''' 
    def __init__(self,model:str,api_key:str,base_url:str):
        self.model = model
        self.client = OpenAI(api_key=api_key,base_url=base_url)

    def generate_text(self,prompt:str,system_prompt:str)->str:
        '''调用LLM来生成回应'''
        print("loading...正在调用LLM")
        try:
            messages = [
                {"role":'system','content':system_prompt},
                {'role':'user','content':prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
                temperature=0.5,
            )
            answer = response.choices[0].message.content
            print("LLM调用成功")
            return answer
        except Exception as e:
            print(f"LLM调用失败: {e}")
            return f"错误: LLM调用失败 - {e}"