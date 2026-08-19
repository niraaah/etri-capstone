const API_BASE = "http://localhost:8002";

async function request(path, options) {
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, options);
  } catch {
    throw new Error("서버에 연결하지 못했습니다. API 서버가 실행 중인지 확인해 주세요.");
  }

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = typeof body.detail === "string" ? body.detail : null;
    throw new Error(detail || `요청이 실패했습니다 (HTTP ${response.status})`);
  }

  try {
    return await response.json();
  } catch {
    throw new Error("서버 응답을 해석하지 못했습니다.");
  }
}

export function fetchReports() {
  return request("/reports");
}

export function fetchReport(reportId) {
  return request(`/reports/${reportId}`);
}

export function deleteReport(reportId) {
  return request(`/reports/${reportId}`, { method: "DELETE" });
}

export function searchPapers(title, limit = 5) {
  return request(`/search?${new URLSearchParams({ title, limit })}`);
}

export function createReportFromPaper(paper) {
  return request("/reports/from-paper", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(paper),
  });
}
