"""
MCP Scholar 测试套件
使用 pytest 进行单元测试和集成测试
"""

import asyncio
import pytest
import pytest_asyncio
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_scholar.openalex import OpenAlexClient
from mcp_scholar.semantic_scholar import SemanticScholarClient
from mcp_scholar.models import Paper, SearchResult


class TestOpenAlexAPI:
    """测试 OpenAlex API 集成"""

    @pytest_asyncio.fixture
    async def client(self):
        client = OpenAlexClient()
        yield client
        await client.close()

    @pytest.mark.asyncio
    async def test_search_basic(self, client):
        """基本搜索功能"""
        result = await client.search_papers("machine learning", max_results=2)
        assert isinstance(result, SearchResult)
        assert result.total > 0
        assert len(result.papers) <= 2

    @pytest.mark.asyncio
    async def test_search_year_range(self, client):
        """年份范围过滤"""
        result = await client.search_papers("deep learning", max_results=2, year_from=2023, year_to=2024)
        assert result.total > 0
        for paper in result.papers:
            if paper.year:
                assert 2023 <= paper.year <= 2024

    @pytest.mark.asyncio
    async def test_search_year_from_only(self, client):
        """只有起始年份"""
        result = await client.search_papers("AI", max_results=2, year_from=2023)
        assert result.total > 0

    @pytest.mark.asyncio
    async def test_search_year_to_only(self, client):
        """只有结束年份"""
        result = await client.search_papers("ML", max_results=2, year_to=2024)
        assert result.total > 0

    @pytest.mark.asyncio
    async def test_search_sort_citations(self, client):
        """按引用数排序"""
        result = await client.search_papers("transformer", max_results=3, sort="cited_by_count")
        assert result.total > 0
        if len(result.papers) > 1:
            citations = [p.citations for p in result.papers]
            assert citations == sorted(citations, reverse=True)

    @pytest.mark.asyncio
    async def test_get_paper_details(self, client):
        """获取论文详情"""
        search = await client.search_papers("machine learning", max_results=1)
        paper_id = search.papers[0].id
        paper = await client.get_paper(paper_id)
        assert paper.id == paper_id
        assert paper.title
        assert len(paper.authors) > 0

    @pytest.mark.asyncio
    async def test_get_citations(self, client):
        """获取引用文献"""
        search = await client.search_papers("deep learning", max_results=1, sort="cited_by_count")
        paper_id = search.papers[0].id
        citations = await client.get_citations(paper_id, max_results=5)
        assert citations.total > 0
        assert len(citations.papers) <= 5


class TestSemanticScholarAPI:
    """测试 Semantic Scholar API 集成"""

    @pytest_asyncio.fixture
    async def client(self):
        client = SemanticScholarClient()
        yield client
        await client.close()

    @pytest.mark.asyncio
    async def test_search_basic(self, client):
        """基本搜索（可能遇到速率限制）"""
        try:
            result = await client.search_papers("machine learning", max_results=2)
            assert isinstance(result, SearchResult)
        except Exception as e:
            if "429" in str(e):
                pytest.skip("Rate limit (expected)")
            else:
                raise


class TestDataModels:
    """测试数据模型"""

    def test_paper_creation(self):
        paper = Paper(id="W123", title="Test", authors=["A"], citations=10)
        assert paper.id == "W123"
        assert paper.title == "Test"

    def test_search_result_creation(self):
        papers = [Paper(id="1", title="P1", authors=["A"], citations=1)]
        result = SearchResult(papers=papers, total=100, source="openalex", query="test")
        assert len(result.papers) == 1
        assert result.total == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
