# my_simpleagent.py
import re
from typing import Optional,Iterator
from hello_agents import SimpleAgent,HelloAgentsLLM,Message,Config,ToolRegistry

class MysimpleAgent(SimpleAgent):
    """
    重写的简单对话Agent
    展示如何基于框架基类构建自定义Agent
    """
    def __init__(
        self,
        name:str,
        llm:HelloAgentsLLM,
        system_prompt:Optional[str]=None,
        config:Optional[Config]=None,
        tool_registry:Optional[ToolRegistry]=None,
        enable_tool_calling:bool=True
    ):
        super().__init__(name, llm, system_prompt, config)
        self.tool_registry = tool_registry
        self.enable_tool_calling = enable_tool_calling and tool_registry is not None #确保能够调用工具
        print(f"{name} agent 初始化完成，工具调用:{'启用' if self.enable_tool_calling else '禁用'}")

    def run(self,input_text:str,max_tool_iterations:int = 3,**kwargs)->str:
        """
        重写运行方法:实现简单对话逻辑，支持可选工具调用
        """
        print(f"[开始执行]\n {self.name} 正在处理用户输入:\n{input_text}")

        #构建消息列表
        message = []

        #添加系统信息(可以包含工具信息)
        enhanced_system_prompt = self._get_enhanced_system_prompt()
        if enhanced_system_prompt:  # 只有当系统提示词不为空时才添加
            message.append({"role":"system","content":enhanced_system_prompt})

        #访问历史信息并添加至message
        for msg in self._history:
            '''
            self._history.append(message) 说明_history是一个列表，列表中存储的是Message对象
            Message对象的role属性是字符串，表示消息的角色，如"user"、"assistant"、"system"等
            Message对象的content属性是字符串，表示消息的内容
            '''
            message.append({"role":msg.role,"content":msg.content})

        #添加当前用户信息
        message.append({"role":"user","content":input_text})

        #如果没有工具调用，调用简单对话逻辑
        if not self.enable_tool_calling:
            # think() 返回生成器，invoke() 返回字符串
            response = self.llm.invoke(message)
            self.add_message(Message(role="user",content=input_text))
            self.add_message(Message(role="assistant",content=response))
            return response
        
        # 如果有工具调用，使用工具调用逻辑
        return self._run_with_tools(message, input_text, max_tool_iterations, **kwargs)

    def stream_run(self, input_text: str, **kwargs) -> Iterator[str]:
        """
        自定义的流式运行方法
        """
        print(f"🌊 {self.name} 开始流式处理: {input_text}")

        messages = []

        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        for msg in self._history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": input_text})

        # 流式调用LLM
        full_response = ""
        print("📝 实时响应: ", end="")
        for chunk in self.llm.stream_invoke(messages, **kwargs):
            full_response += chunk
            print(chunk, end="", flush=True)
            yield chunk

        print()  # 换行

        # 保存完整对话到历史记录
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(full_response, "assistant"))
        print(f"✅ {self.name} 流式响应完成")

    def _get_enhanced_system_prompt(self)->str:
        '''
        获取增强后的系统提示词
        根据历史信息和当前需求，生成更精确的系统提示词,包含工具信息
        '''
        base_prompt = self.system_prompt or "你是一个有用的AI助手"

        if not self.enable_tool_calling or not self.tool_registry:
            return base_prompt #没有工具调用或工具注册，直接返回原始系统提示词

        #获取工具描述
        tool_desc = self.tool_registry.get_tools_description()
        if not tool_desc or tool_desc == "暂无可以调用工具":
            return base_prompt #没有工具描述，直接返回原始系统提示词

        tools_section = "\n\n## 可用工具\n"
        tools_section += "你可以使用以下工具来帮助回答问题:\n"
        tools_section += tool_desc + "\n"

        tools_section += "\n## 工具调用格式\n"
        tools_section += "当需要使用工具时，请使用以下格式:\n"
        tools_section += "`[TOOL_CALL:{tool_name}:{parameters}]`\n"
        tools_section += "例如:`[TOOL_CALL:search:Python编程]` 或 `[TOOL_CALL:memory:recall=用户信息]`\n\n"
        tools_section += "工具调用结果会自动插入到对话中，然后你可以基于结果继续回答。\n"

        return base_prompt + tools_section

    def _run_with_tools(self,message:list,input_text:str,max_tool_iterations:int = 3,**kwargs)->str:
        '''
        支持工具调用的运行逻辑
        1.设置最大调用次数和最终答案
        2.进入多次问答循环，每次执行得到带工具标签的结果后进入第二层循环
        3.第二层循环中，解析工具标签，调用工具并获取结果

        '''
        current_iteration = 0
        final_response = None
        
        while current_iteration < max_tool_iterations:
            response = self.llm.invoke(message)  # 直接获得结果

            #检查是否有工具调用
            tool_calls = self._parse_tool_calls(response)

            if tool_calls:
                '''
                检测到有工具调用
                '''
                print(f"检测到{len(tool_calls)}个工具调用")

                tool_results = []  # 存储工具调用结果
                clean_response = response

                for tool_call in tool_calls:
                    result = self._execute_tool_call(tool_call['tool_name'], tool_call['params'])
                    tool_results.append(result)
                    # 从响应中移除工具调用标记
                    clean_response = clean_response.replace(tool_call['original_tool_call'], "")
                
                #构建包含工具调用结果的信息
                message.append({"role": "assistant", "content": clean_response})

                # 添加工具结果
                tool_results_text = "\n\n".join(tool_results)
                message.append({"role": "user", "content": f"工具执行结果:\n{tool_results_text}\n\n请基于这些结果给出完整的回答。"})

                current_iteration += 1
                continue
            
            # 没有工具调用
            final_response = response
            break
        
        # 如果超过最大迭代次数，获取最后一次回答
        if current_iteration >= max_tool_iterations and not final_response:
            final_response = self.llm.invoke(message, **kwargs)

        # 保存到历史记录
        self.add_message(Message(role="user",content=input_text))
        self.add_message(Message(role="assistant",content=final_response))
        print(f"✅ {self.name} 响应完成")
        return final_response

    def _parse_tool_calls(self,response:str)->list:
        '''
        解析文本中的工具调用标签
        '''
        pattern = r'\[TOOL_CALL:([^:]+):([^\]]+)\]'
        matches = re.findall(pattern,response)

        tool_calls = []

        for tool_name,params in matches:
            tool_calls.append({
                'tool_name':tool_name,
                'params':params,
                'original_tool_call':f"[TOOL_CALL:{tool_name}:{params}]",
            })

        return tool_calls

    def _execute_tool_call(self,tool_name:str,params:str)->str:
        '''
        执行工具调用
        '''
        if not self.enable_tool_calling or not self.tool_registry:
            return f"错误:工具调用未启用或工具注册不存在"

        try:
            tool = self.tool_registry.get_tool(tool_name) #获取Tool对象
            param_dict = self._parse_tool_parameters(tool_name,params) #解析工具参数
            if not tool:
                return f"错误:未找到工具{tool_name}"
            result = tool.run(param_dict) #执行工具
            return result
        except Exception as e:
            return f"错误:执行工具{tool_name}失败: {str(e)}"
        

    
    
    def _parse_tool_parameters(self, tool_name: str, parameters: str) -> dict:
        """智能解析工具参数"""
        param_dict = {}

        if '=' in parameters:
            # 格式: key=value 或 action=search,query=Python
            if ',' in parameters:
                # 多个参数:action=search,query=Python,limit=3
                pairs = parameters.split(',')
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        param_dict[key.strip()] = value.strip()
            else:
                # 单个参数:key=value
                key, value = parameters.split('=', 1)
                param_dict[key.strip()] = value.strip()
        else:
            # 直接传入参数，根据工具类型智能推断
            if tool_name == 'search':
                param_dict = {'query': parameters}
            elif tool_name == 'memory':
                param_dict = {'action': 'search', 'query': parameters}
            else:
                param_dict = {'input': parameters}

        return param_dict

    def add_tool(self,tool) -> None:
        '''
        添加工具到Agent
        '''
        if not self.tool_registry:
            self.tool_registry = ToolRegistry()
            self.enable_tool_calling = True
        
        self.tool_registry.register_tool(tool)
        print(f"✅ 工具{tool.name}已添加到Agent")

    def has_tool(self) -> bool:
        '''
        检查是否有工具可用
        '''
        return self.enable_tool_calling and self.tool_registry is not None

    def remove_tool(self,tool_name:str) -> None:
        '''
        移除工具
        '''
        if not self.tool_registry:
            return
        self.tool_registry.unregister(tool_name)
        print(f"🗑️ 工具{tool_name}已移除")
        
    def list_tools(self) -> list:
        '''
        列出所有工具
        '''
        if not self.tool_registry:
            return []
        return self.tool_registry.list_tools()
    
    

        




    


        





        