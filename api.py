from __future__ import annotations

from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import analysis
import db
import openalex

load_dotenv()
db.init_db()

DEFAULT_RESULT_LIMIT = openalex.DEFAULT_RESULT_LIMIT

app = FastAPI(title="etri-capstone reports API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/reports")
def get_reports() -> dict:
    return {"reports": db.list_reports()}


@app.get("/reports/{report_id}")
def get_report(report_id: int) -> dict:
    report = db.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail=f"리포트 {report_id}를 찾을 수 없습니다.")
    return report


@app.delete("/reports/{report_id}")
def delete_report(report_id: int) -> dict:
    deleted = db.delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"리포트 {report_id}를 찾을 수 없습니다.")
    return {"deleted": True}


@app.get("/search")
def search_papers(title: str, limit: int = DEFAULT_RESULT_LIMIT) -> dict:
    normalized_title, safe_limit = openalex.normalize_query(title, limit)
    if not normalized_title:
        raise HTTPException(status_code=400, detail="검색할 논문명을 입력해 주세요.")
    return openalex.search(normalized_title, safe_limit)


class Paper(BaseModel):
    title: str
    authors: list[str] = []
    publication_year: int | None = None
    doi: str | None = None
    landing_page_url: str | None = None
    openalex_id: str | None = None
    cited_by_count: int | None = None
    abstract: str | None = None


def _build_fallback_body(paper: Paper) -> str:
    lines = [
        "_ANTHROPIC_API_KEY가 설정되어 있지 않거나 분석 호출에 실패해, "
        "LLM 분석 대신 논문 메타데이터만 표시합니다._",
        "",
        "## 논문 정보",
        "",
    ]
    if paper.authors:
        lines.append(f"- 저자: {', '.join(paper.authors)}")
    if paper.publication_year:
        lines.append(f"- 발행연도: {paper.publication_year}")
    if paper.doi:
        lines.append(f"- DOI: {paper.doi}")
    if paper.landing_page_url:
        lines.append(f"- 원문: {paper.landing_page_url}")
    if paper.cited_by_count is not None:
        lines.append(f"- 인용수: {paper.cited_by_count}회 (OpenAlex 기준)")
    lines.append("")
    lines.append("## 초록")
    lines.append("")
    lines.append(paper.abstract if paper.abstract else "OpenAlex에서 초록을 제공하지 않는 논문입니다.")
    return "\n".join(lines) + "\n"


@app.post("/reports/from-paper")
def create_report_from_paper(paper: Paper) -> dict:
    """검색한 논문에 대해 Claude가 분석한 리포트를 생성해 저장한다.

    ANTHROPIC_API_KEY가 없거나 호출이 실패하면 메타데이터만 나열하는 stub으로 대체된다.
    """

    body_markdown = analysis.generate_report_body(
        paper.title, paper.authors, paper.abstract, paper.publication_year
    ) or _build_fallback_body(paper)
    paper_record = paper.model_dump(exclude={"abstract"})
    report_id = db.save_report(paper.title, body_markdown, [paper_record], source="auto")
    return {"report_id": report_id}
