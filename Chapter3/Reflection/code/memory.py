'''
Reflection 的核心在于迭代，而迭代的前提是能够记住之前的尝试和获得的反馈。因此，一个“短期记忆”模块是实现该范式的必需品。这个记忆模块将负责存储每一次“执行-反思”循环的完整轨迹。
'''
from typing import List,Dict,Any,Optional

class Memory:
    '''
    短期记忆模块，用于存储智能体的行动与反思轨迹
    '''
    def __init__(self):
        '''
        初始化一个空的列表来存储所有记录
        '''
        self.records:List[Dict[str,Any]] = []
        '''
        举例说明records内容：
        self.records = [
            # 第一条记录：第1步的操作
            {
                "step_index": 0,                    # 整数 (int)
                "action": "Google搜索",              # 字符串 (str)
                "query": "武大华科 2025 分数线",      # 字符串 (str)
                "status": "success",                # 字符串 (str)
                "output": "搜索结果: 630分...",      # 字符串 (str)
                "timestamp": 1716920000             # 浮点数 (float) -> 这就是为什么值是 Any
            },

            # 第二条记录：第2步的操作
            {
                "step_index": 1,
                "action": "Python代码计算",
                "code": "print(630 > 600)",
                "status": "error",
                "error_msg": "NameError: ...",      # 这一行只有出错时才有，体现了 Dict 的灵活性
                "retry_count": 1
            },

            # 第三条记录：第3步的操作 (Reflect后的重试)
            {
                "step_index": 1,
                "action": "Python代码计算(修正版)",
                "code": "score = 630; print(score)",
                "status": "success",
                "output": "630"
            }
        ]
        '''

    def add_record(self,record_type:str,content:str):
        '''
        向记忆中添加一条新纪录

        参数：
        - record_type (str): 记录的类型 ('execution' 或 'reflection')。
        - content (str): 记录的具体内容 (例如，生成的代码或反思的反馈)。
        '''
        record = {
            "type":record_type,
            "content":content,
        }
        self.records.append(record)
        print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")


    def get_trajector(self)->str:
        '''
        将所有记忆记录格式化为一个连贯的字符串文本，用于后续构建提示词
        '''
        trajectory_parts = []
        for record in self.records:
            if record['type'] == 'execution':#执行记录
                trajectory_parts.append(f"--- 上一轮尝试 ---\n{record['content']}")
            elif record['type'] == 'reflection':
                trajectory_parts.append(f"--- 评审员反馈 ---\n{record['content']}")
        
        return "\n\n".join(trajectory_parts)
    
    def get_last_execution(self) -> Optional[str]: #Optional[str]指返回的这个变量，要么是一个字符串（String），要么什么都不是（None）。
        """
        获取最近一次的执行结果 (例如，最新生成的代码)。
        如果不存在，则返回 None。
        """
        for record in reversed(self.records):
            if record['type'] == 'execution':
                return record['content']
        return None
    