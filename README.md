# Hello Agents

一个 AI Agent 学习项目，分为三个章节，逐步学习如何构建智能 Agent。

## 项目说明

这个项目包含三个独立的学习章节：

**Chapter 1**: 基础 Agent - 学习如何用 LLM 调用工具
- 实现一个旅行助手 Agent
- 使用天气查询和景点推荐工具
- 理解 Thought-Action-Observation 循环

**Chapter 2**: 本地模型 - 使用本地模型进行推理
- 使用 Qwen 模型本地推理
- 无需调用 API，支持 GPU 加速

**Chapter 3**: ReAct 框架 - 更强大的推理能力
- 改进的工具执行器
- 更好的推理链支持

## 目录结构

```
Hello_agents/
├── Chapter1/               # 基础 Agent
│   ├── codes/
│   │   ├── main.py         # 旅行助手示例
│   │   ├── llm.py          # LLM 类
│   │   └── tools/          # 工具集
│   └── image/
├── Chapter2/               # 本地模型
│   └── llm_call.py
└── Chapter3/               # ReAct 框架
    ├── ReAct
```

## 安装和使用

### 依赖
```bash
pip install openai python-dotenv  # Chapter 1 & 3
pip install torch transformers    # Chapter 2
```

### 配置（Chapter 1 & 3）
在 `Chapter1/codes/` 下创建 `.env` 文件：
```
OPENAI_API_KEY=your_key_here
```

### 运行
```bash
# Chapter 1
cd Chapter1/codes
python main.py

# Chapter 2
cd Chapter2
python llm_call.py

# Chapter 3
cd Chapter3
python ReAct.py
```

## 工作流程

Agent 的基本流程：
1. 用户提问
2. LLM 思考并决定使用哪个工具
3. 执行工具，获得结果
4. 反馈给 LLM，继续推理
5. 重复直到得出最终答案

```
用户输入 → LLM 思考 → 选择工具 → 执行 → 观察结果 → 迭代 → 最终答案
```

## 🔧 工具调用示例

### 基础工具模式
```python
# 定义工具函数
def search(query: str) -> str:
    """执行网络搜索"""
    return search_results

# 注册工具
toolExecutor.register_tool("Search", "网络搜索工具", search)

# Agent 调用
# Thought: 用户想了解某个信息
# Action: Search(query="搜索词")
# Observation: [搜索结果]
```

## 📊 学习路线

| 章节 | 难度 | 主要学习 | 所需时间 |
|------|------|--------|--------|
| Chapter 1 | ⭐⭐ | Agent 基础、Tool 集成、Prompt 工程 | 2-3 小时 |
| Chapter 2 | ⭐⭐ | 本地模型、Transformers、推理优化 | 1-2 小时 |
| Chapter 3 | ⭐⭐⭐ | ReAct 框架、推理链、复杂决策 | 2-3 小时 |

## 🎯 学习目标

- ✅ 理解 LLM 和 Agent 的基本概念
- ✅ 掌握 Prompt Engineering 最佳实践
- ✅ 学会设计和集成自定义工具
- ✅ 实现 ReAct 等高级 Agent 框架
- ✅ 了解本地模型部署和优化
- ✅ 能够独立构建生产级 Agent 系统

## 常见问题

**Q: 导入错误？**
A: 确保使用相对导入。例如在 `tool/` 目录下应该使用：
```python
from .search_tool import search
```

**Q: API 密钥错误？**
A: 检查 `.env` 文件是否正确配置和放在正确位置

**Q: 本地模型很慢？**
A: 使用更小的模型，或启用 GPU 加速

## 🤝 贡献指南

欢迎提交 PR 或 Issue 来改进项目：
- 新增章节内容
- 优化代码实现
- 补充学习资源
- 修复 bug

## 📚 参考资源

- [OpenAI API 文档](https://platform.openai.com/docs)
- [Prompt Engineering 最佳实践](https://platform.openai.com/docs/guides/prompt-engineering)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [ReAct 论文](https://arxiv.org/abs/2210.03629)

## 📄 许可证

MIT License - 可自由使用、修改和分发

## 📞 联系方式

有问题或建议？欢迎通过 Issue 或讨论与我们联系！

---

**最后更新**: 2025-11-28  
**当前版本**: 1.0.0  
**维护者**: seuwestbrrook
# Hello Agents

一个 AI Agent 学习项目，分为三个章节，逐步学习如何构建智能 Agent。

## 项目说明

这个项目包含三个独立的学习章节：

**Chapter 1**: 基础 Agent - 学习如何用 LLM 调用工具
- 实现一个旅行助手 Agent
- 使用天气查询和景点推荐工具
- 理解 Thought-Action-Observation 循环

**Chapter 2**: 本地模型 - 使用本地模型进行推理
- 使用 Qwen 模型本地推理
- 无需调用 API，支持 GPU 加速

**Chapter 3**: ReAct 框架 - 更强大的推理能力
- 改进的工具执行器
- 更好的推理链支持

## 目录结构

```
Hello_agents/
├── Chapter1/               # 基础 Agent
│   ├── codes/
│   │   ├── main.py         # 旅行助手示例
│   │   ├── llm.py          # LLM 类
│   │   └── tools/          # 工具集
│   └── image/
├── Chapter2/               # 本地模型
│   └── llm_call.py
└── Chapter3/               # ReAct 框架
    ├── ReAct
```

## 安装和使用

### 依赖
```bash
pip install openai python-dotenv  # Chapter 1 & 3
pip install torch transformers    # Chapter 2
```

### 配置（Chapter 1 & 3）
在 `Chapter1/codes/` 下创建 `.env` 文件：
```
OPENAI_API_KEY=your_key_here
```

### 运行
```bash
# Chapter 1
cd Chapter1/codes
python main.py

# Chapter 2
cd Chapter2
python llm_call.py

# Chapter 3
cd Chapter3
python ReAct.py
```

## 工作流程

Agent 的基本流程：
1. 用户提问
2. LLM 思考并决定使用哪个工具
3. 执行工具，获得结果
4. 反馈给 LLM，继续推理
5. 重复直到得出最终答案

```
用户输入 → LLM 思考 → 选择工具 → 执行 → 观察结果 → 迭代 → 最终答案
```

## 常见问题

**Q: 导入错误？**
A: 确保使用相对导入。例如在 `tool/` 目录下应该使用：
```python
from .search_tool import search
```

**Q: API 密钥错误？**
A: 检查 `.env` 文件是否正确配置和放在正确位置

**Q: 本地模型很慢？**
A: 使用更小的模型，或启用 GPU 加速

## 许可证

MIT License
