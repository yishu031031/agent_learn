# 使用 FastMCP 构建 MCP 服务器

本指南将详细介绍如何使用 FastMCP 框架构建一个完整的 MCP（Model Context Protocol）服务器，并以天气查询服务作为实际案例。

## 什么是 FastMCP？

FastMCP 是一个基于 Python 的 MCP 服务器开发框架，它简化了 MCP 服务器的创建过程。通过 FastMCP，开发者可以：

- 快速定义工具（Tools）
- 提供资源（Resources）
- 创建提示模板（Prompts）
- 支持多种传输方式（Stdio、HTTP、SSE 等）

## 安装依赖

### 前置要求

- Python 3.10 或更高版本
- pip 或 uv 包管理器

### 安装 FastMCP

**方式 1：使用 pip 安装（推荐）**

```bash
pip install fastmcp
```

**方式 2：使用 uv 安装（更快）**

```bash
uv add fastmcp
```

**方式 3：从项目安装依赖**

```bash
pip install -r requirements.txt
```

### 验证安装

安装完成后，可以通过以下命令验证：

```bash
python -c "import fastmcp; print(fastmcp.__version__)"
```

## 核心思路

### 1. MCP 服务器架构

MCP 服务器采用三层架构：

```
用户/智能体 → MCP Client → MCP Server → 工具/资源
```

- **MCP Server**：提供工具和资源的服务端
- **MCP Client**：连接服务器并调用工具的客户端
- **工具（Tools）**：可执行的操作，如查询天气、读取文件等
- **资源（Resources）**：提供数据的只读接口
- **提示（Prompts）**：预定义的提示模板

### 2. MCP 三大核心能力详解

MCP 协议提供了三种核心能力，每种能力都有其独特的用途和使用场景。理解它们的区别对于构建高效的 MCP 服务器至关重要。

#### 2.1 工具（Tools）- 主动执行操作

**什么是工具？**

工具是 MCP 服务器提供的**可执行函数**，它们能够执行具体的操作并可能产生副作用（Side Effects）。工具是**主动的**，意味着它们会改变系统状态或执行实际操作。

**工具的特点：**

- ✅ **主动执行**：执行具体的操作（如发送邮件、创建文件、调用 API）
- ✅ **可能有副作用**：操作可能改变系统状态或外部世界
- ✅ **需要参数**：通常需要输入参数来执行操作
- ✅ **返回结果**：执行后返回操作结果或状态

**工具的使用场景：**

1. **API 调用**：查询天气、搜索信息、发送消息
2. **文件操作**：创建、修改、删除文件
3. **数据库操作**：插入、更新、删除数据
4. **系统操作**：执行命令、启动服务

**工具示例：**

```python
from fastmcp import FastMCP

mcp = FastMCP("示例服务器")

# 示例 1：天气查询工具（本项目的核心示例）
@mcp.tool()
def get_weather(city: str) -> str:
    """
    查询指定城市的天气信息。
    
    这是一个典型的工具示例：它主动调用外部 API，获取实时数据。
    
    Args:
        city: 城市名称
        
    Returns:
        天气信息字符串
    """
    import requests
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    data = response.json()
    temp = data['current_condition'][0]['temp_C']
    return f"{city}当前温度：{temp}°C"

# 示例 2：文件创建工具（有副作用）
@mcp.tool()
def create_file(filename: str, content: str) -> str:
    """
    创建新文件并写入内容。
    
    这个工具有明显的副作用：在文件系统中创建新文件。
    
    Args:
        filename: 文件名
        content: 文件内容
        
    Returns:
        操作结果
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"文件 {filename} 创建成功"

# 示例 3：数据库插入工具（有副作用）
@mcp.tool()
def add_user(name: str, email: str) -> str:
    """
    向数据库添加新用户。
    
    这个工具会改变数据库状态。
    
    Args:
        name: 用户姓名
        email: 用户邮箱
        
    Returns:
        操作结果
    """
    # 伪代码示例
    # db.insert("users", {"name": name, "email": email})
    return f"用户 {name} 添加成功"

# 示例 4：计算工具（无副作用，纯函数）
@mcp.tool()
def calculate(expression: str) -> float:
    """
    计算数学表达式。
    
    这是一个纯函数工具，没有副作用，但仍然是工具因为它执行了计算操作。
    
    Args:
        expression: 数学表达式字符串，如 "2+2"
        
    Returns:
        计算结果
    """
    return eval(expression)  # 注意：实际使用中应使用更安全的解析方法
```

