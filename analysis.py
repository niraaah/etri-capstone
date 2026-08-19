from __future__ import annotations

import os

from anthropic import Anthropic

MODEL = "claude-sonnet-5"

PROMPT_TEMPLATE = """다음 논문을 분석해 한국어 리포트 본문을 Markdown으로 작성해줘.

제목: {title}
저자: {authors}
발행연도: {publication_year}
초록: {abstract}

아래 네 개 섹션을 ## 제목으로 구성해줘.
## 개요
## 핵심 방법론
## 주요 실험 결과
## 의의와 한계

각 섹션은 초록에서 확인 가능한 사실을 근거로 작성하고, 확인할 수 없는 수치나 사실은
지어내지 말고 일반적인 설명에 그쳐줘. 본문만 출력하고 다른 안내 문구는 붙이지 마."""


def generate_report_body(
    title: str,
    authors: list[str],
    abstract: str | None,
    publication_year: int | None,
) -> str | None:
    """Claude를 호출해 논문 분석 리포트 본문을 생성한다. 키가 없거나 호출에 실패하면 None을 반환한다."""

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    prompt = PROMPT_TEMPLATE.format(
        title=title,
        authors=", ".join(authors) if authors else "정보 없음",
        publication_year=publication_year or "정보 없음",
        abstract=abstract or "초록이 제공되지 않음",
    )

    try:
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except Exception:
        return None
