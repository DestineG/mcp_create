# Prompt: 创建 MCP Scholar - 学术论文搜索服务器

请帮我创建一个MCP (Model Context Protocol) server，用于搜索学术论文。

## 需求

**功能：**
1. 支持 OpenAlex 和 Semantic Scholar 两个数据源
2. 提供三个主要工具：
   - `search_papers`: 搜索论文
   - `get_paper_details`: 获取论文详情
   - `get_paper_citations`: 获取引用该论文的文献
3. 返回完整的论文元数据：标题、作者、年份、引用数、DOI、摘要、BibTeX等

**技术栈：**
- Python 3.10+
- MCP SDK (mcp>=1.0.0)
- httpx (异步HTTP客户端)
- pydantic (数据验证)

## 项目结构

```
mcp-scholar/
├── pyproject.toml
├── README.md
├── .gitignore
└── src/
    └── mcp_scholar/
        ├── __init__.py
        ├── __main__.py
        ├── server.py          # MCP服务器主文件
        ├── models.py          # Pydantic数据模型
        ├── openalex.py        # OpenAlex客户端
        └── semantic_scholar.py # Semantic Scholar客户端
```

## 核心代码要点

### 1. models.py - 数据模型
```python
from pydantic import BaseModel, Field
from typing import Optional

class Paper(BaseModel):
    id: str
    title: str
    authors: list[str]
    year: Optional[int] = None
    citations: int = 0
    doi: Optional[str] = None
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    abstract: Optional[str] = None
    venue: Optional[str] = None
    bibtex: Optional[str] = None

class SearchResult(BaseModel):
    papers: list[Paper]
    total: int
    source: str
    query: str
```

### 2. openalex.py - OpenAlex客户端
- API端点: `https://api.openalex.org`
- 无需API key，但提供email可获得更高限额
- 主要方法：
  - `search_papers(query, max_results, year_from, year_to, sort)`
  - `get_paper(paper_id)` - 支持OpenAlex ID或DOI
  - `get_citations(paper_id, max_results)`
- 注意：abstract存储为inverted index格式，需要重建
- 自动生成BibTeX引用

### 3. semantic_scholar.py - Semantic Scholar客户端
- API端点: `https://api.semanticscholar.org/graph/v1`
- 可选API key (环境变量 `SEMANTIC_SCHOLAR_API_KEY`)
- 类似的方法接口
- 可以直接获取BibTeX (在citationStyles字段)

### 4. server.py - MCP服务器
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("mcp-scholar")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_papers",
            description="搜索学术论文",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "source": {"type": "string", "enum": ["openalex", "semantic_scholar"], "default": "openalex"},
                    "max_results": {"type": "integer", "default": 10},
                    "year_from": {"type": "integer"},
                    "year_to": {"type": "integer"},
                    "sort": {"type": "string", "enum": ["relevance", "cited_by_count", "publication_date"]}
                },
                "required": ["query"]
            }
        ),
        # ... 其他工具
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # 处理工具调用
    pass

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())
```

### 5. pyproject.toml
```toml
[project]
name = "mcp-scholar"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]

[project.scripts]
mcp-scholar = "mcp_scholar.server:run"
```

## API参考

### OpenAlex
- 搜索: `GET /works?search={query}&per_page={limit}`
- 过滤: 使用 `filter` 参数，如 `publication_year:>=2020`
- 排序: `sort=cited_by_count:desc`
- 礼貌池: 添加 `mailto={email}` 参数

### Semantic Scholar
- 搜索: `GET /paper/search?query={query}&limit={limit}&fields=...`
- 年份过滤: `year=2020-2024`
- 字段: `paperId,title,authors,year,citationCount,abstract,venue,openAccessPdf,externalIds,url`

## 配置示例

Claude Desktop配置 (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "scholar": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-scholar", "run", "mcp-scholar"],
      "env": {
        "OPENALEX_EMAIL": "your@email.com",
        "SEMANTIC_SCHOLAR_API_KEY": "optional-key"
      }
    }
  }
}
```

## 注意事项

1. **错误处理**: 妥善处理HTTP 404、限流等错误
2. **抽象重建**: OpenAlex的abstract是inverted index，需要重建成字符串
3. **BibTeX生成**: 如果API不提供，需要自己生成，需要标注bib是否为自动生成
4. **异步清理**: 记得在适当时候调用 `client.aclose()`
5. **限流**: OpenAlex免费每天10万次，Semantic Scholar每5分钟100次

## 测试

创建测试脚本验证功能是否正常：
```python
import asyncio
from mcp_scholar.openalex import OpenAlexClient

async def test():
    client = OpenAlexClient()
    result = await client.search_papers("machine learning", max_results=3)
    for paper in result.papers:
        print(f"{paper.title} ({paper.year}) - {paper.citations} citations")
    await client.close()

asyncio.run(test())
```

---

请按照这个规范创建完整的MCP Scholar项目，包括所有文件和功能实现。确保代码质量、错误处理和文档完整。