**工具调用流程：**

```
用户请求 → LLM 分析 → 选择工具 → 调用工具 → 执行操作 → 返回结果 → LLM 生成回答
```

#### 2.2 资源（Resources）- 被动提供数据

**什么是资源？**

资源是 MCP 服务器提供的**只读数据接口**，它们用于向 LLM 提供上下文信息。资源是**被动的**，意味着它们只是提供数据，不会执行操作或产生副作用。

**资源的特点：**

- 📖 **只读访问**：只能读取数据，不能修改
- 📖 **被动提供**：不执行操作，只是提供信息
- 📖 **URI 标识**：每个资源有唯一的 URI（如 `file://path/to/file`）
- 📖 **上下文增强**：用于增强 LLM 的上下文理解

**资源的使用场景：**

1. **文件内容**：提供文件内容给 LLM 阅读
2. **配置信息**：提供系统配置、环境变量
3. **数据快照**：提供数据库快照、缓存数据
4. **文档内容**：提供文档、知识库内容

**资源示例：**

```python
from fastmcp import FastMCP
import json
import os

mcp = FastMCP("资源示例服务器")

# 示例 1：文件资源（提供文件内容）
@mcp.resource("file://config")
def get_config_file() -> str:
    """
    提供配置文件内容。
    
    这是一个资源示例：它被动地提供配置文件的内容，
    LLM 可以读取这些信息来了解系统配置。
    
    Returns:
        配置文件内容
    """
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return json.dumps({"error": "配置文件不存在"})

# 示例 2：环境变量资源
@mcp.resource("env://variables")
def get_environment_variables() -> str:
    """
    提供环境变量信息。
    
    LLM 可以通过这个资源了解当前环境配置。
    
    Returns:
        环境变量 JSON 字符串
    """
    env_vars = {
        "PYTHON_VERSION": os.getenv("PYTHON_VERSION", "unknown"),
        "API_KEY_SET": "yes" if os.getenv("API_KEY") else "no"
    }
    return json.dumps(env_vars, indent=2, ensure_ascii=False)

# 示例 3：支持的城市列表资源
@mcp.resource("weather://supported-cities")
def get_supported_cities() -> str:
    """
    提供支持查询天气的城市列表。
    
    这是一个静态资源，提供可用数据列表。
    
    Returns:
        城市列表 JSON 字符串
    """
    cities = {
        "热门城市": ["北京", "上海", "广州", "深圳"],
        "国际城市": ["New York", "London", "Tokyo", "Paris"],
        "总数": 8
    }
    return json.dumps(cities, ensure_ascii=False, indent=2)

# 示例 4：数据库快照资源
@mcp.resource("db://users-snapshot")
def get_users_snapshot() -> str:
    """
    提供用户数据快照。
    
    这是一个资源，提供数据的只读视图，不会修改数据库。
    
    Returns:
        用户数据 JSON 字符串
    """
    # 伪代码示例
    # users = db.query("SELECT name, email FROM users LIMIT 10")
    users = [
        {"name": "张三", "email": "zhangsan@example.com"},
        {"name": "李四", "email": "lisi@example.com"}
    ]
    return json.dumps(users, ensure_ascii=False, indent=2)
```

**资源访问流程：**

```
用户请求 → LLM 需要上下文 → 请求资源 → 服务器提供数据 → LLM 使用数据增强理解 → 生成回答
```

**工具 vs 资源的对比：**

| 特性 | 工具（Tools） | 资源（Resources） |
|------|--------------|------------------|
| **性质** | 主动执行 | 被动提供 |
| **副作用** | 可能有副作用 | 无副作用 |
| **用途** | 执行操作 | 提供数据 |
| **调用时机** | LLM 决定执行 | LLM 需要上下文时 |
| **示例** | 查询天气、创建文件 | 读取文件、获取配置 |

#### 2.3 提示（Prompts）- 引导对话模板

**什么是提示？**

提示是 MCP 服务器提供的**预定义对话模板**，它们帮助用户或 LLM 快速进入特定的工作模式。提示不是数据，也不是功能，而是**标准化的对话开场方式**。

**提示的特点：**

