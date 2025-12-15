"""消息系统"""
from typing import Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel

# 定义消息角色的类型，限制其取值
MessageRole = Literal["user", "assistant", "system", "tool"] #类型声明

'''
Literal 是 Python 的类型注解工具，用于限制变量只能是几个特定的字面量值之一。
'''

class Message(BaseModel):
    """消息类"""
    '''
    BaseModel 来自 pydantic，是一个数据验证框架，可以：
        自动验证数据类型
        自动类型转换
        提供清晰的错误信息
        支持 JSON 序列化/反序列化
    继承 BaseModel 后，创建 Message 实例时会自动验证 content 必须是字符串，role 必须是 "user"、"assistant"、"system" 或 "tool" 之一，提高了代码的健壮性和可维护性。
    '''
    content: str
    role: MessageRole
    timestamp: datetime = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __init__(self, content: str, role: MessageRole, **kwargs):
        super().__init__(
            content=content,
            role=role,
            timestamp=kwargs.get('timestamp', datetime.now()),
            metadata=kwargs.get('metadata', {})
        )
        '''
        除了 content 和 role 这两个核心字段外，我们还增加了 timestamp 和 metadata，为日志记录和未来功能扩展预留了空间。
        '''
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式（OpenAI API格式）"""
        return {
            "role": self.role,
            "content": self.content
        }
    
    def __str__(self) -> str:
        return f"[{self.role}] {self.content}"
