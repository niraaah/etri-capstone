# SPEC: 저장된 리포트 목록·상세 조회 (React 프론트엔드)

## Context

`etri-capstone`은 OpenAlex 기반 연구 지원 MCP 서버 프로젝트다. 현재 `server.py`에는 논문 검색 Tool(`search_papers_by_title`)만 있고, 리포트 저장/조회/삭제 기능과 SQLite 저장소는 없다. React 프론트엔드는 MCP(stdio)에 직접 접근할 수 없으므로 별도의 HTTP API가 필요하다.

## Goal

연구자가 MCP 서버(Claude Desktop 등 MCP Host)를 통해 작성·저장한 리포트를, 브라우저(`localhost:3000`)에서 목록으로 확인하고 클릭해 상세 내용(본문 + 참고 논문)을 읽을 수 있게 한다.

## Non-goals

- React UI에서 리포트 본문을 자유롭게 직접 작성/수정하는 화면 (수동 작성은 MCP Tool을 통해서만; UI에서는 검색한 논문을 저장하면 자동 생성되는 리포트만 가능)
- 인증/권한 관리
- 배포(로컬 실행만 목표)

> 업데이트: 최초 스펙에서는 "React UI에 삭제 버튼 없음"과 "React UI에서 리포트 작성 없음"이 non-goal이었으나, 이후 요청으로 목록/상세 페이지에 삭제 버튼을, `/search` 페이지에 "검색 → 저장 시 자동 리포트 생성" 흐름을 추가했다.

## User Flow

1. (사전) Claude Desktop 등에서 논문 검색 → 리포트 작성 후 `save_report` Tool 호출로 저장
2. 사용자가 브라우저에서 `localhost:3000/reports` 접속 → 저장된 리포트 목록(제목, 저장일) 표시
3. 목록에서 리포트 클릭 → `/reports/:id`로 이동 → 본문(Markdown 렌더링)과 참고 논문 목록(제목/저자/DOI/링크) 표시

## Functional Requirements

### MCP Tools 추가 (`server.py`)

- `save_report(title, body_markdown, papers)` → 리포트와 참고 논문을 SQLite에 저장, `report_id` 반환
- `list_reports()` → 저장된 리포트 목록(id, title, created_at) 반환
- `get_report(report_id)` → 리포트 상세(본문 + 참고 논문 목록) 반환
- `delete_report(report_id)` → 리포트 삭제

### HTTP API 서버 신규 추가

FastAPI, MCP stdio 서버와 별개 프로세스, 포트 `8002`(로컬 환경에서 `8000`·`8001` 모두 종료해도 살아있는 유령 리스너와 충돌해 `8002`로 변경. `--reload` 옵션도 이 환경에서 재시작이 잘 반영되지 않아 제거하고, 백엔드 코드를 고칠 때는 수동으로 재시작한다), SQLite 파일 공유.

- `GET /reports` → 목록
- `GET /reports/{id}` → 상세
- `DELETE /reports/{id}` → 삭제
- `GET /search?title=&limit=` → OpenAlex 논문 검색 (`openalex.py` 공용 모듈, 초록 포함)
- `POST /reports/from-paper` → 논문 1건을 받아 제목/저자/연도/DOI/초록으로 리포트 본문을 자동 생성해 저장
- CORS: `http://localhost:3000` 허용

### React 프론트엔드

Vite + React + `react-router-dom`, `localhost:3000`.

- `/reports`: 목록 페이지 (카드/리스트 레이아웃, 호버 효과, 삭제 버튼, 로딩/에러 상태 표시)
- `/reports/:id`: 상세 페이지 (제목, 본문 Markdown 렌더링, 참고 논문 목록, 삭제 버튼)
- `/search`: 논문 검색 페이지 (OpenAlex 검색, 결과별 "리포트로 저장" 버튼 → 저장 시 자동으로 리포트가 생성되고 상세 페이지로 이동)

### 시드 스크립트

실제 검색 결과 기반 샘플 리포트를 SQLite에 직접 삽입하는 1회성 스크립트(`seed.py`). Transformer·SimCLR·SHAP·ResNet·BERT·GAN·Adam·AlexNet·OpenAlex 총 9개를 기본 시드로 포함하며, 이후 `/search` 페이지에서 검색→저장한 리포트(예: Word2Vec)가 추가로 쌓인다.

BERT는 `search_papers_by_title`로 검색해도 원 논문이 전혀 나오지 않았는데, DOI(`10.18653/v1/N19-1423`)로 직접 조회한 결과 OpenAlex의 해당 레코드(`W2963341956`)가 `title`/`display_name` 필드 자체가 빈 문자열이어서 텍스트 검색으로는 원천적으로 찾을 수 없는 것으로 확인됐다(OpenAlex 쪽 데이터 결측치, 저희 쪽 버그 아님). Transformer·GAN·AlexNet은 검색 1순위 결과의 연도/DOI가 실제 값과 달라, openalex_id·저자는 검색 결과를 유지하고 연도·DOI만 실제 값으로 수동 보정했다.

## Persistence

SQLite, 파일: `etri-capstone/reports.db` (이미 `.gitignore`에 포함됨)

```
reports(id INTEGER PK, title TEXT, body_markdown TEXT, created_at TEXT, source TEXT DEFAULT 'manual')
report_papers(id INTEGER PK, report_id INTEGER FK, title TEXT, authors TEXT(JSON), doi TEXT, landing_page_url TEXT, openalex_id TEXT, cited_by_count INTEGER)
```

`source`는 `manual`(MCP save_report Tool을 통한 LLM 분석 리포트) 또는 `auto`(`/search` 페이지에서 "리포트로 저장" 클릭 시 생성되는 메타데이터 stub)이다.

## Error Behavior

- 존재하지 않는 `report_id` 조회/삭제 시 API는 404 반환, React는 에러 메시지 표시
- API 서버 연결 실패 시 React 목록/상세 페이지에 에러 상태 표시 (빈 화면 대신)

## Completion Criteria

- 시드 스크립트 실행 후 `localhost:3000/reports`에서 샘플 리포트 3개 목록이 보인다
- 목록의 리포트를 클릭하면 상세 페이지로 이동해 본문과 참고 논문이 보인다
- FastAPI 서버(`localhost:8002`)와 React 개발 서버(`localhost:3000`)를 각각 실행해 위 흐름이 동작함을 확인한다

## Constraints

- React는 기본기 위주로 구현하되 목록/상세 화면은 기본 스타일 이상(호버, 로딩/에러 상태)으로 다듬는다
- 기존 `search_papers_by_title` Tool과 `.env`/`OPENALEX_API_KEY` 설정은 변경하지 않는다

## Assumptions

- React 프로젝트는 Vite로 새로 생성한다 (CRA는 React 팀에서 더 이상 권장하지 않음)
- API 서버는 포트 `8002`를 사용한다
- `papers`는 프론트에서 별도 편집 없이 저장 시점의 스냅샷으로 취급한다 (OpenAlex 재조회 안 함)

## Open Risks

- FastAPI, uvicorn 등 새 패키지가 `requirements.txt`에 추가로 필요함
- SQLite 파일에 두 프로세스(MCP 서버, API 서버)가 동시 접근 시 락 이슈 가능성은 낮지만 완전히 배제되진 않음 (단일 사용자 로컬 환경이므로 실습 범위에서는 문제 없을 것으로 가정)
