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
- `docs/index.html`: looping cinematic browser animation. The opening scene
  runs `yuchen-assistant`, presents important notices and schedule, then shows
  Food, Work & Inbox, Stock, AI & Research, Deals, and Secondhand report
  entrances. The cinematic cursor opens Stock as the representative deep-dive.
- `docs/architecture.html`: the written companion to the demo, titled
  "How to make a personal AI system that knows you well". Nine sections:
  addressing, the tree that uniqueness forces, what is worth saving, the control
  plane, an eight-step build recipe, an inventory of the deployed system, how
  books become output gates, honest costs, and a reproducible quickstart. It
  describes the private deployment in aggregate without exposing instructions,
  credentials, personal data, or identifiable names.

Future storage or model backends must preserve the domain contracts in
`models.py` and `agent.py` rather than creating a second memory lifecycle.

## The Article

`docs/architecture.html` is a technical write-up, not a landing page. It exists
to make a reader able to build the same thing.

Its structure is fixed and was set by the author. Do not renumber or re-scope
these without asking:

1. **Where it fell short** — 1.1 It remembers the wrong things · 1.2 It answers
   like the median person · 1.3 It never gets better
2. **Approach** — 2.1 Address space and assignment rules · 2.2 Domain modules ·
   2.3 Schema evolution
3. **The deployed system** — 3.1 Domain inventory · 3.2 Module catalog

Sections 2.1, 2.2, and 2.3 each repair exactly one failure from section 1, in
that order. Every subsection ends with a numbered procedure.

### Vocabulary

These names are canonical. Do not introduce synonyms for them.

| Concept | Canonical name |
|---|---|
| The governing layer that does no domain work | control plane |
| The seventy working modules | data plane, or domain modules |
| The always-resident top-level instruction file | the charter |
| The only component allowed to create, move, or delete parts | the registrar |
| A module's `SKILL.md` | router |
| A module's `assets/` | procedures |
| A module's `references/` | the record |
| The decision tree that assigns paths | the address space |
| A pointer that lets two branches reach one file | cross-link |

### Rules

- **Headings are noun phrases.** A section title names its subject and stops.
  No colon punchline, no em-dash subtitle, no imperative slogan. Write
  `Address space and assignment rules`, not
  `Address space: give every fact one address`. The only narrative headings
  allowed are in the motivation section.
- **No slogan blocks.** Centered one-line aphorisms are banned. If a sentence
  would look at home on a product page, it does not belong here. Every
  emphasized block must contain a rule, a measurement, or a file.
- **Report, do not sell.** State what was built, what it cost, and where it
  fails. Never state a benefit without the mechanism that produces it.
- **Steps, not prose.** A reader must be able to follow the article one action
  at a time. Prefer bullets, numbered steps, tables, and trees over paragraphs.
  No section may be a wall of continuous text.
- **Every claim carries an artifact.** A design assertion is only allowed next
  to a real tree, rule, count, or file listing taken from the running system.
  Never invent an example, a number, or a rule that is not on disk.
- **Numbers get verified before they are written.** Counts in the article
  (modules, files, bytes, ratios, dates) are measured, not remembered. Re-measure
  before changing any of them.
- **Every section ends with something executable** — a tree, an assertion, a
  checklist, or a numbered procedure. Not a summary sentence.
- **Keep the tradeoffs section honest.** Section 8 must state real costs,
  including where this design is worse than similarity search. Removing it makes
  the whole article read as marketing.
- **The article must obey its own rules.** One canonical statement per idea; if
  a point is repeated, one of the two copies is wrong. Terminology is uniform
  because uniformity is the thesis.

### Privacy

- No employer, team, org, cluster, or internal codename. Generalize
  infrastructure names and say that they were generalized.
- No real colleague names, and no words attributed to a real person.
- Domains and module names may be listed; their contents may not be quoted.
- Aggregate counts are publishable. Individual records are not.
- Before publishing: render the page and search the text for names, employers,
  and internal terms. Do not rely on reading the source.

### Validation

1. `python - <<` tag-balance and anchor check: every `href="#x"` resolves to a
   `<section id="x">`.
2. Serve `docs/` locally and load the page with a real browser; require zero
   console errors and zero failed requests.
3. Screenshot the full scroll and read it as a reader would.
4. Grep the rendered `innerText` (not the HTML) for private terms.

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
8. When `docs/architecture.html` changes, run the four checks in
   **The Article / Validation** before publishing.
