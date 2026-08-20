import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from persistent_memory_agent.agent import PersistentMemoryAgent
from persistent_memory_agent.models import MemoryWrite
from persistent_memory_agent.store import MemoryStore


class FakeModel:
    def extract_memory_writes(self, user_message):
        return [
            MemoryWrite(
                subject="user",
                predicate="meeting_time",
                value="after 10:00 local time",
                kind="preference",
                importance=0.9,
            )
        ]

    def generate_reply(self, user_message, memory_context):
        return f"Grounded with: {memory_context}"


class MemoryStoreTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = MemoryStore(os.path.join(self.temp_dir.name, "memory.db"))
        self.now = datetime(2026, 8, 20, tzinfo=timezone.utc)

    def tearDown(self):
        self.store.close()
        self.temp_dir.cleanup()

    def test_new_value_supersedes_old_value_without_deleting_history(self):
        first_event = self.store.record_event(
            "user",
            "I live in Seattle.",
            now=self.now,
        )
        first = self.store.set_memory(
            MemoryWrite("user", "home_city", "Seattle", "profile"),
            first_event,
            now=self.now,
        )
        second_event = self.store.record_event(
            "user",
            "I moved to San Francisco.",
            now=self.now,
        )
        second = self.store.set_memory(
            MemoryWrite("user", "home_city", "San Francisco", "profile"),
            second_event,
            now=self.now,
        )

        self.assertEqual(self.store.get_memory(first.id).status, "superseded")
        self.assertEqual(second.supersedes_id, first.id)
        self.assertEqual(
            [memory.value for memory in self.store.list_memories("active")],
            ["San Francisco"],
        )

    def test_retrieval_returns_relevant_active_memory(self):
        event = self.store.record_event(
            "user",
            "I am focused on persistent agent research.",
            now=self.now,
        )
        expected = self.store.set_memory(
            MemoryWrite(
                "user",
                "career_focus",
                "persistent agent memory research",
                "project",
                importance=1.0,
            ),
            event,
            now=self.now,
        )

        retrieved = self.store.retrieve(
            "persistent memory agent",
            now=self.now,
        )

        self.assertEqual(retrieved[0].memory.id, expected.id)
        self.assertGreater(retrieved[0].lexical_score, 0)

    def test_retrieval_accepts_naive_datetime_and_filters_unrelated_memory(self):
        event = self.store.record_event(
            "user",
            "My favorite color is blue.",
            now=self.now,
        )
        self.store.set_memory(
            MemoryWrite(
                "user",
                "favorite_color",
                "blue",
                "preference",
            ),
            event,
            now=self.now,
        )

        retrieved = self.store.retrieve(
            "database indexing",
            now=datetime(2026, 8, 20),
        )

        self.assertEqual(retrieved, [])

    def test_changed_confidence_creates_a_new_memory_version(self):
        first_event = self.store.record_event(
            "user",
            "I may prefer morning meetings.",
            now=self.now,
        )
        first = self.store.set_memory(
            MemoryWrite(
                "user",
                "meeting_time",
                "morning",
                "preference",
                confidence=0.6,
            ),
            first_event,
            now=self.now,
        )
        second_event = self.store.record_event(
            "user",
            "I definitely prefer morning meetings.",
            now=self.now,
        )
        second = self.store.set_memory(
            MemoryWrite(
                "user",
                "meeting_time",
                "morning",
                "preference",
                confidence=1.0,
            ),
            second_event,
            now=self.now,
        )

        self.assertNotEqual(first.id, second.id)
        self.assertEqual(second.supersedes_id, first.id)

    def test_context_respects_character_budget(self):
        event = self.store.record_event(
            "user",
            "I prefer meetings after 10am.",
            now=self.now,
        )
        self.store.set_memory(
            MemoryWrite(
                "user",
                "meeting_time",
                "after 10:00 local time",
                "preference",
            ),
            event,
            now=self.now,
        )

        context = self.store.build_context(
            "meeting time",
            max_chars=20,
            now=self.now,
        )

        self.assertEqual(context, "")

    def test_agent_records_events_and_applies_model_memory_writes(self):
        agent = PersistentMemoryAgent(self.store, FakeModel())

        turn = agent.handle_message("Please remember my meeting preference.")

        self.assertEqual(len(turn.written_memory_ids), 1)
        self.assertIn("meeting_time", turn.memory_context)
        self.assertEqual(
            [event["source"] for event in self.store.list_events()],
            ["user", "assistant"],
        )


if __name__ == "__main__":
    unittest.main()
