import os
import httpx
from typing import Optional
from .models import Paper, SearchResult


class OpenAlexClient:
    def __init__(self, email: Optional[str] = None):
        self.base_url = "https://api.openalex.org"
        self.email = email or os.getenv("OPENALEX_EMAIL")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        await self.client.aclose()

    async def search_papers(
        self,
        query: str,
        max_results: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort: str = "relevance"
    ) -> SearchResult:
        params = {
            "search": query,
            "per_page": min(max_results, 200)
        }

        if self.email:
            params["mailto"] = self.email

        filters = []
        if year_from:
            filters.append(f"publication_year:>={year_from}")
        if year_to:
            filters.append(f"publication_year:<={year_to}")

        if filters:
            params["filter"] = ",".join(filters)

        sort_map = {
            "relevance": "relevance_score:desc",
            "cited_by_count": "cited_by_count:desc",
            "publication_date": "publication_date:desc"
        }
        params["sort"] = sort_map.get(sort, "relevance_score:desc")

        try:
            response = await self.client.get(f"{self.base_url}/works", params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                return SearchResult(papers=[], total=0, source="openalex", query=query)

            papers = []
            for work in data.get("results", []):
                papers.append(self._parse_work(work))

            return SearchResult(
                papers=papers,
                total=data.get("meta", {}).get("count", len(papers)),
                source="openalex",
                query=query
            )
        except httpx.HTTPError as e:
            raise Exception(f"OpenAlex API error: {str(e)}")

    async def get_paper(self, paper_id: str) -> Paper:
        if paper_id.startswith("https://doi.org/"):
            url = f"{self.base_url}/works/doi:{paper_id.replace('https://doi.org/', '')}"
        elif paper_id.startswith("W"):
            url = f"{self.base_url}/works/{paper_id}"
        else:
            url = f"{self.base_url}/works/doi:{paper_id}"

        params = {}
        if self.email:
            params["mailto"] = self.email

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            work = response.json()
            return self._parse_work(work)
        except httpx.HTTPError as e:
            raise Exception(f"OpenAlex API error: {str(e)}")

    async def get_citations(self, paper_id: str, max_results: int = 50) -> SearchResult:
        if not paper_id.startswith("W"):
            paper = await self.get_paper(paper_id)
            paper_id = paper.id

        params = {
            "filter": f"cites:{paper_id}",
            "per_page": min(max_results, 200),
            "sort": "cited_by_count:desc"
        }

        if self.email:
            params["mailto"] = self.email

        try:
            response = await self.client.get(f"{self.base_url}/works", params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                return SearchResult(papers=[], total=0, source="openalex", query=f"citations:{paper_id}")

            papers = []
            for work in data.get("results", []):
                papers.append(self._parse_work(work))

            return SearchResult(
                papers=papers,
                total=data.get("meta", {}).get("count", len(papers)),
                source="openalex",
                query=f"citations:{paper_id}"
            )
        except httpx.HTTPError as e:
            raise Exception(f"OpenAlex API error: {str(e)}")

    def _parse_work(self, work: dict) -> Paper:
        authors = []
        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            if author.get("display_name"):
                authors.append(author["display_name"])

        abstract = self._rebuild_abstract(work.get("abstract_inverted_index"))

        doi = work.get("doi")
        if doi and doi.startswith("https://doi.org/"):
            doi = doi.replace("https://doi.org/", "")

        pdf_url = None
        primary_location = work.get("primary_location") or {}
        if primary_location.get("pdf_url"):
            pdf_url = primary_location["pdf_url"]
        else:
            for location in work.get("locations", []):
                if location.get("pdf_url"):
                    pdf_url = location["pdf_url"]
                    break

        venue = None
        if primary_location and primary_location.get("source"):
            source = primary_location.get("source") or {}
            if source.get("display_name"):
                venue = source["display_name"]

        bibtex = self._generate_bibtex(work, authors, doi)

        return Paper(
            id=work.get("id", "").split("/")[-1],
            title=work.get("title", ""),
            authors=authors,
            year=work.get("publication_year"),
            citations=work.get("cited_by_count", 0),
            doi=doi,
            url=work.get("id"),
            pdf_url=pdf_url,
            abstract=abstract,
            venue=venue,
            bibtex=bibtex
        )

    def _rebuild_abstract(self, inverted_index: Optional[dict]) -> Optional[str]:
        if not inverted_index:
            return None

        words = []
        for word, positions in inverted_index.items():
            for pos in positions:
                words.append((pos, word))

        words.sort()
        return " ".join(word for _, word in words)

    def _generate_bibtex(self, work: dict, authors: list[str], doi: Optional[str]) -> str:
        work_id = work.get("id", "").split("/")[-1]
        title = work.get("title", "Untitled")
        year = work.get("publication_year", "n.d.")

        author_str = " and ".join(authors) if authors else "Unknown"

        venue = ""
        primary_location = work.get("primary_location") or {}
        if primary_location:
            source = primary_location.get("source") or {}
            venue = source.get("display_name", "")

        bibtex = f"@article{{{work_id},\n"
        bibtex += f"  title = {{{title}}},\n"
        bibtex += f"  author = {{{author_str}}},\n"
        bibtex += f"  year = {{{year}}},\n"
        if venue:
            bibtex += f"  journal = {{{venue}}},\n"
        if doi:
            bibtex += f"  doi = {{{doi}}},\n"
        bibtex += f"  note = {{Auto-generated from OpenAlex}}\n"
        bibtex += "}"

        return bibtex
