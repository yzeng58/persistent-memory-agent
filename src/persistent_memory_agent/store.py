import json
import math
import os
import re
import sqlite3
from datetime import datetime, timezone

from persistent_memory_agent.models import (
    MEMORY_KINDS,
    Memory,
    MemoryWrite,
    RetrievedMemory,
)

_TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")
_TOKEN_ALIASES = {
    "agents": "agent",
    "calls": "meeting",
    "conversation": "meeting",
    "conversations": "meeting",
    "opportunities": "career",
    "opportunity": "career",
    "researcher": "research",
    "researchers": "research",
    "roles": "career",
    "role": "career",
    "schedule": "meeting",
    "scheduling": "meeting",
}
_STOPWORDS = frozenset(
    {
        "a",
        "about",
        "an",
        "and",
        "for",
        "i",
        "in",
        "my",
        "of",
        "the",
        "to",
        "with",
    }
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _as_timestamp(value: datetime) -> str:
    return _normalize_datetime(value).isoformat()


def _tokens(text: str) -> set[str]:
    raw_tokens = _TOKEN_PATTERN.findall(text.lower().replace("_", " "))
    return {
        _TOKEN_ALIASES.get(token, token)
        for token in raw_tokens
        if token not in _STOPWORDS
    }


class MemoryStore:
    """Canonical SQLite owner for events, memory versions, and retrieval."""

    def __init__(self, database_path: str):
        self.database_path = os.path.expanduser(database_path)
        parent = os.path.dirname(self.database_path)
        if self.database_path != ":memory:" and parent:
            os.makedirs(parent, exist_ok=True)
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "MemoryStore":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def _initialize_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                predicate TEXT NOT NULL,
                value TEXT NOT NULL,
                kind TEXT NOT NULL,
                importance REAL NOT NULL,
                confidence REAL NOT NULL,
                source_event_id INTEGER NOT NULL REFERENCES events(id),
                supersedes_id INTEGER REFERENCES memories(id),
                status TEXT NOT NULL CHECK (status IN ('active', 'superseded')),
                valid_from TEXT NOT NULL,
                valid_to TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS memories_active_key
                ON memories(subject, predicate, kind, status);
            CREATE INDEX IF NOT EXISTS memories_status
                ON memories(status, valid_from, valid_to);
            CREATE UNIQUE INDEX IF NOT EXISTS memories_one_active_key
                ON memories(subject, predicate, kind)
                WHERE status = 'active';
            """
        )

    def record_event(
        self,
        source: str,
        content: str,
        metadata: dict[str, object] | None = None,
        now: datetime | None = None,
    ) -> int:
        """Append one immutable observation and return its event ID."""
        source = source.strip()
        content = content.strip()
        if not source or not content:
            raise ValueError("source and content must be non-empty")
        timestamp = _as_timestamp(now or _utc_now())
        cursor = self.connection.execute(
            """
            INSERT INTO events(source, content, metadata_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (source, content, json.dumps(metadata or {}, sort_keys=True), timestamp),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def set_memory(
        self,
        write: MemoryWrite,
        source_event_id: int,
        now: datetime | None = None,
    ) -> Memory:
        """Set the active value for one memory key while preserving old versions."""
        self._validate_write(write)
        timestamp = _as_timestamp(now or _utc_now())
        active_row = self.connection.execute(
            """
            SELECT *
            FROM memories
            WHERE subject = ? AND predicate = ? AND kind = ? AND status = 'active'
            ORDER BY id DESC
            LIMIT 1
            """,
            (write.subject.strip(), write.predicate.strip(), write.kind),
        ).fetchone()

        if (
            active_row is not None
            and active_row["value"] == write.value.strip()
            and float(active_row["importance"]) == write.importance
            and float(active_row["confidence"]) == write.confidence
        ):
            return self._row_to_memory(active_row)

        supersedes_id = None
        with self.connection:
            if active_row is not None:
                supersedes_id = int(active_row["id"])
                self.connection.execute(
                    """
                    UPDATE memories
                    SET status = 'superseded', valid_to = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (timestamp, timestamp, supersedes_id),
                )

            cursor = self.connection.execute(
                """
                INSERT INTO memories(
                    subject,
                    predicate,
                    value,
                    kind,
                    importance,
                    confidence,
                    source_event_id,
                    supersedes_id,
                    status,
                    valid_from,
                    valid_to,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, NULL, ?, ?)
                """,
                (
                    write.subject.strip(),
                    write.predicate.strip(),
                    write.value.strip(),
                    write.kind,
                    write.importance,
                    write.confidence,
                    source_event_id,
                    supersedes_id,
                    timestamp,
                    timestamp,
                    timestamp,
                ),
            )

        return self.get_memory(int(cursor.lastrowid))

    def get_memory(self, memory_id: int) -> Memory:
        """Return one memory version by ID."""
        row = self.connection.execute(
            "SELECT * FROM memories WHERE id = ?",
            (memory_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"memory {memory_id} does not exist")
        return self._row_to_memory(row)

    def list_memories(self, status: str | None = None) -> list[Memory]:
        """List memory versions in creation order, optionally filtered by status."""
        if status is not None and status not in {"active", "superseded"}:
            raise ValueError("status must be active, superseded, or None")
        if status is None:
            rows = self.connection.execute(
                "SELECT * FROM memories ORDER BY id"
            ).fetchall()
        else:
            rows = self.connection.execute(
                "SELECT * FROM memories WHERE status = ? ORDER BY id",
                (status,),
            ).fetchall()
        return [self._row_to_memory(row) for row in rows]

    def retrieve(
        self,
        query: str,
        limit: int = 8,
        now: datetime | None = None,
    ) -> list[RetrievedMemory]:
        """Rank active, temporally valid memories for a query."""
        if limit < 1:
            raise ValueError("limit must be positive")
        query_tokens = _tokens(query)
        current_time = _normalize_datetime(now or _utc_now())
        timestamp = _as_timestamp(current_time)
        rows = self.connection.execute(
            """
            SELECT *
            FROM memories
            WHERE status = 'active'
              AND valid_from <= ?
              AND (valid_to IS NULL OR valid_to > ?)
            """,
            (timestamp, timestamp),
        ).fetchall()

        ranked = [
            self._score_memory(self._row_to_memory(row), query_tokens, current_time)
            for row in rows
        ]
        if query_tokens:
            ranked = [item for item in ranked if item.lexical_score > 0]
        ranked.sort(key=lambda item: (item.score, item.memory.id), reverse=True)
        return ranked[:limit]

    def build_context(
        self,
        query: str,
        max_chars: int = 2_000,
        now: datetime | None = None,
    ) -> str:
        """Pack ranked memories into a bounded, provenance-bearing context block."""
        if max_chars < 1:
            raise ValueError("max_chars must be positive")
        lines: list[str] = []
        current_length = 0
        for item in self.retrieve(query, now=now):
            memory = item.memory
            line = (
                f"[{memory.kind}] {memory.subject}.{memory.predicate} = "
                f"{memory.value} (source event {memory.source_event_id}, "
                f"confidence {memory.confidence:.2f})"
            )
            added_length = len(line) + (1 if lines else 0)
            if current_length + added_length > max_chars:
                break
            lines.append(line)
            current_length += added_length
        return "\n".join(lines)

    def list_events(self) -> list[dict[str, object]]:
        """Return the immutable event log in chronological order."""
        rows = self.connection.execute(
            "SELECT * FROM events ORDER BY id"
        ).fetchall()
        return [
            {
                "id": int(row["id"]),
                "source": row["source"],
                "content": row["content"],
                "metadata": json.loads(row["metadata_json"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def _score_memory(
        self,
        memory: Memory,
        query_tokens: set[str],
        now: datetime,
    ) -> RetrievedMemory:
        memory_tokens = _tokens(
            f"{memory.subject} {memory.predicate} {memory.value} {memory.kind}"
        )
        lexical_score = (
            len(query_tokens & memory_tokens) / len(query_tokens)
            if query_tokens
            else 0.0
        )
        updated_at = datetime.fromisoformat(memory.updated_at)
        age_days = max((now - updated_at).total_seconds() / 86_400, 0.0)
        recency_score = math.exp(-age_days / 30.0)
        score = (
            0.55 * lexical_score
            + 0.20 * memory.importance
            + 0.15 * memory.confidence
            + 0.10 * recency_score
        )
        return RetrievedMemory(
            memory=memory,
            score=score,
            lexical_score=lexical_score,
            recency_score=recency_score,
        )

    @staticmethod
    def _validate_write(write: MemoryWrite) -> None:
        if write.kind not in MEMORY_KINDS:
            raise ValueError(f"unsupported memory kind: {write.kind}")
        if not write.subject.strip() or not write.predicate.strip():
            raise ValueError("subject and predicate must be non-empty")
        if not write.value.strip():
            raise ValueError("value must be non-empty")
        if not 0.0 <= write.importance <= 1.0:
            raise ValueError("importance must be between 0 and 1")
        if not 0.0 <= write.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    @staticmethod
    def _row_to_memory(row: sqlite3.Row) -> Memory:
        return Memory(
            id=int(row["id"]),
            subject=row["subject"],
            predicate=row["predicate"],
            value=row["value"],
            kind=row["kind"],
            importance=float(row["importance"]),
            confidence=float(row["confidence"]),
            source_event_id=int(row["source_event_id"]),
            supersedes_id=(
                int(row["supersedes_id"])
                if row["supersedes_id"] is not None
                else None
            ),
            status=row["status"],
            valid_from=row["valid_from"],
            valid_to=row["valid_to"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
