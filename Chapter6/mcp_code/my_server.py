# 文件名: server.py
from fastmcp import FastMCP

# 1. 创建 MCP 服务
mcp = FastMCP("MathHelper")

# 2. 定义工具：加法
@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的和"""
    return a + b

# 3. 定义工具：复杂的字符串处理（模拟业务逻辑）
@mcp.tool()
def analyze_data(text: str) -> str:
    """分析文本数据的长度和单词数"""
    length = len(text)
    words = len(text.split())
    return f"数据分析报告: 文本长度={length}, 单词数={words}"

if __name__ == "__main__":
    # 默认使用 stdio 模式运行（这是 Agent 调用的标准方式）
    mcp.run()