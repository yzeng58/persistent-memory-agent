from dataclasses import dataclass
from typing import Literal

MemoryKind = Literal[
    "profile",
    "preference",
    "project",
    "relationship",
    "commitment",
    "procedure",
]

MEMORY_KINDS = frozenset(
    {
        "profile",
        "preference",
        "project",
        "relationship",
        "commitment",
        "procedure",
    }
)


@dataclass(frozen=True)
class MemoryWrite:
    """A model-proposed durable fact with an explicit stable key."""

    subject: str
    predicate: str
    value: str
    kind: MemoryKind
    importance: float = 0.5
    confidence: float = 1.0


@dataclass(frozen=True)
class Memory:
    """One version of a durable memory, including its provenance and status."""

    id: int
    subject: str
    predicate: str
    value: str
    kind: MemoryKind
    importance: float
    confidence: float
    source_event_id: int
    supersedes_id: int | None
    status: str
    valid_from: str
    valid_to: str | None
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class RetrievedMemory:
    """A memory selected for the current context, with inspectable scores."""

    memory: Memory
    score: float
    lexical_score: float
    recency_score: float
