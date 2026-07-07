# MCP 服务器集合

这个仓库集中管理多个 MCP (Model Context Protocol) 服务器项目，支持一键批量安装。

## 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/DestineG/mcp_create.git
cd mcp_create

# 2. 一键安装所有 MCP（自动运行测试）
chmod +x install-all.sh
./install-all.sh

# 3. 配置到 Claude CLI
claude mcp add scholar mcp-scholar
claude mcp add time mcp-time

# 4. 验证
claude mcp list
```

就这么简单！✨

> **注意**: `install-all.sh` 会在安装前自动运行每个项目的测试套件，确保代码质量。

## 📦 包含的 MCP 服务器

| 项目 | 描述 | 工具数 | 测试数 | 文档 |
|------|------|--------|--------|------|
| **mcp-scholar** | 学术论文搜索（OpenAlex + Semantic Scholar） | 3 | 9 | [详细说明](#mcp-scholar-使用) |
| **mcp-time** | 时区和时间工具 | 3 | 11 | [详细说明](#mcp-time-使用) |

### mcp-scholar 使用

提供 3 个工具：

**1. search_papers** - 搜索论文
```
参数：
  - query: 搜索关键词（必需）
  - source: 数据源 (openalex/semantic_scholar)，默认 openalex
  - max_results: 最大结果数，默认 10
  - year_from: 起始年份
  - year_to: 结束年份
  - sort: 排序方式 (relevance/cited_by_count/publication_date)

示例：
  "搜索关于深度学习的论文"
  "查找 2020 年后关于强化学习的论文，按引用数排序"
```

**2. get_paper_details** - 获取论文详情
```
参数：
  - paper_id: 论文 ID 或 DOI（必需）
  - source: 数据源，默认 openalex

示例：
  "获取这篇论文的详细信息: 10.1038/nature14539"
```

**3. get_paper_citations** - 获取引用文献
```
参数：
  - paper_id: 论文 ID 或 DOI（必需）
  - source: 数据源，默认 openalex
  - max_results: 最大结果数，默认 50

示例：
  "查看引用 Attention Is All You Need 的文献"
```

### mcp-time 使用

提供 3 个工具：

**1. get_current_time** - 获取当前时间
```
参数：
  - timezone: 时区名称（如 'Asia/Shanghai'），默认 UTC
  - format: 格式 (iso/unix/human)，默认 iso

示例：
  "现在北京时间几点？"
  "东京现在几点？"
```

**2. convert_timezone** - 时区转换
```
参数：
  - time: ISO 格式时间（必需）
  - from_timezone: 源时区，默认 UTC
  - to_timezone: 目标时区（必需）

示例：
  "把纽约时间 2024-01-01 12:00 转换成上海时间"
```

**3. list_timezones** - 列出时区
```
参数：
  - region: 按区域筛选（如 'Asia', 'America'）

示例：
  "列出所有亚洲的时区"
```

## 💡 使用提示

**MCP 服务器不是传统 CLI 工具**：
- ❌ 不支持 `mcp-scholar --help`
- ❌ 不能直接在终端运行
- ✅ 通过 Claude CLI 自动调用
- ✅ 只需用自然语言描述需求

**示例对话**：
```
你: "搜索关于机器学习的论文"
Claude: [自动调用 search_papers 工具]

你: "现在纽约几点？"
Claude: [自动调用 get_current_time 工具]
```

## 🛠️ 开发工作流

### 添加新的 MCP 项目

```bash
cd mcp_create

# 1. 创建新项目目录
mkdir mcp-weather
cd mcp-weather

# 2. 创建项目结构（参考下面的模板）
mkdir -p src/mcp_weather tests
touch src/mcp_weather/__init__.py
touch src/mcp_weather/__main__.py
touch src/mcp_weather/server.py
touch tests/__init__.py
touch tests/test_weather.py
touch pyproject.toml
touch pytest.ini
touch README.md

# 3. 编写代码和测试（参考开发规范）

# 4. 本地测试和安装
cd ..
./install-all.sh  # 自动运行测试并安装

# 5. 提交
git add .
git commit -m "Add mcp-weather"
git push
```

**自动发现**：脚本会扫描所有包含 `pyproject.toml` 的子目录，无需配置！

**自动测试**：安装前自动运行 `pytest`，测试失败则跳过安装。

### 修改现有项目

```bash
# 1. 修改代码
cd mcp-scholar
# ... 修改 ...

# 2. 运行测试
uv run pytest -v

# 3. 重新安装
cd ..
./install-all.sh  # 自动运行测试并重新安装

# 4. 提交
git add .
git commit -m "Update mcp-scholar"
git push
```

**跳过测试**（不推荐）：
```bash
RUN_TESTS=false ./install-all.sh
```

### 其他机器同步更新

```bash
cd mcp_create
git pull && ./install-all.sh
```

## 🔧 配置 Claude CLI

### 方法 1: 一键配置（推荐）

```bash
chmod +x configure-claude-cli.sh
./configure-claude-cli.sh
```

### 方法 2: 手动配置

```bash
# 添加 mcp-scholar
claude mcp add scholar mcp-scholar

# 添加 mcp-time
claude mcp add time mcp-time

