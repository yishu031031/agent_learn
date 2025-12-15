# 构建个人智能体框架

在前面的章节中，我们讲解了智能体的基础知识，并体验了主流框架带来的开发便利。从本章开始，我们将进入一个更具挑战也更有价值的阶段：从零开始，逐步构建一个智能体框架——(Name)Agent。

为确保学习过程的连贯性与可复现性，你所命名的 Agent 将以版本迭代的方式推进开发。

## 框架整体架构设计

### 为何需要自建 Agent 框架

在智能体技术快速发展的今天，市面上已经存在众多成熟的 Agent 框架。那么，为什么我们还要从零开始构建一个新的框架呢？

#### 1. 市面框架的快速迭代与局限性

智能体领域是一个快速发展的领域，随时会有新的概念产生，对于智能体的设计每个框架都有自己的定位和理解，不过智能体的核心知识点是一致的。

- **过度抽象的复杂性**：许多框架为了追求通用性，引入了大量抽象层和配置选项。以 LangChain 为例，其链式调用机制虽然灵活，但对初学者而言学习曲线陡峭，往往需要理解大量概念才能完成简单任务。

- **快速迭代带来的不稳定性**：商业化框架为了抢占市场，API 接口变更频繁。开发者经常面临版本升级后代码无法运行的困扰，维护成本居高不下。

- **黑盒化的实现逻辑**：许多框架将核心逻辑封装得过于严密，开发者难以理解 Agent 的内部工作机制，缺乏深度定制能力。遇到问题时只能依赖文档和社区支持，尤其是如果社区不够活跃，可能一个反馈意见会非常久也没有人推进，影响后续的开发效率。

- **依赖关系的复杂性**：成熟框架往往携带大量依赖包，安装包体积庞大，在需要与别的项目代码配合的情况下可能出现依赖冲突问题。

#### 2. 从使用者到构建者的能力跃迁

构建自己的 Agent 框架，实际上是一个从"使用者"向"构建者"转变的过程。这种转变带来的价值是长远的。

- **深度理解 Agent 工作原理**：通过亲手实现每个组件，开发者能够真正理解 Agent 的思考过程、工具调用机制、以及各种设计模式的好坏与区别。

- **获得完全的控制权**：自建框架意味着对每一行代码都有完全的掌控，可以根据具体需求进行精确调优，而不受第三方框架设计理念的束缚。

- **培养系统设计能力**：框架构建过程涉及模块化设计、接口抽象、错误处理等软件工程核心技能，这些能力对开发者的长期成长具有重要价值。

#### 3. 定制化需求与深度掌握的必要性

在实际应用中，不同场景对智能体的需求差异巨大，往往都需要在通用框架基础上做二次开发。

- **特定领域的优化需求**：金融、医疗、教育等垂直领域往往需要针对性的提示词模板、特殊的工具集成、以及定制化的安全策略。

- **性能与资源的精确控制**：生产环境中，对响应时间、内存占用、并发处理能力都有严格要求，通用框架的"一刀切"方案往往无法满足精细化需求。

- **学习与教学的透明性要求**：在我们的教学场景中，学习者更期待的是清晰地看到智能体的每一步构建过程，理解不同范式的工作机制，这要求框架具有高度的可观测性和可解释性。

### 核心学习内容

```
hello-agents/
├── hello_agents/
│   │
│   ├── core/                     # 核心框架层
│   │   ├── agent.py              # Agent基类
│   │   ├── llm.py                # HelloAgentsLLM统一接口
│   │   ├── message.py            # 消息系统
│   │   ├── config.py             # 配置管理
│   │   └── exceptions.py         # 异常体系
│   │
│   ├── agents/                   # Agent实现层
│   │   ├── simple_agent.py       # SimpleAgent实现
│   │   ├── react_agent.py        # ReActAgent实现
│   │   ├── reflection_agent.py   # ReflectionAgent实现
│   │   └── plan_solve_agent.py   # PlanAndSolveAgent实现
│   │
│   ├── tools/                    # 工具系统层
│   │   ├── base.py               # 工具基类
│   │   ├── registry.py           # 工具注册机制
│   │   ├── chain.py              # 工具链管理系统
│   │   ├── async_executor.py     # 异步工具执行器
│   │   └── builtin/              # 内置工具集
│   │       ├── calculator.py     # 计算工具
│   │       └── search.py         # 搜索工具
└──
```

# 从HelloAgentLLM出发

## 支持多提供商

