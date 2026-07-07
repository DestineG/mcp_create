# 测试

运行测试：

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 运行所有测试
uv run pytest

# 运行并显示详细输出
uv run pytest -v

# 运行并显示覆盖率
uv run pytest --cov=mcp_scholar --cov-report=html
```
