# MCP 服务器集合

这个仓库集中管理多个 MCP (Model Context Protocol) 服务器项目。

## 🚀 快速开始

### 在任何机器上一键安装所有 MCP

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/mcp_create.git
cd mcp_create

# 2. 一键安装所有 MCP 服务器
chmod +x install-all.sh
./install-all.sh

# 3. 验证安装
uv tool list
```

就这么简单！✨

## 📦 包含的 MCP 服务器

- **mcp-scholar**: 学术论文搜索服务器
  - 支持 OpenAlex 和 Semantic Scholar
  - 提供论文搜索、详情查询、引用分析
  - [详细文档](./mcp-scholar/README.md)

## 🛠️ 开发工作流

### 当前机器（开发）

```bash
# 1. 创建新的 MCP 项目
mkdir mcp-weather
cd mcp-weather
# ... 开发项目 ...

# 2. 本地测试所有 MCP
cd ..
./install-all.sh

# 3. 提交到 Git
git add .
git commit -m "Add mcp-weather"
git push
```

### 其他机器（使用）

```bash
# 1. 拉取最新代码
cd mcp_create
git pull

# 2. 更新安装
./install-all.sh
```

**就是这么简单！** 不需要传输任何构建文件，所有机器都从源码安装。

## 📁 项目结构

```
mcp_create/
├── README.md              # 本文件
├── install-all.sh         # 一键安装脚本
├── build-all.sh           # 批量构建（可选）
├── .gitignore
├── mcp-scholar/           # MCP 项目 1
│   ├── src/
│   ├── pyproject.toml
│   └── README.md
└── mcp-xxx/               # MCP 项目 2
    ├── src/
    ├── pyproject.toml
    └── README.md
```

## 🔧 配置 Claude Desktop

安装完成后，编辑 Claude Desktop 配置文件：

**配置文件位置**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**添加配置**:
```json
{
  "mcpServers": {
    "scholar": {
      "command": "mcp-scholar",
      "env": {
        "OPENALEX_EMAIL": "your@email.com"
      }
    }
  }
}
```

重启 Claude Desktop 即可使用。

## 📝 添加新的 MCP 项目

1. 在 `mcp_create/` 下创建新目录
2. 确保包含 `pyproject.toml`
3. 提交到 Git
4. 在任何机器上运行 `git pull && ./install-all.sh`

**自动发现**：脚本会自动扫描并安装所有项目，无需修改任何配置！

## 🔄 更新工作流

### 修改现有 MCP 项目

```bash
# 1. 修改代码
cd mcp-scholar
# ... 修改 ...

# 2. 本地测试
cd ..
./install-all.sh

# 3. 提交
git add .
git commit -m "Update mcp-scholar"
git push
```

### 其他机器同步更新

```bash
git pull
./install-all.sh  # 自动更新所有修改过的项目
```

## 🗑️ 卸载

```bash
# 卸载所有 MCP
uv tool list | grep -E "^mcp-" | awk '{print $1}' | xargs -I {} uv tool uninstall {}

# 或单个卸载
uv tool uninstall mcp-scholar
```

## 📋 常见问题

### Q: 为什么不用构建好的 wheel 文件？
A: 源码安装更简单：
- ✅ 不需要维护 `dist-all/` 目录
- ✅ Git 仓库更小（不包含二进制文件）
- ✅ 修改后直接 `git pull` 即可，无需重新构建
- ✅ 所有机器环境一致

### Q: `install-all.sh` 做了什么？
A: 
1. 扫描所有包含 `pyproject.toml` 的子目录
2. 对每个项目执行 `uv tool install --force ./项目目录`
3. `--force` 确保安装最新版本（覆盖旧版）
4. 显示安装统计信息

### Q: 修改代码后必须重新安装吗？
A: 是的。`uv tool install` 是从源码安装到独立环境，修改源码不会自动生效。

### Q: 可以选择性安装某些项目吗？
A: 可以，直接安装单个项目：
```bash
uv tool install ./mcp-scholar
```

### Q: 如何验证 MCP 是否正常工作？
A: 
```bash
# 查看已安装的工具
uv tool list

# 测试运行（Ctrl+C 退出）
mcp-scholar
```

## 🎯 最佳实践

1. **单一仓库管理**：所有 MCP 项目放在一个仓库
2. **源码分发**：通过 Git 同步，不传输构建文件
3. **自动化安装**：使用 `install-all.sh` 统一安装
4. **版本控制**：用 Git 管理所有变更
5. **文档齐全**：每个项目都有独立的 README

## 🤝 贡献

欢迎添加新的 MCP 服务器项目！

## 📄 许可证

MIT
