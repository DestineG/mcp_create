# 快速设置指南

## 📍 首次设置（当前机器）

```bash
cd /home/liujiang/projects/tools/mcp_create

# 1. 提交到 Git
git add .
git commit -m "Initial commit: MCP servers collection"

# 2. 在 GitHub 上创建仓库
# 访问 https://github.com/new
# 创建名为 "mcp_create" 的仓库（不要初始化 README）

# 3. 推送到 GitHub
git remote add origin https://github.com/你的用户名/mcp_create.git
git branch -M main
git push -u origin main
```

## 🌍 在其他机器上使用

### 第一次安装

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/mcp_create.git
cd mcp_create

# 2. 一键安装所有 MCP
chmod +x install-all.sh
./install-all.sh

# 3. 配置 Claude Desktop
# 编辑配置文件（见下方）
```

### 后续更新

```bash
# 简单两步
cd mcp_create
git pull && ./install-all.sh
```

## 🔧 Claude Desktop 配置

**macOS**: 编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "scholar": {
      "command": "mcp-scholar",
      "env": {
        "OPENALEX_EMAIL": "your@email.com",
        "SEMANTIC_SCHOLAR_API_KEY": "optional"
      }
    }
  }
}
```

重启 Claude Desktop 即可使用。

## 📊 完整工作流示例

### 场景 1: 添加新的 MCP 项目

**开发机器**:
```bash
cd mcp_create

# 创建新项目
mkdir mcp-weather
cd mcp-weather
# ... 开发代码 ...

# 测试
cd ..
./install-all.sh

# 提交
git add .
git commit -m "Add mcp-weather"
git push
```

**其他机器**:
```bash
cd mcp_create
git pull
./install-all.sh  # 自动安装新项目
```

### 场景 2: 修改现有项目

**开发机器**:
```bash
cd mcp_create/mcp-scholar
# 修改代码...

cd ..
./install-all.sh  # 重新安装以测试

git add .
git commit -m "Fix: improve error handling"
git push
```

**其他机器**:
```bash
cd mcp_create
git pull
./install-all.sh  # 自动更新
```

## ✅ 验证清单

在每台机器上完成安装后，检查：

```bash
# 1. 检查已安装的 MCP
uv tool list

# 2. 检查可执行文件
which mcp-scholar

# 3. 测试运行（Ctrl+C 退出）
mcp-scholar

# 4. 在 Claude Desktop 中测试
# 打开 Claude Desktop，输入：
# "搜索关于 machine learning 的论文"
```

## 🎯 关键优势

✅ **一次配置，处处使用**  
✅ **Git 管理，版本清晰**  
✅ **源码安装，环境一致**  
✅ **自动发现，无需配置**  
✅ **一键操作，简单高效**

## 🚨 注意事项

1. **修改代码后必须运行** `./install-all.sh` **才能生效**
2. **每台机器都需要安装 uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **Claude Desktop 需要重启**才能识别新安装的 MCP
4. **不要提交** `dist/`, `dist-all/`, `.venv/` 到 Git（已在 .gitignore 中）

## 💡 小技巧

```bash
# 创建别名加速工作流
echo 'alias mcp-update="git pull && ./install-all.sh"' >> ~/.bashrc
source ~/.bashrc

# 使用
cd mcp_create
mcp-update  # 拉取最新代码并安装
```
