# MCP 服务器集合

这个仓库集中管理多个 MCP (Model Context Protocol) 服务器项目，支持一键批量安装。

## 🚀 快速开始

### 首次设置（推送到 GitHub）

```bash
# 1. 在 GitHub 创建仓库
# 访问 https://github.com/new
# 创建名为 "mcp_create" 的仓库（不要初始化 README）

# 2. 推送代码
git remote add origin https://github.com/你的用户名/mcp_create.git
git branch -M main
git push -u origin main
```

### 在任何机器上使用

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/mcp_create.git
cd mcp_create

# 2. 一键安装所有 MCP
chmod +x install-all.sh
./install-all.sh

# 3. 验证
uv tool list
```

就这么简单！✨

## 📦 包含的 MCP 服务器

| 项目 | 描述 | 工具数 |
|------|------|--------|
| **mcp-scholar** | 学术论文搜索（OpenAlex + Semantic Scholar） | 3 |
| **mcp-time** | 时区和时间工具 | 3 |

详细文档见各项目的 README。

## 🛠️ 开发工作流

### 添加新的 MCP 项目

```bash
cd mcp_create

# 1. 创建新项目
mkdir mcp-weather
cd mcp-weather
# ... 开发代码，确保包含 pyproject.toml ...

# 2. 本地测试
cd ..
./install-all.sh  # 自动发现并安装新项目

# 3. 提交
git add .
git commit -m "Add mcp-weather"
git push
```

**自动发现**：脚本会扫描所有包含 `pyproject.toml` 的子目录，无需配置！

### 修改现有项目

```bash
# 1. 修改代码
cd mcp-scholar
# ... 修改 ...

# 2. 测试
cd ..
./install-all.sh  # 重新安装

# 3. 提交
git add .
git commit -m "Update mcp-scholar"
git push
```

### 其他机器同步更新

```bash
cd mcp_create
git pull && ./install-all.sh
```

## 🔧 配置 Claude CLI

```bash
# 一键配置所有已安装的 MCP 到 Claude CLI
chmod +x configure-claude-cli.sh
./configure-claude-cli.sh
```

配置会立即生效，无需重启！

### 手动配置（可选）

编辑 `~/.claude/settings.json`，添加：

```json
{
  "mcpServers": {
    "scholar": {
      "command": "mcp-scholar"
    },
    "time": {
      "command": "mcp-time"
    }
  }
}
```

## 📁 项目结构

```
mcp_create/
├── README.md                 # 本文件
├── install-all.sh            # 批量安装脚本
├── configure-claude-cli.sh   # 自动配置 Claude CLI
├── .gitignore
├── mcp-scholar/              # 学术论文搜索
│   ├── src/mcp_scholar/
│   ├── pyproject.toml
│   └── README.md
└── mcp-time/                 # 时区工具
    ├── src/mcp_time/
    ├── pyproject.toml
    └── README.md
```

## 📋 常见问题

**Q: 修改代码后必须重新安装吗？**  
A: 是的。运行 `./install-all.sh` 使修改生效。

**Q: 可以只安装某个项目吗？**  
A: 可以。`uv tool install ./mcp-scholar`

**Q: 如何卸载？**  
A: 单个卸载：`uv tool uninstall mcp-scholar`  
   全部卸载：`uv tool list | grep -E "^mcp-" | awk '{print $1}' | xargs -I {} uv tool uninstall {}`

**Q: 为什么用源码安装而不是 wheel 文件？**  
A: 源码安装更简单：Git 仓库更小，修改后直接 `git pull` 即可，所有机器环境一致。

## 💡 小技巧

创建别名加速工作流：

```bash
echo 'alias mcp-sync="git pull && ./install-all.sh"' >> ~/.bashrc
source ~/.bashrc

# 使用
cd mcp_create
mcp-sync  # 一键同步并安装
```

## 🚨 注意事项

1. 每台机器需要先安装 uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. 修改代码后必须运行 `./install-all.sh` 才能生效
3. Claude Desktop 需要重启才能识别新安装的 MCP
4. 不要提交构建文件（已在 .gitignore 中配置）

## 🎯 核心优势

- ✅ 在当前目录统一管理所有 MCP
- ✅ 通过 Git 同步到其他机器
- ✅ 一键安装所有 MCP 服务器
- ✅ 自动发现新项目，无需配置
- ✅ 源码分发，环境一致

## 📄 许可证

MIT
