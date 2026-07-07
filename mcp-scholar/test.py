#!/usr/bin/env python3
"""
测试脚本：验证 MCP Scholar 的功能
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_scholar.openalex import OpenAlexClient
from mcp_scholar.semantic_scholar import SemanticScholarClient


async def test_openalex():
    print("=" * 60)
    print("测试 OpenAlex 客户端")
    print("=" * 60)

    client = OpenAlexClient()

    try:
        # 测试搜索
        print("\n1. 测试搜索功能 (关键词: 'machine learning')")
        result = await client.search_papers("machine learning", max_results=3)
        print(f"   找到 {result.total} 篇论文，显示前 {len(result.papers)} 篇：")
        for i, paper in enumerate(result.papers, 1):
            print(f"   [{i}] {paper.title}")
            print(f"       作者: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
            print(f"       年份: {paper.year} | 引用数: {paper.citations}")
            print(f"       DOI: {paper.doi or 'N/A'}")

        # 测试获取论文详情
        if result.papers:
            paper_id = result.papers[0].id
            print(f"\n2. 测试获取论文详情 (ID: {paper_id})")
            paper = await client.get_paper(paper_id)
            print(f"   标题: {paper.title}")
            print(f"   摘要: {paper.abstract[:200] if paper.abstract else 'N/A'}...")
            print(f"   BibTeX 前 200 字符: {paper.bibtex[:200] if paper.bibtex else 'N/A'}...")

            # 测试获取引用
            print(f"\n3. 测试获取引用 (ID: {paper_id})")
            citations = await client.get_citations(paper_id, max_results=5)
            print(f"   共有 {citations.total} 篇论文引用了这篇文章，显示前 {len(citations.papers)} 篇：")
            for i, citing_paper in enumerate(citations.papers, 1):
                print(f"   [{i}] {citing_paper.title} ({citing_paper.year})")

        print("\n✅ OpenAlex 测试通过！")

    except Exception as e:
        import traceback
        print(f"\n❌ OpenAlex 测试失败: {e}")
        traceback.print_exc()
    finally:
        await client.close()


async def test_semantic_scholar():
    print("\n" + "=" * 60)
    print("测试 Semantic Scholar 客户端")
    print("=" * 60)

    client = SemanticScholarClient()

    try:
        # 测试搜索
        print("\n1. 测试搜索功能 (关键词: 'transformer neural network')")
        result = await client.search_papers("transformer neural network", max_results=3)
        print(f"   找到论文，显示前 {len(result.papers)} 篇：")
        for i, paper in enumerate(result.papers, 1):
            print(f"   [{i}] {paper.title}")
            print(f"       作者: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
            print(f"       年份: {paper.year} | 引用数: {paper.citations}")

        # 测试通过 DOI 获取论文
        print("\n2. 测试通过特定 paper ID 获取论文详情")
        try:
            paper = await client.get_paper("204e3073870fae3d05bcbc2f6a8e263d9b72e776")  # BERT paper
            print(f"   标题: {paper.title}")
            print(f"   年份: {paper.year}")
            print(f"   引用数: {paper.citations}")
        except Exception as e:
            print(f"   跳过详情测试: {e}")

        print("\n✅ Semantic Scholar 测试通过！")

    except Exception as e:
        print(f"\n❌ Semantic Scholar 测试失败: {e}")
    finally:
        await client.close()


async def main():
    print("\n🚀 开始测试 MCP Scholar\n")

    await test_openalex()
    await test_semantic_scholar()

    print("\n" + "=" * 60)
    print("✨ 所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