我们之前定义的 HelloAgentsLLM 类，已经能够通过 api_key 和 base_url 这两个核心参数，连接任何兼容 OpenAI 接口的服务。这在理论上保证了通用性，但在实际应用中，不同的服务商在环境变量命名、默认 API 地址和推荐模型等方面都存在差异。如果每次切换服务商都需要用户手动查询并修改代码，会极大影响开发效率。为了解决这一问题，我们引入 provider.其改进思路是：让 HelloAgentsLLM 在内部处理不同服务商的配置细节，从而为用户提供一个统一、简洁的调用体验。


### 自主检测机制

`_auto_detect_provider` 方法负责根据环境信息，按照下述优先级顺序，尝试自动推断服务商：

#### 1. 最高优先级：检查特定服务商的环境变量

这是最直接、最可靠的判断依据。框架会依次检查以下环境变量是否存在：
- `MODELSCOPE_API_KEY`
- `OPENAI_API_KEY`
- `ZHIPU_API_KEY`
- `DEEPSEEK_API_KEY`
- `DASHSCOPE_API_KEY`
- 等其他特定服务商的环境变量

一旦发现任何一个，就会立即确定对应的服务商。

#### 2. 次高优先级：根据 base_url 进行判断

如果用户没有设置特定服务商的密钥，但设置了通用的 `LLM_BASE_URL`，框架会转而解析这个 URL：

- **域名匹配**：通过检查 URL 中是否包含以下特征字符串来识别云服务商：
  - `api-inference.modelscope.cn` → ModelScope
  - `api.openai.com` → OpenAI
  - `api.deepseek.com` → DeepSeek
  - `dashscope.aliyuncs.com` → 通义千问
  - `api.moonshot.cn` → Kimi
  - `open.bigmodel.cn` → 智谱AI

- **端口匹配**：通过检查 URL 中是否包含以下标准端口来识别本地部署方案：
  - `:11434` → Ollama
  - `:8000` → VLLM
  - `:8080` 或 `:7860` → 其他本地服务

#### 3. 辅助判断：分析 API 密钥的格式

在某些情况下，如果上述两种方式都无法确定，框架会尝试分析通用环境变量 `LLM_API_KEY` 的格式：

- 某些服务商的 API 密钥有固定的前缀或独特的编码格式
- 例如：以 `ms-` 开头的密钥通常属于 ModelScope
- 由于这种方式可能存在模糊性（例如多个服务商的密钥格式相似），因此它的优先级较低，仅作为辅助手段

其部分关键代码如下：
```python
    def _auto_detect_provider(self, api_key: Optional[str], base_url: Optional[str]) -> str:
        """
        自动检测LLM提供商

        检测逻辑：
        1. 优先检查特定提供商的环境变量
        2. 根据API密钥格式判断
        3. 根据base_url判断
        4. 默认返回通用配置
        """
        # 1. 检查特定提供商的环境变量 (最高优先级)
        if os.getenv("MODELSCOPE_API_KEY"): return "modelscope"
        if os.getenv("OPENAI_API_KEY"): return "openai"
        if os.getenv("ZHIPU_API_KEY"): return "zhipu"
        # ... 其他服务商的环境变量检查

        # 获取通用的环境变量
        actual_api_key = api_key or os.getenv("LLM_API_KEY")
        actual_base_url = base_url or os.getenv("LLM_BASE_URL")

        # 2. 根据 base_url 判断
        if actual_base_url:
            base_url_lower = actual_base_url.lower()
            if "api-inference.modelscope.cn" in base_url_lower: return "modelscope"
            if "open.bigmodel.cn" in base_url_lower: return "zhipu"
            if "localhost" in base_url_lower or "127.0.0.1" in base_url_lower:
                if ":11434" in base_url_lower: return "ollama"
                if ":8000" in base_url_lower: return "vllm"
                return "local" # 其他本地端口

        # 3. 根据 API 密钥格式辅助判断
        if actual_api_key:
            if actual_api_key.startswith("ms-"): return "modelscope"
            # ... 其他密钥格式判断

        # 4. 默认返回 'auto'，使用通用配置
        return "auto"
```

### 凭证解析机制

一旦 `provider` 被确定（无论是用户指定还是自动检测），`_resolve_credentials` 方法便会接手处理服务商的差异化配置。

该方法的核心逻辑是：

