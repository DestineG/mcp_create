# MCP Scholar

一个用于搜索学术论文的 MCP (Model Context Protocol) 服务器，支持 OpenAlex 和 Semantic Scholar 两个数据源。

## 功能特性

- 🔍 **论文搜索**: 支持关键词搜索、年份过滤、排序
- 📄 **论文详情**: 获取完整的论文元数据，包括标题、作者、摘要、引用数等
- 📚 **引用分析**: 查看引用某篇论文的其他文献
- 📖 **BibTeX 导出**: 自动生成标准的 BibTeX 引用格式
- 🌐 **双数据源**: OpenAlex (无需 API key) 和 Semantic Scholar (可选 API key)

## 安装

### 使用 uv (推荐)

```bash
cd mcp-scholar
uv sync
```

### 使用 pip

```bash
cd mcp-scholar
pip install -e .
```

## 配置

### Claude Desktop

在 Claude Desktop 配置文件中添加以下内容 (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "scholar": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-scholar", "run", "mcp-scholar"],
      "env": {
        "OPENALEX_EMAIL": "your@email.com",
        "SEMANTIC_SCHOLAR_API_KEY": "optional-api-key"
      }
    }
  }
}
```

### 环境变量

- `OPENALEX_EMAIL`: (可选) 提供邮箱可获得更高的 API 限额
- `SEMANTIC_SCHOLAR_API_KEY`: (可选) Semantic Scholar API key

## 使用示例

### 搜索论文

```python
# 在 Claude Desktop 中使用
"搜索关于 transformer 的论文"
"查找 2020 年后关于强化学习的论文，按引用数排序"
```

### 获取论文详情

```python
"获取这篇论文的详细信息: 10.1038/nature14539"
```

### 查看论文引用

```python
"查看引用 Attention Is All You Need 这篇论文的文献"
```

## 工具列表

### 1. search_papers

搜索学术论文。

**参数**:
- `query` (必需): 搜索关键词
- `source`: 数据源 (`openalex` 或 `semantic_scholar`)，默认 `openalex`
- `max_results`: 最大结果数，默认 10
- `year_from`: 起始年份
- `year_to`: 结束年份
- `sort`: 排序方式 (`relevance`, `cited_by_count`, `publication_date`)

### 2. get_paper_details

获取论文详细信息。

**参数**:
- `paper_id` (必需): 论文 ID 或 DOI
- `source`: 数据源，默认 `openalex`

### 3. get_paper_citations

获取引用某篇论文的文献列表。

**参数**:
- `paper_id` (必需): 论文 ID 或 DOI
- `source`: 数据源，默认 `openalex`
- `max_results`: 最大结果数，默认 50

## API 限制

- **OpenAlex**: 免费，每天 10 万次请求，提供邮箱后可获得更高优先级
- **Semantic Scholar**: 免费层每 5 分钟 100 次请求，需要 API key 可获得更高限额

## 开发

### 运行测试

```bash
# 测试 OpenAlex
uv run python -c "
import asyncio
from src.mcp_scholar.openalex import OpenAlexClient

async def test():
    client = OpenAlexClient()
    result = await client.search_papers('machine learning', max_results=3)
    for paper in result.papers:
        print(f'{paper.title} ({paper.year}) - {paper.citations} citations')
    await client.close()

asyncio.run(test())
"
```

### 直接运行服务器

```bash
uv run mcp-scholar
```

## 项目结构

```
mcp-scholar/
├── pyproject.toml          # 项目配置
├── README.md               # 说明文档
├── .gitignore
└── src/
    └── mcp_scholar/
        ├── __init__.py
        ├── __main__.py
        ├── server.py       # MCP 服务器主文件
        ├── models.py       # Pydantic 数据模型
        ├── openalex.py     # OpenAlex API 客户端
        └── semantic_scholar.py  # Semantic Scholar API 客户端
```

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！
