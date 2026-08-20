from dataclasses import dataclass
from typing import Protocol, Sequence

from persistent_memory_agent.models import MemoryWrite
from persistent_memory_agent.store import MemoryStore


class AgentModel(Protocol):
    """Model behavior required by the persistent-memory orchestration loop."""

    def extract_memory_writes(self, user_message: str) -> Sequence[MemoryWrite]:
        """Return only durable facts explicitly supported by the user message."""

    def generate_reply(self, user_message: str, memory_context: str) -> str:
        """Generate a reply grounded in the retrieved memory context."""


@dataclass(frozen=True)
class AgentTurn:
    reply: str
    memory_context: str
    written_memory_ids: tuple[int, ...]


class PersistentMemoryAgent:
    """Record, consolidate, retrieve, and use memory for one conversation turn."""

    def __init__(self, store: MemoryStore, model: AgentModel):
        self.store = store
        self.model = model

    def handle_message(self, user_message: str) -> AgentTurn:
        """Process one user message and return the grounded agent turn."""
        user_message = user_message.strip()
        if not user_message:
            raise ValueError("user_message must be non-empty")

        event_id = self.store.record_event("user", user_message)
        written_memories = [
            self.store.set_memory(write, source_event_id=event_id)
            for write in self.model.extract_memory_writes(user_message)
        ]
        memory_context = self.store.build_context(user_message)
        reply = self.model.generate_reply(user_message, memory_context).strip()
        if not reply:
            raise ValueError("model returned an empty reply")
        self.store.record_event(
            "assistant",
            reply,
            metadata={"written_memory_ids": [item.id for item in written_memories]},
        )
        return AgentTurn(
            reply=reply,
            memory_context=memory_context,
            written_memory_ids=tuple(item.id for item in written_memories),
        )
