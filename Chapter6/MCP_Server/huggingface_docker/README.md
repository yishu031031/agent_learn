# HuggingFace Spaces Docker 部署示例

本示例展示了如何将基于 FastMCP 的天气查询 MCP 服务器打包为 Docker 镜像，并部署到 HuggingFace Spaces。

## 📋 目录结构

```
huggingface_docker/
├── Dockerfile          # Docker 镜像构建文件
├── requirements.txt    # Python 依赖列表
├── weather_server.py   # MCP 服务器代码（需要从上级目录复制）
└── README.md          # 本文件
```

## 🚀 快速开始

### 1. 准备文件

在 HuggingFace Space 中，您需要以下文件：

- `Dockerfile`
- `requirements.txt`
- `weather_server.py`（MCP 服务器代码）

### 2. 创建 HuggingFace Space

1. 登录 [HuggingFace](https://huggingface.co/)
2. 点击 "New Space"
3. 填写 Space 信息：
   - **Space name**: `weather-mcp-server`（或您喜欢的名称）
   - **SDK**: 选择 `Docker`
   - **Visibility**: 选择 `Public` 或 `Private`

### 3. 上传文件

将以下文件上传到 Space 的根目录：

- `Dockerfile`
- `requirements.txt`
- `weather_server.py`

### 4. 配置 Space

在 Space 的根目录创建或编辑 `README.md`，添加以下 YAML 配置：

```yaml
---
title: Weather MCP Server
emoji: 🌤️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
pinned: false
license: mit
---
```

### 5. 自动部署

HuggingFace 会自动检测到 Dockerfile 并开始构建。构建过程通常需要 5-10 分钟。

## 🔧 本地测试

在部署到 HuggingFace 之前，您可以在本地测试 Docker 镜像：

### 构建镜像

```bash
# 在 huggingface_docker 目录下
docker build -t weather-mcp-server .
```

### 运行容器

```bash
docker run -p 8000:8000 weather-mcp-server
```

### 测试服务器

```bash
# 测试健康检查端点（如果已实现）
curl http://localhost:8000/health

# 或者使用 MCP 客户端测试
python test_server.py
```

## 📝 Dockerfile 说明

### 基础镜像

```dockerfile
FROM python:3.10-slim
```

使用 Python 3.10 的精简版镜像，减小镜像体积。

### 工作目录

```dockerfile
WORKDIR /app
```

设置应用工作目录为 `/app`。

### 安装依赖

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

安装 Python 依赖包，`--no-cache-dir` 选项可以减小镜像体积。

### 暴露端口

```dockerfile
EXPOSE 8000
```

暴露 8000 端口。注意：HuggingFace Spaces 可能会使用不同的端口，通过 `PORT` 环境变量传递。

### 运行命令

```dockerfile
CMD python -c "import os; port = os.getenv('PORT', '8000'); exec('import uvicorn; from weather_server import mcp; uvicorn.run(mcp.http_app, host=\"0.0.0.0\", port=int(port))')"
```

动态读取 `PORT` 环境变量，如果未设置则使用默认端口 8000。

## 🌐 访问部署的服务器

部署完成后，您可以通过以下方式访问：

1. **Web 界面**: HuggingFace Space 会自动提供一个 Web 界面
2. **API 端点**: `https://your-username-weather-mcp-server.hf.space`

## 🔐 环境变量

如果需要配置环境变量（如 API 密钥），可以在 HuggingFace Space 设置中添加：

1. 进入 Space 设置页面
2. 找到 "Variables and secrets" 部分
3. 添加环境变量，例如：
   - `WEATHER_API_KEY`: 您的天气 API 密钥（如果需要）

## 📊 监控和日志

HuggingFace Spaces 提供：

- **构建日志**: 查看 Docker 构建过程
- **运行日志**: 查看应用运行时的日志
- **资源使用**: 监控 CPU 和内存使用情况

## 🐛 故障排除

### 构建失败

1. 检查 `Dockerfile` 语法是否正确
2. 确认 `requirements.txt` 中的包名和版本正确
3. 查看构建日志中的错误信息

### 运行失败

1. 检查应用日志
2. 确认端口配置正确
3. 验证代码中是否有语法错误

### 端口问题

如果 HuggingFace 使用不同的端口，确保代码能够读取 `PORT` 环境变量：

```python
import os
port = int(os.getenv('PORT', '8000'))
```

## 🔄 更新部署

每次推送到 Space 的代码仓库时，HuggingFace 会自动重新构建和部署。

## 📚 相关资源

- [HuggingFace Spaces 文档](https://huggingface.co/docs/hub/spaces)
- [Docker Spaces 指南](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [FastMCP 文档](https://fastmcp.wiki/)

## 💡 最佳实践

1. **使用 .dockerignore**: 排除不必要的文件，减小构建上下文
2. **多阶段构建**: 对于大型应用，考虑使用多阶段构建减小镜像体积
3. **健康检查**: 实现健康检查端点，便于监控
4. **日志记录**: 添加适当的日志记录，便于调试
5. **错误处理**: 确保应用有完善的错误处理机制

## 📄 许可证

本项目使用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

