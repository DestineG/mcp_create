# MCP Scholar 开发指南

## 修改源码后更新

### 方法 1: 强制重装（推荐）
```bash
cd /path/to/mcp-scholar
uv tool install --force .
```

### 方法 2: 先卸载再安装
```bash
uv tool uninstall mcp-scholar
cd /path/to/mcp-scholar
uv tool install .
```

### 开发模式（不推荐用于 MCP）
```bash
# 这种方式会安装可编辑版本，但 MCP 服务器可能会遇到路径问题
uv tool install --editable .
```

---

## 在其他机器上安装

### 方法 1: 从本地目录安装（需要源码）

```bash
# 1. 复制整个项目到目标机器
scp -r mcp-scholar user@remote-machine:/path/to/

# 2. 在目标机器上安装
ssh user@remote-machine
cd /path/to/mcp-scholar
uv tool install .
```

### 方法 2: 从 Git 仓库安装（推荐）

```bash
# 首先将项目推送到 Git
cd mcp-scholar
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/mcp-scholar.git
git push -u origin main

# 在其他机器上直接从 Git 安装
uv tool install git+https://github.com/username/mcp-scholar.git
```

### 方法 3: 打包发布到 PyPI（适合公开发布）

```bash
# 1. 构建包
cd mcp-scholar
uv build

# 2. 发布到 PyPI（需要 PyPI 账号）
uv publish

# 3. 在任何机器上安装
uv tool install mcp-scholar
```

### 方法 4: 打包成 wheel 文件（适合内部分发）

```bash
# 1. 在源机器上构建
cd mcp-scholar
uv build
# 会生成 dist/mcp_scholar-0.1.0-py3-none-any.whl

# 2. 复制 wheel 文件到目标机器
scp dist/mcp_scholar-0.1.0-py3-none-any.whl user@remote:/tmp/

# 3. 在目标机器上安装
uv tool install /tmp/mcp_scholar-0.1.0-py3-none-any.whl
```

---

## 配置 Claude Desktop（在任何机器上）

安装完成后，在 Claude Desktop 配置文件中添加：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "scholar": {
      "command": "mcp-scholar",
      "env": {
        "OPENALEX_EMAIL": "your@email.com",
        "SEMANTIC_SCHOLAR_API_KEY": "optional-key"
      }
    }
  }
}
```

---

## 验证安装

```bash
# 检查是否安装成功
which mcp-scholar
uv tool list

# 测试运行（Ctrl+C 退出）
mcp-scholar
```

---

## 常见问题

### Q: uv tool install 和 pip install 有什么区别？
A: 
- `uv tool install`: 安装到独立环境，不污染全局 Python，适合 CLI 工具
- `pip install`: 安装到当前 Python 环境，可能导致依赖冲突

### Q: 修改了代码但忘记重新安装，会怎样？
A: 运行的还是旧版本代码，修改不会生效

### Q: 如何查看当前安装的版本？
A: 
```bash
uv tool list | grep mcp-scholar
```

### Q: 如何在开发时快速测试而不重装？
A: 
```bash
# 直接在项目目录运行
cd mcp-scholar
uv run python -m mcp_scholar.server
```