- 📝 **模板化**：预定义的文本模板
- 📝 **引导性**：引导 LLM 进入特定角色或任务
- 📝 **可参数化**：可以接受参数进行定制
- 📝 **可复用**：一次定义，多次使用

**提示的使用场景：**

1. **角色设定**：让 LLM 扮演特定角色（如数据分析师、代码审查员）
2. **任务模板**：提供标准化的任务描述模板
3. **工作流程**：定义多步骤任务的执行流程
4. **专业领域**：针对特定领域的专业提示

**提示示例：**

```python
from fastmcp import FastMCP

mcp = FastMCP("提示示例服务器")

# 示例 1：天气分析提示模板
@mcp.prompt()
def weather_analysis_prompt(city: str) -> str:
    """
    生成天气分析提示模板。
    
    这个提示会引导 LLM 扮演天气分析师的角色，
    并按照特定格式分析天气数据。
    
    Args:
        city: 要分析的城市名称
        
    Returns:
        格式化的提示文本
    """
    return f"""你是一名专业的天气分析师。请分析{city}的天气情况，并按照以下格式提供报告：

1. 当前天气状况
2. 温度分析（与历史平均对比）
3. 出行建议
4. 未来趋势预测

请使用专业的术语，并提供实用的建议。"""

# 示例 2：代码审查提示模板
@mcp.prompt()
def code_review_prompt(language: str = "Python") -> str:
    """
    生成代码审查提示模板。
    
    这个提示引导 LLM 进行代码审查。
    
    Args:
        language: 编程语言
        
    Returns:
        代码审查提示
    """
    return f"""你是一名资深的{language}代码审查专家。请对提供的代码进行审查，重点关注：

1. **代码质量**：可读性、可维护性
2. **性能问题**：潜在的效率问题
3. **安全性**：安全漏洞和风险
4. **最佳实践**：是否符合{language}最佳实践
5. **改进建议**：具体的优化建议

请提供详细、建设性的反馈。"""

# 示例 3：数据分析提示模板
@mcp.prompt()
def data_analysis_prompt(dataset_name: str, analysis_type: str = "exploratory") -> str:
    """
    生成数据分析提示模板。
    
    Args:
        dataset_name: 数据集名称
        analysis_type: 分析类型（exploratory, statistical, predictive）
        
    Returns:
        数据分析提示
    """
    analysis_instructions = {
        "exploratory": "进行探索性数据分析，包括数据分布、异常值检测、相关性分析",
        "statistical": "进行统计分析，包括假设检验、置信区间、统计显著性",
        "predictive": "进行预测分析，包括特征工程、模型选择、预测评估"
    }
    
    return f"""你是一名数据科学家，正在分析数据集：{dataset_name}

分析类型：{analysis_type}
分析要求：{analysis_instructions.get(analysis_type, "综合分析")}

请按照以下步骤进行分析：
1. 数据概览和基本统计
2. 数据质量检查
3. 深入分析（根据分析类型）
4. 可视化建议
5. 结论和建议

请提供专业、详细的分析报告。"""

# 示例 4：多步骤任务提示模板
@mcp.prompt()
def project_setup_prompt(project_type: str, framework: str) -> str:
    """
    生成项目设置提示模板。
    
    这个提示引导 LLM 执行多步骤的项目设置任务。
    
    Args:
        project_type: 项目类型（web, api, cli等）
        framework: 使用的框架
        
    Returns:
        项目设置提示
    """
    return f"""你是一名经验丰富的{framework}开发者。请帮助设置一个{project_type}项目。

请按照以下步骤执行：

步骤 1：项目结构规划
- 分析项目需求
- 设计目录结构
- 确定依赖关系

步骤 2：初始化项目
- 创建必要的文件和目录
- 配置开发环境
- 设置版本控制

步骤 3：核心功能实现
- 实现主要功能模块
- 添加必要的工具函数
- 编写配置文件

步骤 4：测试和文档
- 编写单元测试
- 创建README文档
- 添加使用示例

请逐步执行，并在每个步骤完成后等待确认。"""
```

**提示使用流程：**

```
用户选择提示 → 提示模板被填充 → 发送给 LLM → LLM 按照提示执行任务
```

**工具、资源、提示的协同使用：**

在实际应用中，这三种能力经常协同工作：

