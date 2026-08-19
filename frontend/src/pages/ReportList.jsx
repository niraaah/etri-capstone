import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { deleteReport, fetchReports } from "../api";
import ConfirmDeleteButton from "../ConfirmDeleteButton";

function formatDate(isoString) {
  return new Date(isoString).toLocaleString("ko-KR", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export default function ReportList() {
  const [reports, setReports] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReports()
      .then((data) => setReports(data.reports))
      .catch((err) => setError(err.message));
  }, []);

  async function handleDelete(reportId) {
    await deleteReport(reportId);
    setReports((current) => current.filter((report) => report.id !== reportId));
  }

  if (error) {
    return (
      <div className="page">
        <div className="state-banner state-error">
          <strong>리포트 목록을 불러오지 못했습니다.</strong>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (reports === null) {
    return (
      <div className="page">
        <div className="state-banner">
          <span className="spinner" aria-hidden="true" />
          불러오는 중...
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-heading">
        <h1>저장된 리포트</h1>
        <p className="page-subtitle">
          {reports.length > 0 ? (
            <>
              총 <span className="count-accent">{reports.length}개</span>의 리포트가 저장되어
              있습니다.
            </>
          ) : (
            "MCP 서버에서 작성한 리포트가 이 곳에 모입니다."
          )}
        </p>
      </div>

      {reports.length === 0 ? (
        <div className="empty-state">
          <span className="empty-state-mark" aria-hidden="true">
            🔍
          </span>
          <p>저장된 리포트가 아직 없습니다.</p>
          <Link to="/search" className="btn btn-primary">
            논문 검색하고 첫 리포트 만들기
          </Link>
        </div>
      ) : (
        <ul className="report-list">
          {reports.map((report, index) => (
            <li
              key={report.id}
              className="fade-in-up"
              style={{ animationDelay: `${Math.min(index, 6) * 40}ms` }}
            >
              <Link to={`/reports/${report.id}`} className="report-card">
                <div className="report-card-main">
                  <span className="report-card-title" title={report.title}>
                    {report.title}
                  </span>
                  <span className="report-card-date">{formatDate(report.created_at)}</span>
                </div>
                <div className="report-card-actions">
                  <ConfirmDeleteButton onConfirm={() => handleDelete(report.id)} />
                  <span className="report-card-arrow" aria-hidden="true">
                    →
                  </span>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
