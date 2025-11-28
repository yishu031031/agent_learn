from typing import Dict,Any  #Any 表示“任意类型”
from .search_tool import search
'''
封装工具类
'''

class ToolExecutor:
    '''
    工具执行器，负责管理和执行工具
    '''
    def __init__(self):
        self.tools:Dict[str,Dict[str,Any]] = {} #存储工具的字典,第一个str是工具名，第二个Dict存储工具的属性，如函数、描述等

    def register_tool(self,name:str,description:str,func:callable): #callable是指可以被调用的对象
        '''
        向工具箱中注册一个新工具
        '''
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在，正在覆盖。")
        self.tools[name] = {
            "descirption":description,
            "function":func
        }
        print(f"工具{name}已注册")

    
    def get_tool(self,name:str)->callable:
        '''
        根据名称获取一个工具的执行函数
        '''
        return self.tools.get(name,{}).get("function")
    
    def getAvailableTools(self)->Dict[str,str]:
        '''
        获取所有已注册工具的名称和描述
        '''
        return "\n".join([
            f"{name}: {info['descirption']}"
        for name,info in self.tools.items()
        ])
        

#测试
if __name__ == '__main__':
    # 1.初始化工具执行器类
    toolExecutor = ToolExecutor() 

    # 2.注册搜索工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"

    toolExecutor.register_tool("Search",search_description,search)

    #3. 打印可以调用的工具
    available_tools = toolExecutor.getAvailableTools()
    print("\n----可用的工具------")
    print(available_tools)

    #4.智能体如何调用工具
    print("\n---- 执行Action:Search['郧阳中学在哪'] ---")
    tool_name = 'Search'
    tool_input = "郧阳中学在哪"

    tool_function = toolExecutor.get_tool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("----观察(Observation)----")
        print(observation)
    else:
        print(f"错误，未找到{tool_name}的工具")





    
            