# 验证配置
claude mcp list
```

输出示例：
```
scholar: mcp-scholar  - ✓ Connected
time: mcp-time  - ✓ Connected
```

配置会立即生效，无需重启！

## 📋 MCP 开发规范

### 标准项目结构

```
mcp-xxx/
├── src/
│   └── mcp_xxx/
│       ├── __init__.py
│       ├── __main__.py
│       ├── server.py          # MCP 服务器主文件
│       └── [其他模块].py
├── tests/                     # ✅ 必需：单元测试
│   ├── __init__.py
│   ├── test_xxx.py
│   └── README.md
├── pyproject.toml             # 项目配置
├── pytest.ini                 # pytest 配置
├── README.md                  # 项目文档
└── .gitignore
```

### pyproject.toml 模板

```toml
[project]
name = "mcp-xxx"
version = "0.1.0"
description = "简短描述"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    # 其他依赖
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",  # 如果有异步测试
]

[project.scripts]
mcp-xxx = "mcp_xxx.server:run"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mcp_xxx"]
```

### server.py 模板

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import json

app = Server("mcp-xxx")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="tool_name",
            description="工具描述",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "参数描述"
                    }
                },
                "required": ["param1"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "tool_name":
            result = {"key": "value"}
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

def run():
    import asyncio
    asyncio.run(main())
```

### 测试模板 (tests/test_xxx.py)

```python
import pytest
import pytest_asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_xxx.server import app

class TestXXXTools:
    """测试工具功能"""
    
    @pytest.mark.asyncio
    async def test_tool_basic(self):
        """基本功能测试"""
        # 测试代码
        assert True

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
```

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### 开发检查清单

创建新 MCP 项目时，确保：

- [ ] 项目结构符合标准
- [ ] pyproject.toml 配置正确
- [ ] 实现了 `list_tools()` 和 `call_tool()`
- [ ] 添加了单元测试（tests/ 目录）
- [ ] 所有测试通过（`uv run pytest -v`）
- [ ] README 包含完整文档
- [ ] 工具参数有详细的 inputSchema
- [ ] 错误处理完善
- [ ] 返回 JSON 格式数据
- [ ] 使用 `ensure_ascii=False` 支持中文

### 测试要求

每个 MCP 项目必须包含测试：

1. **单元测试**：测试核心功能逻辑
2. **集成测试**：测试 API 调用（如果有外部依赖）
3. **边界测试**：测试异常情况和边界条件
4. **覆盖率**：争取 80%+ 代码覆盖率

### 最佳实践

1. **工具命名**：使用 `snake_case`，简洁明了
2. **参数设计**：必需参数尽量少，提供合理默认值
3. **错误处理**：捕获所有异常，返回友好错误信息
4. **文档完整**：每个工具都要有清晰的描述和示例
5. **测试覆盖**：关键功能必须有测试
6. **日志记录**：适当使用日志，便于调试
7. **性能考虑**：避免阻塞操作，使用异步 I/O

## 📁 项目结构

```
mcp_create/
├── README.md                      # 本文件
├── install-all.sh                 # 批量安装脚本（自动测试）
├── configure-claude-cli.sh        # 自动配置 Claude CLI（可选）
├── .gitignore
├── mcp-scholar/                   # 学术论文搜索
│   ├── src/mcp_scholar/
│   ├── tests/                     # 9 个单元测试
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── README.md
└── mcp-time/                      # 时区工具
    ├── src/mcp_time/
    ├── tests/                     # 11 个单元测试
    ├── pyproject.toml
    ├── pytest.ini
    └── README.md
```

## 📋 常见问题

**Q: 修改代码后必须重新安装吗？**  
A: 是的。运行 `./install-all.sh` 使修改生效。

**Q: 可以只安装某个项目吗？**  
A: 可以。`uv tool install ./mcp-scholar`

**Q: 如何跳过测试安装？**  
A: `RUN_TESTS=false ./install-all.sh`（不推荐，可能安装有问题的代码）

**Q: 如何单独运行某个项目的测试？**  
A: `cd mcp-scholar && uv run pytest -v`

**Q: 如何卸载？**  
A: 单个卸载：`uv tool uninstall mcp-scholar`  
   全部卸载：`uv tool list | grep -E "^mcp-" | awk '{print $1}' | xargs -I {} uv tool uninstall {}`

**Q: 为什么用源码安装而不是 wheel 文件？**  
A: 源码安装更简单：Git 仓库更小，修改后直接 `git pull` 即可，所有机器环境一致。

**Q: 如何确保代码质量？**  
A: 每个项目都包含完整的单元测试套件，`install-all.sh` 会在安装前自动运行测试。

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
3. Claude CLI 无需重启，配置立即生效
4. 不要提交构建文件（已在 .gitignore 中配置）
5. 确保每个项目包含测试套件（tests/ 目录）
6. 添加新 MCP 时请遵循上面的开发规范

## 🎯 核心优势

- ✅ 在当前目录统一管理所有 MCP
- ✅ 通过 Git 同步到其他机器
- ✅ 一键安装所有 MCP 服务器
- ✅ 自动发现新项目，无需配置
- ✅ 源码分发，环境一致
- ✅ 自动测试，确保代码质量
- ✅ 完整的开发规范和模板
- ✅ 20 个单元测试覆盖核心功能

## 📄 许可证

MIT
