# 리서치 리포트 프론트엔드

저장된 리포트를 목록·상세로 조회하고, OpenAlex에서 논문을 검색해 리포트를 생성하는 React 화면이다. 백엔드 API는 [`../api.py`](../api.py) FastAPI 서버가 제공한다.

## 준비

Node.js가 필요하다.

```bash
node --version
```

## 실행

먼저 저장소 루트에서 API 서버를 띄운다 (`localhost:8002`).

```bash
# 저장소 루트에서
.\.venv\Scripts\python.exe -m uvicorn api:app --port 8002
```

그 다음 이 폴더에서 프론트엔드를 실행한다 (`localhost:3000`).

```bash
npm install
npm run dev
```

API 서버가 실행 중이 아니면 화면에 연결 실패 에러가 표시된다.

## 화면 구성

- `/search`: OpenAlex 논문 검색. 검색 결과에서 "리포트로 저장"을 누르면 Claude(Anthropic API)가 분석한 리포트가 생성된다. `ANTHROPIC_API_KEY`가 없거나 호출에 실패하면 논문 메타데이터만 나열하는 리포트로 대체된다.
- `/reports`: 저장된 리포트 목록.
- `/reports/:id`: 리포트 상세(본문, 참고 논문, 삭제).

## API 주소 변경

`src/api.js`의 `API_BASE` 상수가 API 서버 주소(`http://localhost:8002`)를 가리킨다. 포트를 바꿔 실행했다면 이 값도 함께 바꿔야 한다.
