# Persistent Personal Agent Project

## Purpose

Build a public, privacy-safe series of short cinematic product demonstrations
for a persistent personal AI chief of staff, backed by a reference
implementation of durable memory.

The browser experience is an advertisement, not a landing page:

- Show only the computer and the workflow happening inside it.
- Do not place explanatory copy, capability grids, or technical prose outside
  the computer screen.
- Each scene should communicate one complete user outcome in a short, readable
  sequence; never trade legibility for an arbitrary runtime.
- Prefer visible actions, app transitions, and approval gates over descriptions.
- A terminal command may launch a scene, but the product value must immediately
  unfold into a visual experience rather than terminal-style output.
- Use progressive disclosure instead of dense dashboards: establish one clear
  primary view, then place optional detail in consistent expandable sections.
- Keep visual hierarchy deliberate and reusable. The daily brief starts with
  fixed important notices and schedule, followed by the same report-section
  pattern for deeper domains.
- Analytical deep dives open as independent mini-pages with facts, analysis,
  and recommended actions; never compress them into small accordion bodies.
- Ad deep dives use a linear reading path rather than a detailed dashboard:
  establish status first, then simulate scrolling into the next useful content.

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
- `docs/`: looping cinematic browser animation scenes. The opening scene runs
  `yuchen-assistant`, presents important notices and schedule, then shows Food,
  Work & Inbox, Stock, AI & Research, Deals, and Secondhand report entrances.
  The cinematic cursor opens Stock as the representative deep-dive.

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
3. Add one short cinematic workflow at a time; do not turn the demo back into a
   feature-explanation page.
4. Keep each workflow focused on visible user outcomes while accurately
   representing routing, memory, tools, and confirmation gates.
5. Run `python -m unittest discover -s tests -v`.
6. Run `python -m compileall -q src tests`.
7. Verify `docs/index.html` through a local static server before publishing.
