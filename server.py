from __future__ import annotations

from typing import Any

from dotenv import load_dotenv
from mcp.server import MCPServer

import db
import openalex

load_dotenv()
db.init_db()


DEFAULT_RESULT_LIMIT = openalex.DEFAULT_RESULT_LIMIT

server = MCPServer(
    name="openalex-paper-search",
    title="OpenAlex 논문 검색",
    description="논문명을 검색해 OpenAlex의 논문 정보를 반환합니다.",
)


@server.tool(structured_output=True)
def search_papers_by_title(
    title: str,
    limit: int = DEFAULT_RESULT_LIMIT,
) -> dict[str, Any]:
    """논문명을 검색어로 사용해 OpenAlex에서 관련 논문을 찾는다.

    Args:
        title: 찾고 싶은 논문의 이름 또는 제목에 포함된 검색어.
        limit: 반환할 논문 수. 기본값은 5이며 최대 10이다.
    """

    normalized_title, safe_limit = openalex.normalize_query(title, limit)
    if not normalized_title:
        return {
            "query": title,
            "error": "검색할 논문명을 입력해 주세요.",
            "papers": [],
        }

    return openalex.search(normalized_title, safe_limit)


@server.tool(structured_output=True)
def save_report(
    title: str,
    body_markdown: str,
    papers: list[dict[str, Any]],
) -> dict[str, Any]:
    """리포트를 근거 논문과 함께 저장한다.

    Args:
        title: 리포트 제목.
        body_markdown: 근거와 출처가 포함된 리포트 본문 (Markdown).
        papers: 참고한 논문 목록. search_papers_by_title이 반환하는 형식과 동일하게
            title, authors, doi, landing_page_url, openalex_id, cited_by_count를 포함한다.
    """

    report_id = db.save_report(title, body_markdown, papers)
    return {"report_id": report_id}


@server.tool(structured_output=True)
def list_reports() -> dict[str, Any]:
    """저장된 리포트 목록(제목, 저장 일시)을 반환한다."""

    return {"reports": db.list_reports()}


@server.tool(structured_output=True)
def get_report(report_id: int) -> dict[str, Any]:
    """저장된 리포트 하나를 본문과 참고 논문 목록까지 포함해 반환한다.

    Args:
        report_id: 조회할 리포트의 id.
    """

    report = db.get_report(report_id)
    if report is None:
        return {"error": f"리포트 {report_id}를 찾을 수 없습니다."}
    return report


@server.tool(structured_output=True)
def delete_report(report_id: int) -> dict[str, Any]:
    """저장된 리포트를 삭제한다.

    Args:
        report_id: 삭제할 리포트의 id.
    """

    deleted = db.delete_report(report_id)
    return {"deleted": deleted}


if __name__ == "__main__":
    server.run(transport="stdio")
