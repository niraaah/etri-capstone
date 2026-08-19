from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent / "reports.db"


def _decode_authors(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw.split(", ")


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with closing(_connect()) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body_markdown TEXT NOT NULL,
                created_at TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT 'manual'
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS report_papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                authors TEXT,
                doi TEXT,
                landing_page_url TEXT,
                openalex_id TEXT,
                cited_by_count INTEGER
            )
            """
        )


def save_report(
    title: str,
    body_markdown: str,
    papers: list[dict[str, Any]],
    source: str = "manual",
) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    with closing(_connect()) as connection, connection:
        cursor = connection.execute(
            "INSERT INTO reports (title, body_markdown, created_at, source) VALUES (?, ?, ?, ?)",
            (title, body_markdown, created_at, source),
        )
        report_id = cursor.lastrowid
        for paper in papers:
            connection.execute(
                """
                INSERT INTO report_papers
                    (report_id, title, authors, doi, landing_page_url, openalex_id, cited_by_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report_id,
                    paper.get("title"),
                    json.dumps(paper.get("authors") or []),
                    paper.get("doi"),
                    paper.get("landing_page_url"),
                    paper.get("openalex_id"),
                    paper.get("cited_by_count"),
                ),
            )
    return report_id


def list_reports() -> list[dict[str, Any]]:
    with closing(_connect()) as connection, connection:
        rows = connection.execute(
            "SELECT id, title, created_at, source FROM reports ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_report(report_id: int) -> dict[str, Any] | None:
    with closing(_connect()) as connection, connection:
        report_row = connection.execute(
            "SELECT id, title, body_markdown, created_at, source FROM reports WHERE id = ?",
            (report_id,),
        ).fetchone()
        if report_row is None:
            return None
        paper_rows = connection.execute(
            """
            SELECT title, authors, doi, landing_page_url, openalex_id, cited_by_count
            FROM report_papers WHERE report_id = ?
            """,
            (report_id,),
        ).fetchall()

    report = dict(report_row)
    report["papers"] = [
        {
            "title": row["title"],
            "authors": _decode_authors(row["authors"]),
            "doi": row["doi"],
            "landing_page_url": row["landing_page_url"],
            "openalex_id": row["openalex_id"],
            "cited_by_count": row["cited_by_count"],
        }
        for row in paper_rows
    ]
    return report


def delete_report(report_id: int) -> bool:
    with closing(_connect()) as connection, connection:
        cursor = connection.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    return cursor.rowcount > 0
