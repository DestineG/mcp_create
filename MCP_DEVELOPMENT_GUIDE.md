# MCP 项目开发规范

## 📋 项目结构

标准的 MCP 项目应包含以下结构：

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

## 📝 必需文件

### 1. pyproject.toml

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

### 2. server.py 模板

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

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

### 3. tests/test_xxx.py

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

### 4. pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### 5. README.md

应包含以下章节：

```markdown
# MCP XXX

简短描述

## 功能特性

- 功能 1
- 功能 2

## 安装

\`\`\`bash
uv tool install .
\`\`\`

## 工具列表

### tool_name

描述和参数说明

## 使用示例

在 Claude CLI 中的自然语言示例

## 测试

\`\`\`bash
uv run pytest -v
\`\`\`

## 许可证

MIT
```

## ✅ 开发检查清单

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

## 🧪 测试要求

每个 MCP 项目必须包含测试：

1. **单元测试**：测试核心功能逻辑
2. **集成测试**：测试 API 调用（如果有外部依赖）
3. **边界测试**：测试异常情况和边界条件
4. **覆盖率**：争取 80%+ 代码覆盖率

## 📦 发布流程

1. 确保所有测试通过
2. 更新版本号（pyproject.toml）
3. 提交代码到 Git
4. 运行 `./install-all.sh` 测试批量安装
5. 运行 `./configure-claude-cli.sh` 验证配置
6. 推送到 GitHub

## 💡 最佳实践

1. **工具命名**：使用 `snake_case`，简洁明了
2. **参数设计**：必需参数尽量少，提供合理默认值
3. **错误处理**：捕获所有异常，返回友好错误信息
4. **文档完整**：每个工具都要有清晰的描述和示例
5. **测试覆盖**：关键功能必须有测试
6. **日志记录**：适当使用日志，便于调试
7. **性能考虑**：避免阻塞操作，使用异步 I/O

## 🔍 示例项目

参考现有项目：

- **mcp-scholar**：复杂的 API 集成，多数据源
- **mcp-time**：简单的工具集合，无外部依赖

## 📚 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [pytest 文档](https://docs.pytest.org/)
