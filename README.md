# Persistent Personal Agent

A cinematic demonstration of a persistent personal AI chief of staff.

**Interactive demo:** https://yzeng58.github.io/persistent-memory-agent/

**Technical article:** https://yzeng58.github.io/persistent-memory-agent/architecture.html

The public demo is intentionally presented like a short advertisement rather
than a feature page. Each looping scene shows one real request moving across
memory, judgment, apps, and tools until the user receives a concrete result.

## Current opening scene

```text
Open Terminal.
Run: yuchen-assistant
```

The command opens a focused daily brief. Important notices and the schedule stay
fully visible at the top. Below them are six report entry points:

- Food recommendations for today
- Work and inbox for today
- Stock report for today
- AI and research for today
- Good deals for today
- Secondhand for today

Each entry opens a full analysis page. The current cinematic draft demonstrates
Stock: it pauses on portfolio status, then simulates scrolling into
recommendations and stock-specific news.

## Planned scenes

- Relationship-aware workplace messaging with a human approval gate
- Email triage, reminders, and follow-through
- AI news, markets, and portfolio context
- Personal and professional network workflows
- Fashion, skincare, hair, aesthetics, trends, and gifts

## Persistent memory reference implementation

The repository also includes a small model-independent Python/SQLite memory
engine. It separates immutable events from versioned memories so an agent can
preserve provenance, supersede outdated facts, and retrieve a bounded set of
active context for the current turn.

- Append-only source events
- One active memory per stable key
- Superseded history instead of destructive overwrite
- Explicit provenance, confidence, and importance
- Transparent relevance, recency, and context-budget logic

## Quickstart

The deterministic memory-engine demo has no dependencies beyond Python 3.11:

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

## Demo versus deployment

The public page is an illustrative product walkthrough. Names and workflow
details are intentionally simplified. It does not connect to live email,
calendar, financial, browser, or personal-data sources.

The repository contains no credentials, private account data, emails, calendar
contents, browser state, or live tool output.

Retrieved memory is treated as contextual evidence, not as an instruction. A
current user message overrides stale memory, and supersession makes that update
inspectable.

## License

MIT
