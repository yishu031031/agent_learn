[🏠 Home](./README.md) | 🇬🇧 [English](./README.en.md)
---

<!-- 中文 README: 复制自原 README.md 中的中文部分 -->

# Hello Agents（中文）

一个系统的 AI Agent 学习框架，涵盖从基础到高阶的多种 Agent 架构和实现方法。

## 🎯 项目概述

这个项目通过 5 个递进式章节，帮助开发者深入理解和实现现代 AI Agent 系统。从基础的 LLM 调用开始，逐步掌握 ReAct、Plan-and-Solve、Reflection 等核心范式。

## 📚 章节内容

### Chapter 1: 基础 Agent 框架
**核心内容**：LLM 基础调用与工具集成
- LLM 类封装与 OpenAI API 集成
- Prompt Engineering 指令模板
- 工具注册与动态调用机制
- 旅行助手 Agent 完整示例

**代码路径**：`Chapter1/codes/`

---

### Chapter 2: 本地模型推理
**核心内容**：本地大模型部署与推理
- Hugging Face Transformers 框架
- 模型加载与初始化
- CUDA GPU 加速支持
- Chat 模式推理流程

**模型示例**：Qwen1.5-0.5B-Chat

**代码路径**：`Chapter2/`

---

### Chapter 3: 智能体经典范式

#### 🔄 3.1 ReAct 范式
**Reasoning + Acting** - 边想边做的智能体

**核心特点**：
- Thought（思考）→ Action（行动）→ Observation（观察）的循环
- 动态规划与实时纠错
- 高可解释性
- 适合多步推理和工具交互

**关键代码**：`Chapter3/ReAct/`
- `ReAct.py` - ReAct Agent 实现
- `tool/tool_excute.py` - 工具执行器
- `tool/search_tool.py` - 搜索工具

**适用场景**：
- 需要外部知识的任务（天气、新闻、股价查询）
- 需要精确计算的任务（使用计算器工具避免幻觉）
- 需要与 API 交互的任务

---

#### 📋 3.2 Plan-and-Solve 范式
**先规划再执行** - 三思而后行的智能体

**核心特点**：
- Planning Phase（规划阶段）：分解任务，制定清晰计划
- Solving Phase（执行阶段）：按计划逐步执行
- 更好的目标一致性
- 避免执行偏离

**代码路径**：`Chapter3/Plan_and_Solve/`

**适用场景**：
- 多步数学应用题
- 需要多信息源整合的报告撰写
- 复杂代码生成任务
- 结构清晰的复杂任务

---

#### 🔄 3.3 Reflection 范式
**执行 → 反思 → 优化** - 自我进化的智能体

**核心流程**：
1. **Execution**（执行）：完成初步任务
2. **Reflection**（反思）：评估和反馈
3. **Refinement**（优化）：根据反馈改进

**核心组件**：
- **Actor**（执行者）：决策与行动
- **Evaluator**（评价器）：质量评估
- **Trajectory**（短期记忆）：当前任务轨迹
- **Experience**（长期记忆）：经验库

**关键区别**：
| 维度 | Trajectory | Experience |
|------|-----------|-----------|
| 存储内容 | 本轮所有 Action 和 Observation | 高度浓缩的学习建议 |
| 作用范围 | 仅本轮任务有效 | 跨任务、长期有效 |
| 信息密度 | 详细、冗余 | 精炼、核心 |

**代码路径**：`Chapter3/Reflection/`

---

## 🛠️ 安装与配置

### 1. 创建 Conda 环境

```bash
# 创建 Python 3.10 环境
conda create -n hello_agents python=3.10

# 激活环境
conda activate hello_agents
```

### 2. 安装依赖

```bash
# Chapter 1 & 3 依赖（OpenAI 兼容 API）
pip install openai python-dotenv

# Chapter 2 依赖（本地推理）
pip install torch torchvision torchaudio transformers

# 使用 Conda 安装 PyTorch（推荐 GPU 用户）
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 3. 配置 API 密钥

```bash
# 第一次使用时
cp .env.example .env

# 编辑 .env 填入你的 API 密钥
OPENAI_API_KEY=your_key_here
OPENAI_API_BASE_URL=https://api.openai.com/v1
```

**重要**：`.env` 已被加入 `.gitignore`，你的密钥不会被提交到仓库

---

## 📁 项目结构

```
Hello_agents/
├── Chapter1/                    # 基础 Agent
│   ├── codes/
│   │   ├── main.py             # 旅行助手示例
│   │   ├── llm.py              # LLM 类
│   │   ├── instruction_template.md
│   │   └── tools/
│   │       ├── get_weather.py
│   │       └── search_attraction.py
│   └── image/
│
├── Chapter2/                    # 本地模型
│   └── llm_call.py
│
├── Chapter3/                    # 智能体范式
│   ├── intro.md                 # 范式介绍
│   ├── ReAct/                   # ReAct 实现
│   │   ├── ReAct.py
│   │   ├── llm_call.py
│   │   └── tool/
│   ├── Plan_and_Solve/          # Plan-and-Solve 实现
│   │   └── code/
│   └── Reflection/              # Reflection 实现
│       ├── code/
│       ├── image/
│       └── image_explanation.md
│
├── .env.example                 # 环境变量模板
├── .gitignore
└── README.md
```

---

## 🚀 快速开始

### 运行 Chapter 1
```bash
cd Chapter1/codes
python main.py
```

### 运行 Chapter 2
```bash
cd Chapter2
python llm_call.py
```

### 运行 Chapter 3 - ReAct
```bash
cd Chapter3/ReAct
python ReAct.py
```

### 运行 Chapter 3 - Plan-and-Solve
```bash
cd Chapter3/Plan_and_Solve/code
python plan_and_solve.py
```

### 运行 Chapter 3 - Reflection
```bash
cd Chapter3/Reflection/code
python test_output.py
```

---

## 🎓 学习路线

| 章节 | 难度 | 核心内容 | 时间 |
|------|------|--------|------|
| Chapter 1 | ⭐⭐ | LLM 基础、工具集成 | 2-3h |
| Chapter 2 | ⭐⭐ | 本地推理、GPU 加速 | 1-2h |
| Chapter 3.1 | ⭐⭐⭐ | ReAct 框架、动态规划 | 2-3h |
| Chapter 3.2 | ⭐⭐⭐ | Plan-and-Solve、全局规划 | 2-3h |
| Chapter 3.3 | ⭐⭐⭐⭐ | Reflection、自我优化 | 3-4h |

---

## ❓ 常见问题

**Q: 导入错误（ModuleNotFoundError）？**
```python
# ✅ 正确方式：使用相对导入
from .search_tool import search
```

**Q: API 密钥错误？**
- 检查 `.env` 文件是否存在且路径正确
- 验证 API 密钥是否有效
- 确认 API 余额是否充足

**Q: 本地模型推理很慢？**
- 使用更小的模型（如 0.5B）
- 启用 GPU 加速
- 减少 `max_new_tokens` 参数

**Q: 流式响应处理出错？**
- 确保所有 chunk 的 `choices` 非空
- 使用 `try-except` 处理异常
- 检查 API 提供商的响应格式

---

## 📖 学习资源

- [OpenAI API 文档](https://platform.openai.com/docs)
- [ReAct 论文](https://arxiv.org/abs/2210.03629)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

---

## 📄 许可证

MIT License

---

（此处将保留 README.md 中的“中文版本”全部内容，供中文读者阅读）
