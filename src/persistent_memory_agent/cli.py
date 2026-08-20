import argparse
import os

from persistent_memory_agent.agent import PersistentMemoryAgent
from persistent_memory_agent.models import MemoryWrite
from persistent_memory_agent.openai_model import OpenAIResponsesModel
from persistent_memory_agent.store import MemoryStore

DEFAULT_DATABASE = "~/.persistent-memory-agent/memory.db"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Persistent personal memory for tool-using agents."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser(
        "demo",
        help="Run a deterministic synthetic memory lifecycle.",
    )
    demo_parser.add_argument("--db", default=":memory:")

    chat_parser = subparsers.add_parser(
        "chat",
        help="Start an interactive chat using the OpenAI Responses API.",
    )
    chat_parser.add_argument("--db", default=DEFAULT_DATABASE)
    chat_parser.add_argument("--model", default="gpt-5-mini")

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Inspect stored memory versions and provenance.",
    )
    inspect_parser.add_argument("--db", default=DEFAULT_DATABASE)
    inspect_parser.add_argument(
        "--status",
        choices=["active", "superseded"],
        default=None,
    )
    return parser


def run_demo(database_path: str) -> None:
    with MemoryStore(database_path) as store:
        first_event = store.record_event(
            "user",
            "I live in Seattle and prefer meetings after 10am.",
        )
        store.set_memory(
            MemoryWrite(
                subject="user",
                predicate="home_city",
                value="Seattle",
                kind="profile",
                importance=0.8,
            ),
            first_event,
        )
        store.set_memory(
            MemoryWrite(
                subject="user",
                predicate="meeting_time",
                value="after 10:00 local time",
                kind="preference",
                importance=0.9,
            ),
            first_event,
        )

        second_event = store.record_event(
            "user",
            "I moved to San Francisco last month.",
        )
        store.set_memory(
            MemoryWrite(
                subject="user",
                predicate="home_city",
                value="San Francisco",
                kind="profile",
                importance=0.8,
            ),
            second_event,
        )

        third_event = store.record_event(
            "user",
            "I am exploring roles focused on memory and persistent agents.",
        )
        store.set_memory(
            MemoryWrite(
                subject="user",
                predicate="career_focus",
                value="memory and persistent-agent research roles",
                kind="project",
                importance=1.0,
            ),
            third_event,
        )

        query = "Schedule a research conversation about persistent agents"
        print("Memory history:")
        for memory in store.list_memories():
            print(
                f"  #{memory.id} {memory.status:10} "
                f"{memory.subject}.{memory.predicate} = {memory.value}"
            )
        print(f"\nRetrieved context for: {query!r}")
        print(store.build_context(query) or "(none)")


def run_chat(database_path: str, model_name: str) -> None:
    with MemoryStore(database_path) as store:
        agent = PersistentMemoryAgent(
            store=store,
            model=OpenAIResponsesModel(model_name),
        )
        print("Persistent memory agent. Press Ctrl-D to exit.")
        while True:
            try:
                user_message = input("\nYou: ")
            except EOFError:
                print()
                return
            except KeyboardInterrupt:
                print()
                return
            if not user_message.strip():
                continue
            try:
                turn = agent.handle_message(user_message)
            except (RuntimeError, ValueError) as error:
                print(f"Error: {error}")
                continue
            print(f"Agent: {turn.reply}")


def run_inspect(database_path: str, status: str | None) -> None:
    with MemoryStore(database_path) as store:
        memories = store.list_memories(status=status)
        if not memories:
            print("No memories found.")
            return
        for memory in memories:
            print(
                f"#{memory.id} [{memory.status}/{memory.kind}] "
                f"{memory.subject}.{memory.predicate} = {memory.value} "
                f"(event {memory.source_event_id}, "
                f"supersedes {memory.supersedes_id})"
            )


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "demo":
        run_demo(args.db)
    elif args.command == "chat":
        run_chat(os.path.expanduser(args.db), args.model)
    elif args.command == "inspect":
        run_inspect(os.path.expanduser(args.db), args.status)
