import json
from mcp.server import Server
from mcp.types import Tool, TextContent
from .openalex import OpenAlexClient
from .semantic_scholar import SemanticScholarClient

app = Server("mcp-scholar")

openalex_client = None
semantic_scholar_client = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_papers",
            description="Search for academic papers from OpenAlex or Semantic Scholar. Returns paper metadata including title, authors, year, citations, DOI, abstract, and BibTeX.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for papers"
                    },
                    "source": {
                        "type": "string",
                        "enum": ["openalex", "semantic_scholar"],
                        "default": "openalex",
                        "description": "Data source to search"
                    },
                    "max_results": {
                        "type": "integer",
                        "default": 10,
                        "description": "Maximum number of results to return"
                    },
                    "year_from": {
                        "type": "integer",
                        "description": "Filter papers from this year onwards"
                    },
                    "year_to": {
                        "type": "integer",
                        "description": "Filter papers up to this year"
                    },
                    "sort": {
                        "type": "string",
                        "enum": ["relevance", "cited_by_count", "publication_date"],
                        "default": "relevance",
                        "description": "Sort order for results"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_paper_details",
            description="Get detailed information about a specific paper using its ID or DOI. Returns complete metadata including abstract and BibTeX citation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "Paper ID (OpenAlex ID, Semantic Scholar ID, or DOI)"
                    },
                    "source": {
                        "type": "string",
                        "enum": ["openalex", "semantic_scholar"],
                        "default": "openalex",
                        "description": "Data source to use"
                    }
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="get_paper_citations",
            description="Get papers that cite a specific paper. Useful for finding related work and tracking paper impact.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "Paper ID (OpenAlex ID, Semantic Scholar ID, or DOI)"
                    },
                    "source": {
                        "type": "string",
                        "enum": ["openalex", "semantic_scholar"],
                        "default": "openalex",
                        "description": "Data source to use"
                    },
                    "max_results": {
                        "type": "integer",
                        "default": 50,
                        "description": "Maximum number of citing papers to return"
                    }
                },
                "required": ["paper_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    global openalex_client, semantic_scholar_client

    if openalex_client is None:
        openalex_client = OpenAlexClient()
    if semantic_scholar_client is None:
        semantic_scholar_client = SemanticScholarClient()

    try:
        if name == "search_papers":
            source = arguments.get("source", "openalex")
            query = arguments["query"]
            max_results = arguments.get("max_results", 10)
            year_from = arguments.get("year_from")
            year_to = arguments.get("year_to")
            sort = arguments.get("sort", "relevance")

            client = openalex_client if source == "openalex" else semantic_scholar_client
            result = await client.search_papers(
                query=query,
                max_results=max_results,
                year_from=year_from,
                year_to=year_to,
                sort=sort
            )

            response = {
                "source": result.source,
                "query": result.query,
                "total": result.total,
                "count": len(result.papers),
                "papers": [paper.model_dump() for paper in result.papers]
            }

            return [TextContent(
                type="text",
                text=json.dumps(response, indent=2, ensure_ascii=False)
            )]

        elif name == "get_paper_details":
            source = arguments.get("source", "openalex")
            paper_id = arguments["paper_id"]

            client = openalex_client if source == "openalex" else semantic_scholar_client
            paper = await client.get_paper(paper_id)

            return [TextContent(
                type="text",
                text=json.dumps(paper.model_dump(), indent=2, ensure_ascii=False)
            )]

        elif name == "get_paper_citations":
            source = arguments.get("source", "openalex")
            paper_id = arguments["paper_id"]
            max_results = arguments.get("max_results", 50)

            client = openalex_client if source == "openalex" else semantic_scholar_client
            result = await client.get_citations(paper_id, max_results)

            response = {
                "source": result.source,
                "paper_id": paper_id,
                "total": result.total,
                "count": len(result.papers),
                "citing_papers": [paper.model_dump() for paper in result.papers]
            }

            return [TextContent(
                type="text",
                text=json.dumps(response, indent=2, ensure_ascii=False)
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
