# Persistent Personal Agent Project

## Purpose

Build a public, privacy-safe day-in-the-life demonstration of a persistent
personal AI chief of staff, backed by a reference implementation of durable
memory. The public story must lead with what the agent does across everyday
work and life, not with storage internals.

## Privacy Boundary

- All checked-in examples use synthetic people, projects, and preferences.
- Never read from or copy private local agent state, personal references, email,
  calendar, browser profiles, credentials, or unrelated projects.
- API keys are supplied only through standard secret environment variables and
  are never stored in the repository.
- The static web demo is a deterministic visualization, not a live personal
  account.

## Structure

```text
.
├── docs/                         # Static GitHub Pages demonstration
├── src/persistent_memory_agent/  # Python reference implementation
├── tests/                        # Standard-library unit tests
├── .github/
│   ├── instructions/             # Repository-specific Copilot instructions
│   └── project.md                # Canonical project structure and workflow
├── pyproject.toml                # Package and CLI definition
└── README.md                     # Public project explanation and quickstart
```

## Architecture

- `models.py`: immutable domain records shared by storage, retrieval, and agent
  orchestration.
- `store.py`: canonical owner of the SQLite schema, memory lifecycle, retrieval,
  and context packing.
- `agent.py`: one-turn orchestration over a model backend and the memory store.
- `openai_model.py`: optional OpenAI Responses API adapter.
- `cli.py`: thin `demo`, `chat`, and `inspect` entrypoints.
- `docs/`: product demonstration of a morning briefing and a relationship-aware,
  cross-app communication workflow.

Future storage or model backends must preserve the domain contracts in
`models.py` and `agent.py` rather than creating a second memory lifecycle.

## Naming

- Python modules and functions use `snake_case`.
- Memory predicates use stable `snake_case` keys such as `home_city`.
- Synthetic examples use obviously fictional data.
- Generated databases, caches, and local environments are ignored by Git.

## Workflow

1. Update the canonical implementation in `src/persistent_memory_agent/`.
2. Add or update deterministic tests in `tests/`.
3. Keep the product demo focused on user outcomes while accurately representing
   the system's routing, memory, tools, and confirmation gates.
4. Run `python -m unittest discover -s tests -v`.
5. Run `python -m compileall -q src tests`.
6. Verify `docs/index.html` through a local static server before publishing.