```python
# 一个完整的示例：结合工具、资源和提示

@mcp.prompt()
def comprehensive_weather_report(city: str) -> str:
    """
    综合天气报告提示：结合使用工具和资源
    """
    return f"""请为{city}生成一份综合天气报告。

首先，使用 get_weather 工具获取当前天气。
然后，读取 weather://supported-cities 资源了解支持的城市。
最后，使用 get_weather_detailed 工具获取详细信息。

请按照以下格式组织报告：
1. 当前天气概况
2. 详细气象数据
3. 与其他城市对比（如果资源中有数据）
4. 出行建议"""
```

### 3. FastMCP 开发流程详解

使用 FastMCP 开发 MCP 服务器的基本流程：

1. **初始化服务器**
   ```python
   from fastmcp import FastMCP
   mcp = FastMCP("服务器名称")
   ```

2. **定义工具函数**
   ```python
   @mcp.tool()
   def my_tool(param: str) -> str:
       """工具描述"""
       # 工具实现
       return result
   ```

3. **运行服务器**
   ```python
   if __name__ == "__main__":
       mcp.run()
   ```


## 天气查询服务器示例

本项目提供了一个完整的天气查询 MCP 服务器示例，展示了如何：

1. 使用 FastMCP 创建服务器
2. 定义天气查询工具
3. 处理错误和异常
4. 提供清晰的工具描述

### 服务器结构

```
MCP_Server/
├── intro.md                    # 本文档
├── weather_server.py           # 天气查询服务器
├── requirements.txt            # 依赖列表
├── test_server.py              # 测试脚本
└── huggingface_docker/         # HuggingFace Docker 部署示例
    ├── Dockerfile
    ├── README.md
    └── requirements.txt
```

### 核心代码解析

**1. 服务器初始化**

```python
from fastmcp import FastMCP

mcp = FastMCP("Weather MCP Server")
```

**2. 工具定义**

```python
@mcp.tool()
def get_weather(city: str) -> str:
    """
    获取指定城市的当前天气信息。
    
    Args:
        city: 城市名称，支持中文和英文
        
    Returns:
        包含天气状况和温度的字符串描述
    """
    # 实现逻辑
    pass
```

**3. 运行服务器**

```python
if __name__ == "__main__":
    mcp.run()
```

## 运行服务器

### 本地开发模式（Stdio）

```bash
python weather_server.py
```

### HTTP 模式

```bash
uvicorn weather_server:mcp.http_app --host 0.0.0.0 --port 8000
```

### 使用 MCP Client 连接

```python
from hello_agents.tools import MCPTool

# 连接到本地服务器
weather_tool = MCPTool(
    server_command=["python", "weather_server.py"]
)

# 使用工具
result = weather_tool.run({
    "action": "call_tool",
    "tool_name": "get_weather",
    "arguments": {"city": "北京"}
})
```

## 测试服务器

运行测试脚本验证服务器功能：

```bash
python test_server.py
```

## 部署到 HuggingFace Spaces

本项目提供了完整的 HuggingFace Docker 部署示例，详见 `huggingface_docker/` 文件夹。

### 部署步骤

1. 构建 Docker 镜像
2. 创建 HuggingFace Space
3. 上传代码和 Dockerfile
4. 配置环境变量（如需要）
5. 自动部署

详细说明请参考 `huggingface_docker/README.md`。

## 扩展功能详解

### 添加更多工具

工具是 MCP 服务器的核心功能。让我们看看如何添加不同类型的工具。

**示例 1：多天天气预报工具**

```python
@mcp.tool()
def get_weather_forecast(city: str, days: int = 3) -> str:
    """
    获取指定城市的多天天气预报。
    
    这个工具扩展了基本的天气查询功能，提供未来几天的天气预报。
    
    Args:
        city: 城市名称
        days: 预报天数（1-7天，默认3天）
        
    Returns:
        JSON 格式的天气预报数据，包含每天的温度、天气状况、降水概率等
        
    Examples:
        >>> get_weather_forecast("北京", days=5)
        '{"city": "北京", "forecast": [...]}'
    """
    import requests
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    data = response.json()
    
    # 提取未来几天的预报
    forecast = data['weather'][:days]
    result = {
        "city": city,
        "days": days,
        "forecast": [
            {
                "date": day['date'],
                "max_temp": day['maxtempC'],
                "min_temp": day['mintempC'],
                "condition": day['hourly'][0]['weatherDesc'][0]['value']
            }
            for day in forecast
        ]
    }
    return json.dumps(result, ensure_ascii=False, indent=2)
```

