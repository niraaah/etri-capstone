from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

WORKS_URL = "https://api.openalex.org/works"

DEFAULT_RESULT_LIMIT = 5
MAX_RESULT_LIMIT = 10


def normalize_query(title: str, limit: int) -> tuple[str, int]:
    """제목 검색어를 다듬고 limit을 [1, MAX_RESULT_LIMIT] 범위로 clamp한다."""

    return title.strip(), max(1, min(limit, MAX_RESULT_LIMIT))


def _author_names(authorships: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for authorship in authorships:
        author = authorship.get("author") or {}
        name = author.get("display_name")
        if name:
            names.append(str(name))
    return names


def _reconstruct_abstract(inverted_index: dict[str, list[int]] | None) -> str | None:
    if not inverted_index:
        return None
    positions: dict[int, str] = {}
    for word, indices in inverted_index.items():
        for index in indices:
            positions[index] = word
    if not positions:
        return None
    return " ".join(positions[i] for i in range(max(positions) + 1) if i in positions)


def search(title: str, limit: int) -> dict[str, Any]:
    params = {
        "search": title,
        "per_page": limit,
        "select": (
            "id,display_name,publication_year,doi,authorships,primary_location,"
            "abstract_inverted_index,cited_by_count"
        ),
    }
    api_key = os.getenv("OPENALEX_API_KEY")
    if api_key:
        params["api_key"] = api_key

    request = Request(
        f"{WORKS_URL}?{urlencode(params)}",
        headers={"User-Agent": "etri-capstone/1.0"},
    )

    try:
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except HTTPError as error:
        return {
            "query": title,
            "error": f"OpenAlex가 HTTP {error.code} 응답을 반환했습니다.",
            "papers": [],
        }
    except URLError as error:
        return {
            "query": title,
            "error": f"OpenAlex에 연결하지 못했습니다: {error.reason}",
            "papers": [],
        }

    papers: list[dict[str, Any]] = []
    for work in payload.get("results", []):
        primary_location = work.get("primary_location") or {}
        papers.append(
            {
                "openalex_id": work.get("id"),
                "title": work.get("display_name"),
                "publication_year": work.get("publication_year"),
                "authors": _author_names(work.get("authorships") or []),
                "doi": work.get("doi"),
                "landing_page_url": primary_location.get("landing_page_url"),
                "cited_by_count": work.get("cited_by_count"),
                "abstract": _reconstruct_abstract(work.get("abstract_inverted_index")),
            }
        )

    return {
        "query": title,
        "count": len(papers),
        "papers": papers,
    }
