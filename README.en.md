---

# English Version

# Hello Agents

A systematic AI Agent learning framework covering multiple Agent architectures from basics to advanced implementations.

[🏠 Home](./README.md) | 🇨🇳 [中文](./README.zh-CN.md)
---

## 🎯 Project Overview

This project comprises 5 progressive chapters that help developers understand and implement modern AI Agent systems. Starting from basic LLM calls, gradually mastering core paradigms like ReAct, Plan-and-Solve, and Reflection.

## 📚 Chapter Contents

### Chapter 1: Basic Agent Framework
**Core Topics**: LLM API calls and tool integration
- LLM class wrapper and OpenAI API integration
- Prompt Engineering templates
- Tool registration and dynamic calling
- Complete travel assistant Agent example

**Code Path**: `Chapter1/codes/`

---

### Chapter 2: Local Model Inference
**Core Topics**: Local LLM deployment and inference
- Hugging Face Transformers framework
- Model loading and initialization
- CUDA GPU acceleration
- Chat mode inference pipeline

**Example Model**: Qwen1.5-0.5B-Chat

**Code Path**: `Chapter2/`

---

### Chapter 3: Classic Agent Paradigms

#### 🔄 3.1 ReAct Paradigm
**Reasoning + Acting** - Agent that thinks and acts simultaneously

**Key Features**:
- Thought → Action → Observation cycle
- Dynamic planning and real-time error correction
- High interpretability
- Suitable for multi-step reasoning and tool interaction

**Code Path**: `Chapter3/ReAct/`

**Use Cases**:
- Tasks requiring external knowledge (weather, news, stock prices)
- Tasks requiring precise calculations (using calculator tools to avoid hallucinations)
- Tasks requiring API interactions

---

#### 📋 3.2 Plan-and-Solve Paradigm
**Plan First, Execute Second** - Agent with careful planning

**Key Features**:
- Planning Phase: Decompose tasks and create clear plans
- Solving Phase: Execute step by step
- Better goal consistency
- Avoids execution drift

**Code Path**: `Chapter3/Plan_and_Solve/`

**Use Cases**:
- Multi-step math problems
- Report writing requiring multiple information sources
- Complex code generation tasks
- Well-structured complex tasks

---

#### 🔄 3.3 Reflection Paradigm
**Execute → Reflect → Optimize** - Self-evolving Agent

**Core Process**:
1. **Execution**: Complete initial task
2. **Reflection**: Evaluate and provide feedback
3. **Refinement**: Improve based on feedback

**Key Components**:
- **Actor**: Decision-making and execution
- **Evaluator**: Quality assessment
- **Trajectory**: Short-term memory (current task steps)
- **Experience**: Long-term memory (experience repository)

**Code Path**: `Chapter3/Reflection/`

---

### Chapter 4: Mainstream Agent Frameworks
**Core Topics**: Transitioning from manual implementation to framework-based development
- Advantages of frameworks: Code reuse, decoupling, state management, observability
- Introduction to mainstream frameworks: AutoGen, AgentScope, CAMEL, LangGraph
- **AutoGen Practice**: Multi-agent collaboration and automated task decomposition
- **LangGraph Practice**: Building graph-based cyclic workflows

**Code Path**: `Chapter4/`

---

## 🛠️ Installation and Configuration

### 1. Create Conda Environment

```bash
conda create -n hello_agents python=3.10
conda activate hello_agents
```

### 2. Install Dependencies

```bash
# For Chapter 1 & 3
pip install openai python-dotenv

# For Chapter 2
pip install torch torchvision torchaudio transformers

# Optional: For GPU support
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 3. Configure API Keys

```bash
cp .env.example .env
# Edit .env with your API keys
```

---

## 📁 Project Structure

```
Hello_agents/
├── Chapter1/                    # Basic Agent
│   └── codes/
├── Chapter2/                    # Local Model
├── Chapter3/                    # Agent Paradigms
│   ├── ReAct/
│   ├── Plan_and_Solve/
│   └── Reflection/
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

```bash
# Chapter 1
cd Chapter1/codes && python main.py

# Chapter 2
cd Chapter2 && python llm_call.py

# Chapter 3 - ReAct
cd Chapter3/ReAct && python ReAct.py

# Chapter 3 - Plan-and-Solve
cd Chapter3/Plan_and_Solve/code && python plan_and_solve.py

# Chapter 3 - Reflection
cd Chapter3/Reflection/code && python test_output.py
```

---

## 🎓 Learning Path

| Chapter | Difficulty | Topics | Time |
|---------|-----------|--------|------|
| Chapter 1 | ⭐⭐ | LLM basics, tool integration | 2-3h |
| Chapter 2 | ⭐⭐ | Local inference, GPU acceleration | 1-2h |
| Chapter 3.1 | ⭐⭐⭐ | ReAct, dynamic planning | 2-3h |
| Chapter 3.2 | ⭐⭐⭐ | Plan-and-Solve, global planning | 2-3h |
| Chapter 3.3 | ⭐⭐⭐⭐ | Reflection, self-optimization | 3-4h |

---

## ❓ FAQ

**Q: Import errors (ModuleNotFoundError)?**
```python
# ✅ Use relative imports
from .search_tool import search
```

**Q: API key errors?**
- Verify `.env` file exists and is in the correct location
- Check if your API key is valid
- Confirm you have sufficient API credits

**Q: Local model inference is slow?**
- Use smaller models (e.g., 0.5B)
- Enable GPU acceleration
- Reduce `max_new_tokens` parameter

---

## 📖 Learning Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

---

## 📄 License

MIT License