**示例 2：批量查询工具**

```python
@mcp.tool()
def get_multiple_cities_weather(cities: List[str]) -> Dict[str, str]:
    """
    批量查询多个城市的天气。
    
    这个工具展示了如何处理列表类型的参数。
    
    Args:
        cities: 城市名称列表，最多支持10个城市
        
    Returns:
        字典格式的结果，键为城市名，值为天气信息
    """
    if len(cities) > 10:
        return {"error": "最多支持查询10个城市"}
    
    results = {}
    for city in cities:
        try:
            # 调用单个城市查询逻辑
            weather = get_weather(city)
            results[city] = weather
        except Exception as e:
            results[city] = f"查询失败: {str(e)}"
    
    return results
```

**示例 3：带复杂参数的工具**

```python
from typing import Optional
from datetime import datetime

@mcp.tool()
def get_weather_at_time(
    city: str,
    date: Optional[str] = None,
    time: Optional[str] = None
) -> str:
    """
    获取指定城市在特定时间的天气信息。
    
    这个工具展示了如何处理可选参数和日期时间。
    
    Args:
        city: 城市名称
        date: 日期（格式：YYYY-MM-DD），默认为今天
        time: 时间（格式：HH:MM），默认为当前时间
        
    Returns:
        指定时间的天气信息
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    if time is None:
        time = datetime.now().strftime("%H:%M")
    
    # 实现逻辑：查询历史或未来天气
    return f"{city}在{date} {time}的天气信息..."
```

### 添加资源详解

资源用于向 LLM 提供上下文信息。让我们看看如何添加不同类型的资源。

**示例 1：静态资源（城市列表）**

```python
@mcp.resource("weather://supported-cities")
def get_supported_cities() -> str:
    """
    提供支持查询天气的城市列表。
    
    这是一个静态资源，提供固定的数据列表。
    LLM 可以通过这个资源了解哪些城市可以查询。
    
    Returns:
        JSON 格式的城市列表，包含热门城市和国际城市
    """
    cities_data = {
        "热门城市": {
            "中国": ["北京", "上海", "广州", "深圳", "杭州", "成都"],
            "总数": 6
        },
        "国际城市": {
            "美洲": ["New York", "Los Angeles", "Toronto"],
            "欧洲": ["London", "Paris", "Berlin"],
            "亚洲": ["Tokyo", "Seoul", "Singapore"],
            "总数": 9
        },
        "总计": 15,
        "最后更新": "2024-01-01"
    }
    return json.dumps(cities_data, ensure_ascii=False, indent=2)
```

**示例 2：动态资源（实时配置）**

```python
@mcp.resource("weather://api-status")
def get_api_status() -> str:
    """
    提供 API 服务状态信息。
    
    这是一个动态资源，每次访问时都会获取最新的状态。
    
    Returns:
        API 状态信息，包括可用性、响应时间等
    """
    import time
    status = {
        "service": "Weather API",
        "status": "operational",
        "response_time_ms": 150,
        "last_check": time.strftime("%Y-%m-%d %H:%M:%S"),
        "supported_formats": ["json", "xml"],
        "rate_limit": "100 requests/hour"
    }
    return json.dumps(status, ensure_ascii=False, indent=2)
```

**示例 3：参数化资源**

```python
@mcp.resource("file://{path}")
def read_file_resource(path: str) -> str:
    """
    读取文件内容作为资源。
    
    这是一个参数化资源，URI 中包含参数。
    例如：file://config.json
    
    Args:
        path: 文件路径（从 URI 中提取）
        
    Returns:
        文件内容
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return json.dumps({"error": f"文件 {path} 不存在"})
    except Exception as e:
        return json.dumps({"error": f"读取文件失败: {str(e)}"})
```

### 添加提示模板详解

提示模板帮助用户快速进入特定的工作模式。让我们看看如何创建有效的提示模板。

**示例 1：角色扮演提示**

