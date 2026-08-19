import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { deleteReport, fetchReport } from "../api";
import ConfirmDeleteButton from "../ConfirmDeleteButton";

function formatDate(isoString) {
  return new Date(isoString).toLocaleString("ko-KR", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export default function ReportDetail() {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setReport(null);
    setError(null);
    fetchReport(reportId)
      .then(setReport)
      .catch((err) => setError(err.message));
  }, [reportId]);

  async function handleDelete() {
    await deleteReport(reportId);
    navigate("/reports");
  }

  return (
    <div className="page">
      <Link to="/reports" className="back-link">
        ← 목록으로
      </Link>

      {error && (
        <div className="state-banner state-error">
          <strong>리포트를 불러오지 못했습니다.</strong>
          <p>{error}</p>
        </div>
      )}

      {!error && report === null && (
        <div className="state-banner">
          <span className="spinner" aria-hidden="true" />
          불러오는 중...
        </div>
      )}

      {report && (
        <>
          <div className="detail-heading">
            <div>
              <h1>{report.title}</h1>
              <p className="report-date">{formatDate(report.created_at)}</p>
            </div>
            <ConfirmDeleteButton label="리포트 삭제" onConfirm={handleDelete} />
          </div>

          <div className="report-body">
            <ReactMarkdown>{report.body_markdown}</ReactMarkdown>
          </div>

          <h2>참고 논문</h2>
          <ul className="paper-list">
            {report.papers.map((paper, index) => (
              <li key={index} className="paper-card">
                <div className="paper-title">{paper.title}</div>
                <div className="paper-meta">
                  <span className="paper-authors">{paper.authors.join(", ")}</span>
                  {typeof paper.cited_by_count === "number" && (
                    <span className="citation-badge" title="OpenAlex 기준 인용수">
                      인용 {paper.cited_by_count.toLocaleString("ko-KR")}회
                    </span>
                  )}
                </div>
                <div className="paper-links">
                  {paper.doi && (
                    <a
                      href={paper.doi}
                      target="_blank"
                      rel="noreferrer"
                      className="pill-link"
                    >
                      DOI ↗
                    </a>
                  )}
                  {paper.landing_page_url && (
                    <a
                      href={paper.landing_page_url}
                      target="_blank"
                      rel="noreferrer"
                      className="pill-link"
                    >
                      원문 보기 ↗
                    </a>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
