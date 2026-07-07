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