1. **根据 provider 查找对应的环境变量**：每个服务商都有其特定的环境变量名称（如 `OPENAI_API_KEY`、`MODELSCOPE_API_KEY` 等）
2. **设置默认的 base_url**：如果用户未提供 `base_url`，框架会根据 `provider` 自动设置对应的默认地址
3. **优先级处理**：优先使用用户传入的参数，其次使用特定服务商的环境变量，最后使用通用环境变量或默认值

其部分关键实现如下：

```python
def _resolve_credentials(self, api_key: Optional[str], base_url: Optional[str]) -> tuple[str, str]:
    """根据provider解析API密钥和base_url"""
    if self.provider == "openai":
        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
        resolved_base_url = base_url or os.getenv("LLM_BASE_URL") or "https://api.openai.com/v1"
        return resolved_api_key, resolved_base_url

    elif self.provider == "modelscope":
        resolved_api_key = api_key or os.getenv("MODELSCOPE_API_KEY") or os.getenv("LLM_API_KEY")
        resolved_base_url = base_url or os.getenv("LLM_BASE_URL") or "https://api-inference.modelscope.cn/v1/"
        return resolved_api_key, resolved_base_url
    
    # ... 其他服务商的逻辑
```

# 框架接口实现

在上节中，我们构建了 `HelloAgentsLLM` 这一核心组件，解决了与大语言模型通信的关键问题。不过它还需要一系列配套的接口和组件来处理数据流、管理配置、应对异常，并为上层应用的构建提供一个清晰、统一的结构。

本节将讲述以下三个核心文件：

- **`message.py`**：定义了框架内统一的消息格式，确保了智能体与模型之间信息传递的标准化。

- **`config.py`**：提供了一个中心化的配置管理方案，使框架的行为易于调整和扩展。

- **`agent.py`**：定义了所有智能体的抽象基类（`Agent`），为后续实现不同类型的智能体提供了统一的接口和规范。

## Message类

在智能体与大语言模型的交互中，对话历史是至关重要的上下文。
为了规范地管理这些信息，我们设计了一个简易 Message 类。在后续上下文工程章节中，会对其进行扩展。

## Config类

Config 类的职责是将代码中硬编码配置参数集中起来，并支持从环境变量中读取。

## Agent抽象基类

Agent 类是整个框架的顶层抽象。它定义了一个智能体应该具备的通用行为和属性，但并不关心具体的实现方式。
我们通过 Python 的 abc (Abstract Base Classes) 模块来实现它，这强制所有具体的智能体实现（如后续章节的 SimpleAgent, ReActAgent 等）都必须遵循同一个“接口”。

该类的设计体现了面向对象中的抽象原则。首先，它通过继承 ABC 被定义为一个不能直接实例化的抽象类。其构造函数 __init__ 清晰地定义了 Agent 的核心依赖：名称、LLM 实例、系统提示词和配置。最重要的部分是使用 @abstractmethod 装饰的 run 方法，它强制所有子类必须实现此方法，从而保证了所有智能体都有统一的执行入口。此外，基类还提供了通用的历史记录管理方法，这些方法与 Message 类协同工作，体现了组件间的联系。


# Agent范式的框架华实现

## SimpleAgent框架实现

具体开发过程见文件 `` Chapter5/SimpleAgent `` 

# 工具系统

本节内容将在前面构建的 Agent 基础架构上，深入探讨工具系统的设计与实现。我们将从基础设施建设开始，逐步深入到自定义开发设计。

## 学习目标

本节的学习目标围绕以下三个核心方面展开：

- **统一的工具抽象与管理**：建立标准化的 `Tool` 基类和 `ToolRegistry` 注册机制，为工具的开发、注册、发现和执行提供统一的基础设施。

- **实战驱动的工具开发**：以数学计算工具为案例，展示如何设计和实现自定义工具，让读者掌握工具开发的完整流程。

- **高级整合与优化策略**：通过多源搜索工具的设计，展示如何整合多个外部服务，实现智能后端选择、结果合并和容错处理，体现工具系统在复杂场景下的设计思维。

## 工具基类与注册机制设计

在构建可扩展的工具系统时，我们需要首先建立一套标准化的基础设施。这套基础设施包括 `Tool` 基类、`ToolRegistry` 注册表，以及工具管理机制。

### 1. Tool 基类的抽象设计

`Tool` 基类是整个工具系统的核心抽象，它定义了所有工具必须遵循的接口规范：

```python
class Tool(ABC):
    """工具基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, parameters: Dict[str, Any]) -> str:
        """执行工具"""
        pass

    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        """获取工具参数定义"""
        pass
```

