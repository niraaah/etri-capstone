import { useState } from "react";

export default function ConfirmDeleteButton({ onConfirm, label = "삭제", className = "" }) {
  const [confirming, setConfirming] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState(null);

  async function handleConfirm(event) {
    event.stopPropagation();
    event.preventDefault();
    setDeleting(true);
    setError(null);
    try {
      await onConfirm();
    } catch (err) {
      setError(err.message || "삭제하지 못했습니다.");
      setDeleting(false);
    }
  }

  function handleCancel(event) {
    event.stopPropagation();
    setConfirming(false);
    setError(null);
  }

  if (confirming) {
    return (
      <span className={`confirm-delete ${className}`} onClick={(event) => event.stopPropagation()}>
        <span className={`confirm-delete-label${error ? " confirm-delete-error" : ""}`}>
          {error || "정말 삭제할까요?"}
        </span>
        <button type="button" className="btn btn-danger" onClick={handleConfirm} disabled={deleting}>
          {deleting ? "삭제 중..." : "삭제"}
        </button>
        <button type="button" className="btn btn-ghost" onClick={handleCancel} disabled={deleting}>
          취소
        </button>
      </span>
    );
  }

  return (
    <button
      type="button"
      className={`btn btn-ghost btn-danger-text ${className}`}
      onClick={(event) => {
        event.stopPropagation();
        event.preventDefault();
        setConfirming(true);
      }}
    >
      {label}
    </button>
  );
}