```python
@mcp.prompt()
def weather_analyst_prompt(city: str) -> str:
    """
    生成天气分析师角色的提示模板。
    
    这个提示引导 LLM 扮演专业的天气分析师，
    使用专业的术语和分析方法。
    
    Args:
        city: 要分析的城市
        
    Returns:
        格式化的提示文本
    """
    return f"""你是一名资深的天气分析师，拥有10年的气象数据分析经验。

请对{city}的天气情况进行专业分析，包括：

1. **当前天气状况分析**
   - 温度分析（与历史同期对比）
   - 湿度分析
   - 风速和风向分析
   - 能见度评估

2. **气象趋势预测**
   - 短期趋势（未来24小时）
   - 中期趋势（未来3-5天）
   - 异常天气预警

3. **专业建议**
   - 出行建议
   - 健康建议
   - 农业建议（如适用）

请使用专业的气象术语，并提供数据支撑的分析。"""
```

**示例 2：任务流程提示**

```python
@mcp.prompt()
def comprehensive_weather_report_prompt(city: str) -> str:
    """
    生成综合天气报告的任务流程提示。
    
    这个提示定义了一个多步骤的任务流程，
    引导 LLM 按照特定步骤完成任务。
    
    Args:
        city: 城市名称
        
    Returns:
        任务流程提示
    """
    return f"""请为{city}生成一份综合天气报告。请按照以下步骤执行：

**步骤 1：数据收集**
- 使用 get_weather 工具获取当前天气
- 使用 get_weather_detailed 工具获取详细信息
- 读取 weather://supported-cities 资源了解可用数据

**步骤 2：数据分析**
- 分析温度趋势
- 分析天气模式
- 识别异常情况

**步骤 3：报告生成**
请按照以下格式组织报告：

# {city}综合天气报告

## 1. 当前天气概况
[在此处插入当前天气数据]

## 2. 详细气象数据
[在此处插入详细数据]

## 3. 趋势分析
[在此处插入趋势分析]

## 4. 建议和预警
[在此处插入建议]

请确保报告专业、准确、易读。"""
```

**示例 3：多参数提示**

```python
@mcp.prompt()
def comparison_weather_prompt(city1: str, city2: str, comparison_type: str = "temperature") -> str:
    """
    生成城市天气对比提示。
    
    这个提示展示了如何处理多个参数。
    
    Args:
        city1: 第一个城市
        city2: 第二个城市
        comparison_type: 对比类型（temperature, humidity, wind等）
        
    Returns:
        对比分析提示
    """
    comparison_focus = {
        "temperature": "温度对比，包括最高温、最低温、平均温度",
        "humidity": "湿度对比，分析干燥程度和舒适度",
        "wind": "风速和风向对比，分析风力等级",
        "overall": "综合对比，包括所有气象要素"
    }
    
    return f"""你是一名气象对比分析专家。请对比分析{city1}和{city2}的天气情况。

**对比重点：** {comparison_focus.get(comparison_type, "综合对比")}

**分析步骤：**

1. 分别获取两个城市的天气数据
2. 提取关键指标进行对比
3. 分析差异和原因
4. 提供对比结论

**输出格式：**

# {city1} vs {city2} 天气对比

## 对比指标
[列出对比的关键指标]

## 详细对比
[详细对比数据]

## 差异分析
[分析差异原因]

## 结论
[总结对比结果]"""
```

## 最佳实践

1. **清晰的工具描述**：提供详细的 docstring，帮助 LLM 理解工具用途
2. **类型提示**：使用类型提示提高代码可读性和参数验证
3. **错误处理**：妥善处理异常，返回有意义的错误信息
4. **参数验证**：验证输入参数，防止无效请求
5. **日志记录**：记录工具调用和错误，便于调试

## 常见问题

### Q: 如何调试 MCP 服务器？

A: 使用 `mcp.run(transport="stdio")` 在本地运行，查看标准输出日志。

### Q: 支持哪些传输方式？

A: FastMCP 支持 Stdio、HTTP、SSE 等多种传输方式，默认使用 Stdio。

### Q: 如何添加认证？

A: 可以在 HTTP 模式下使用中间件添加认证，或通过环境变量管理 API 密钥。

### Q: 工具调用失败怎么办？

A: 确保返回有意义的错误信息，FastMCP 会自动将异常转换为 MCP 错误响应。

## 参考资源

- [FastMCP 官方文档](https://fastmcp.wiki/)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [HelloAgents MCP 使用指南](../Communication_protocol/protocol/MCP/intro.md)

## 下一步

- 探索更多 MCP 功能（Resources、Prompts）
- 集成到智能体系统中
- 部署到生产环境
- 构建更复杂的工具集

