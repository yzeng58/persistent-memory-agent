# Persistent Personal Agent

A day-in-the-life demonstration of a persistent personal AI chief of staff.

**Interactive demo:** https://yzeng58.github.io/persistent-memory-agent/

The central idea is broader than chat memory. A useful personal agent wakes up
with the user's context, monitors the parts of life spread across different
apps, applies domain-specific judgment, routes each task to the right tool, and
acts with appropriate confirmation gates.

## What the demo shows

- **Morning operating brief:** combines calendars, email, reminders, market
  context, AI news, card offers, spending, and food suggestions.
- **Email and commitment tracking:** drafts replies, extracts deadlines, and
  creates follow-up reminders.
- **Relationship-aware communication:** identifies who a person is, selects an
  appropriate tone, checks scheduling constraints, and chooses the established
  communication channel.
- **Cross-app routing:** sends Microsoft work tasks through authenticated Teams
  browser workflows while other tasks use the appropriate account and tool.
- **Personal judgment:** carries work history, network context, saved books and
  research, financial preferences, food preferences, and aesthetic context
  across sessions.
- **Confirmation gates:** prepares actions but stops before high-impact steps
  such as sending a message.

## Example: message my manager

```text
Request: Message Dimitris that the next BenchPress version is ready and ask
whether the meeting can move to 10am.

1. people-ops identifies Dimitris as the user's manager and collaborator.
2. workplace-communication chooses a concise, warm, proactive tone.
3. calendar-ops checks both calendars.
4. teams-ops selects Microsoft Teams as the established channel.
5. browser routes the action through authenticated Chrome DevTools.
6. The agent presents the exact draft and stops before Send.
```

The point is not the individual tools. The value comes from maintaining enough
context to choose the right sequence without making the user restate who the
person is, why the task matters, which channel to use, or how the message should
sound.

## Everyday domains

- Calendar, travel, priorities, and reminders
- Gmail and Outlook
- Stocks, portfolio context, and AI news
- Credit-card offers, coupons, bills, budgets, and spending
- Daily food suggestions
- Personal and professional network memory
- Workplace communication research and books
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