这个设计体现了面向对象设计的核心思想：

- **统一的执行接口**：通过统一的 `run` 方法接口，所有工具都能以一致的方式执行，接受字典参数并返回字符串结果，确保了框架的一致性。

- **自描述能力**：通过 `get_parameters` 方法能够清晰地告诉调用者自己需要什么参数，这种内省机制为自动化文档生成和参数验证提供了基础。

- **可发现性**：`name` 和 `description` 等元数据的设计，让工具系统具备了良好的可发现性和可理解性。

### 2. ToolParameter 参数定义系统

为了支持复杂的参数验证和文档生成，我们设计了 `ToolParameter` 类：

```python
class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
```

这种设计让工具能够精确描述自己的参数需求，支持：
- 类型检查
- 默认值设置
- 文档自动生成

### 3. ToolRegistry 注册表的实现

`ToolRegistry` 是工具系统的管理中枢，它提供了工具的注册、发现、执行等核心功能。在这一节我们主要用到以下功能：

```python
class ToolRegistry:
    """HelloAgents工具注册表"""

    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._functions: dict[str, dict[str, Any]] = {}

    def register_tool(self, tool: Tool):
        """注册Tool对象"""
        if tool.name in self._tools:
            print(f"⚠️ 警告:工具 '{tool.name}' 已存在，将被覆盖。")
        self._tools[tool.name] = tool
        print(f"✅ 工具 '{tool.name}' 已注册。")
        
    def register_function(self, name: str, description: str, func: Callable[[str], str]):
        """
        直接注册函数作为工具（简便方式）

        Args:
            name: 工具名称
            description: 工具描述
            func: 工具函数，接受字符串参数，返回字符串结果
        """
        if name in self._functions:
            print(f"⚠️ 警告:工具 '{name}' 已存在，将被覆盖。")

        self._functions[name] = {
            "description": description,
            "func": func
        }
        print(f"✅ 工具 '{name}' 已注册。")
```

`ToolRegistry` 支持两种注册方式：

- **Tool 对象注册**：适合复杂工具，支持完整的参数定义和验证
- **函数直接注册**：适合简单工具，快速集成现有函数

### 4. 工具发现与管理机制

注册表提供了丰富的工具管理功能：

#### 获取工具描述

```python
def get_tools_description(self) -> str:
    """获取所有可用工具的格式化描述字符串"""
    descriptions = []

    # Tool对象描述
    for tool in self._tools.values():
        descriptions.append(f"- {tool.name}: {tool.description}")

    # 函数工具描述
    for name, info in self._functions.items():
        descriptions.append(f"- {name}: {info['description']}")

    return "\n".join(descriptions) if descriptions else "暂无可用工具"
```

这个方法生成的描述字符串可以直接用于构建 Agent 的提示词，让 Agent 了解可用的工具。

#### 转换为 OpenAI Schema

```python
def to_openai_schema(self) -> Dict[str, Any]:
    """转换为 OpenAI function calling schema 格式

    用于 FunctionCallAgent，使工具能够被 OpenAI 原生 function calling 使用

    Returns:
        符合 OpenAI function calling 标准的 schema
    """
    parameters = self.get_parameters()

    # 构建 properties
    properties = {}
    required = []

    for param in parameters:
        # 基础属性定义
        prop = {
            "type": param.type,
            "description": param.description
        }

        # 如果有默认值，添加到描述中（OpenAI schema 不支持 default 字段）
        if param.default is not None:
            prop["description"] = f"{param.description} (默认: {param.default})"

        # 如果是数组类型，添加 items 定义
        if param.type == "array":
            prop["items"] = {"type": "string"}  # 默认字符串数组

        properties[param.name] = prop

        # 收集必需参数
        if param.required:
            required.append(param.name)

    return {
        "type": "function",
        "function": {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }
```

这个方法生成的 schema 可以直接用于原生的 OpenAI SDK 的工具调用。

OpenAI Functioncall Schema：

```python
tools = [
  {
    "type": "function", #工具类型
    "function": {
      "name": "get_current_weather", #函数名称
      "description": "Get the current weather in a given location", #函数描述
      "parameters": { #函数参数
        "type": "object", #参数类型
        "properties": { #参数属性
          "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}, #参数名称和描述
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}, #参数枚举值
        },
        "required": ["location"], #参数必填
      },
    }
  }
]
```