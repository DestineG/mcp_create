import os
import httpx
from typing import Optional
from .models import Paper, SearchResult


class SemanticScholarClient:
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.api_key = api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        await self.client.aclose()

    def _get_headers(self) -> dict:
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        return headers

    async def search_papers(
        self,
        query: str,
        max_results: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort: str = "relevance"
    ) -> SearchResult:
        params = {
            "query": query,
            "limit": min(max_results, 100),
            "fields": "paperId,title,authors,year,citationCount,abstract,venue,openAccessPdf,externalIds,url,citationStyles"
        }

        if year_from and year_to:
            params["year"] = f"{year_from}-{year_to}"
        elif year_from:
            params["year"] = f"{year_from}-"
        elif year_to:
            params["year"] = f"-{year_to}"

        try:
            response = await self.client.get(
                f"{self.base_url}/paper/search",
                params=params,
                headers=self._get_headers()
            )
            response.raise_for_status()
            data = response.json()

            papers = []
            for paper_data in data.get("data", []):
                papers.append(self._parse_paper(paper_data))

            return SearchResult(
                papers=papers,
                total=data.get("total", len(papers)),
                source="semantic_scholar",
                query=query
            )
        except httpx.HTTPError as e:
            raise Exception(f"Semantic Scholar API error: {str(e)}")

    async def get_paper(self, paper_id: str) -> Paper:
        fields = "paperId,title,authors,year,citationCount,abstract,venue,openAccessPdf,externalIds,url,citationStyles"

        try:
            response = await self.client.get(
                f"{self.base_url}/paper/{paper_id}",
                params={"fields": fields},
                headers=self._get_headers()
            )
            response.raise_for_status()
            paper_data = response.json()
            return self._parse_paper(paper_data)
        except httpx.HTTPError as e:
            raise Exception(f"Semantic Scholar API error: {str(e)}")

    async def get_citations(self, paper_id: str, max_results: int = 50) -> SearchResult:
        fields = "paperId,title,authors,year,citationCount,abstract,venue,openAccessPdf,externalIds,url,citationStyles"

        params = {
            "fields": fields,
            "limit": min(max_results, 1000)
        }

        try:
            response = await self.client.get(
                f"{self.base_url}/paper/{paper_id}/citations",
                params=params,
                headers=self._get_headers()
            )
            response.raise_for_status()
            data = response.json()

            papers = []
            for citation in data.get("data", []):
                citing_paper = citation.get("citingPaper", {})
                if citing_paper:
                    papers.append(self._parse_paper(citing_paper))

            return SearchResult(
                papers=papers,
                total=len(papers),
                source="semantic_scholar",
                query=f"citations:{paper_id}"
            )
        except httpx.HTTPError as e:
            raise Exception(f"Semantic Scholar API error: {str(e)}")

    def _parse_paper(self, paper_data: dict) -> Paper:
        authors = []
        for author in paper_data.get("authors", []):
            if author.get("name"):
                authors.append(author["name"])

        external_ids = paper_data.get("externalIds", {})
        doi = external_ids.get("DOI")

        pdf_url = None
        open_access = paper_data.get("openAccessPdf")
        if open_access and open_access.get("url"):
            pdf_url = open_access["url"]

        bibtex = None
        citation_styles = paper_data.get("citationStyles", {})
        if citation_styles and citation_styles.get("bibtex"):
            bibtex = citation_styles["bibtex"]
        else:
            bibtex = self._generate_bibtex(paper_data, authors, doi)

        return Paper(
            id=paper_data.get("paperId", ""),
            title=paper_data.get("title", ""),
            authors=authors,
            year=paper_data.get("year"),
            citations=paper_data.get("citationCount", 0),
            doi=doi,
            url=paper_data.get("url"),
            pdf_url=pdf_url,
            abstract=paper_data.get("abstract"),
            venue=paper_data.get("venue"),
            bibtex=bibtex
        )

    def _generate_bibtex(self, paper_data: dict, authors: list[str], doi: Optional[str]) -> str:
        paper_id = paper_data.get("paperId", "unknown")
        title = paper_data.get("title", "Untitled")
        year = paper_data.get("year", "n.d.")
        venue = paper_data.get("venue", "")

        author_str = " and ".join(authors) if authors else "Unknown"

        bibtex = f"@article{{{paper_id},\n"
        bibtex += f"  title = {{{title}}},\n"
        bibtex += f"  author = {{{author_str}}},\n"
        bibtex += f"  year = {{{year}}},\n"
        if venue:
            bibtex += f"  journal = {{{venue}}},\n"
        if doi:
            bibtex += f"  doi = {{{doi}}},\n"
        bibtex += f"  note = {{Auto-generated from Semantic Scholar}}\n"
        bibtex += "}"

        return bibtex
