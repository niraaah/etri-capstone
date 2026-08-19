import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createReportFromPaper, searchPapers } from "../api";

const EXAMPLE_QUERIES = [
  "Attention Is All You Need",
  "Deep Residual Learning for Image Recognition",
  "Generative Adversarial Networks",
  "A Method for Stochastic Optimization",
];

export default function SearchPapers() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [papers, setPapers] = useState(null);
  const [error, setError] = useState(null);
  const [searching, setSearching] = useState(false);
  const [savingKey, setSavingKey] = useState(null);

  async function runSearch(rawTitle) {
    const title = rawTitle.trim();
    if (!title) {
      setError("검색할 논문명을 입력해 주세요.");
      setPapers(null);
      return;
    }

    setSearching(true);
    setError(null);
    setPapers(null);
    try {
      const data = await searchPapers(title, 8);
      setPapers(data.papers);
    } catch (err) {
      setError(err.message);
    } finally {
      setSearching(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    runSearch(query);
  }

  function handleExampleClick(example) {
    setQuery(example);
    runSearch(example);
  }

  async function handleSave(paper) {
    const key = paper.openalex_id || paper.title;
    setSavingKey(key);
    try {
      const { report_id } = await createReportFromPaper(paper);
      navigate(`/reports/${report_id}`);
    } catch (err) {
      setError(err.message);
      setSavingKey(null);
    }
  }

  return (
    <div className="page">
      <div className="search-hero">
        <h1>오늘은 어떤 논문을 살펴볼까요?</h1>
        <p className="page-subtitle">
          OpenAlex에서 논문을 검색하고, 저장하면 리포트가 자동으로 만들어집니다.
        </p>

        <form className="search-form" onSubmit={handleSubmit}>
          <span className="search-input-icon" aria-hidden="true">
            🔍
          </span>
          <input
            type="text"
            className="search-input"
            placeholder="논문 제목을 입력하세요 (예: Attention Is All You Need)"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <button type="submit" className="btn btn-primary" disabled={searching}>
            {searching ? "검색 중..." : "검색"}
          </button>
        </form>

        <div className="example-chips">
          {EXAMPLE_QUERIES.map((example) => (
            <button
              key={example}
              type="button"
              className="chip"
              onClick={() => handleExampleClick(example)}
              disabled={searching}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="state-banner state-error">
          <strong>오류가 발생했습니다.</strong>
          <p>{error}</p>
        </div>
      )}

      {searching && (
        <div className="state-banner">
          <span className="spinner" aria-hidden="true" />
          검색 중...
        </div>
      )}

      {!searching && papers !== null && papers.length === 0 && (
        <div className="state-banner">검색 결과가 없습니다.</div>
      )}

      {papers && papers.length > 0 && (
        <ul className="paper-list">
          {papers.map((paper, index) => {
            const key = paper.openalex_id || paper.title;
            return (
              <li
                key={key}
                className="paper-card fade-in-up"
                style={{ animationDelay: `${Math.min(index, 6) * 40}ms` }}
              >
                <div className="paper-title">{paper.title || "(제목 없음)"}</div>
                <div className="paper-meta">
                  <span className="paper-authors">
                    {paper.authors.join(", ")}
                    {paper.publication_year ? ` · ${paper.publication_year}` : ""}
                  </span>
                  {typeof paper.cited_by_count === "number" && (
                    <span className="citation-badge" title="OpenAlex 기준 인용수">
                      인용 {paper.cited_by_count.toLocaleString("ko-KR")}회
                    </span>
                  )}
                </div>
                {paper.abstract && <p className="paper-abstract">{paper.abstract}</p>}
                <div className="paper-links">
                  {paper.doi && (
                    <a href={paper.doi} target="_blank" rel="noreferrer" className="pill-link">
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
                  <button
                    type="button"
                    className="btn btn-primary"
                    disabled={savingKey === key}
                    onClick={() => handleSave(paper)}
                  >
                    {savingKey === key ? "저장 중..." : "리포트로 저장"}
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
