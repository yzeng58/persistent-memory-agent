# Persistent Memory Agent

A privacy-safe reference implementation of persistent personal memory for
tool-using agents.

**Interactive demo:** https://yzeng58.github.io/persistent-memory-agent/

The project focuses on a practical failure mode in long-running agents: a user
changes over time, but naive memory systems either forget everything or keep
injecting stale facts forever. This implementation separates immutable events
from versioned memories so an agent can preserve provenance, supersede outdated
facts, and retrieve only the active context relevant to the current turn.

## What it demonstrates

- **Append-only events:** raw observations remain auditable.
- **Versioned memory:** a new value supersedes an old value without deleting it.
- **Explicit provenance:** every memory points to the event that produced it.
- **Inspectable retrieval:** normalized lexical concepts gate relevance before
  importance, confidence, and recency are combined into a transparent score.
- **Bounded context:** only the highest-value active memories enter the model
  prompt.
- **Privacy boundary:** all public examples are synthetic and disconnected from
  any deployed personal system.

## Architecture

```text
user message
    |
    v
append immutable event
    |
    v
extract typed memory writes
    |
    v
versioned SQLite memory store
    |
    v
rank active memories for the current query
    |
    v
pack a bounded context with provenance
    |
    v
generate the agent response
```

The model backend has only two responsibilities:

1. Extract durable facts explicitly supported by the current user message.
2. Generate a reply grounded in the retrieved memory context.

The memory lifecycle remains model-independent.

The included retriever is intentionally transparent rather than state of the
art. It normalizes a small set of common concepts, requires positive lexical
overlap, and exposes every score. An embedding or learned retriever can replace
that baseline without changing the storage or supersession contracts.

## Quickstart

The deterministic demo has no dependencies beyond Python 3.11:

```bash
python -m pip install -e .
persistent-memory-agent demo
```

Inspect a persistent database:

```bash
persistent-memory-agent inspect --db ~/.persistent-memory-agent/memory.db
```

To run the optional OpenAI Responses API chat adapter:

```bash
python -m pip install -e '.[openai]'
export OPENAI_API_KEY=...
persistent-memory-agent chat --model gpt-5-mini
```

The model is a CLI parameter rather than hidden configuration. The API key is
the only environment variable because it is a secret.

## Memory model

Each active memory has a stable key:

```text
(subject, predicate, kind) -> value
```

For example:

```text
(user, home_city, profile) -> San Francisco
```

If the user previously lived in Seattle, the Seattle record remains in history
with `status = superseded`, while the San Francisco record links back through
`supersedes_id`.

Memory kinds in the reference implementation:

- `profile`
- `preference`
- `project`
- `relationship`
- `commitment`
- `procedure`

This deliberately excludes free-form hidden summaries. Every memory must have a
stable key, value, type, provenance event, confidence, and importance.

## Repository layout

```text
docs/                         Static synthetic browser demo
src/persistent_memory_agent/  Memory store, agent loop, and optional model adapter
tests/                        Deterministic standard-library tests
```

## Run tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

## Privacy and safety

The repository contains no real personal memories, credentials, emails,
calendar events, browser state, or private tool output. The static demo uses a
small fictional history solely to visualize the lifecycle.

Retrieved memory is treated as contextual evidence, not as an instruction. A
current user message overrides stale memory, and supersession makes that update
inspectable.

## License

MIT
