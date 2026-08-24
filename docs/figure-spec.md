# Trace figure spec

Rules for every routing figure in the write-up. `trace-figures.py` implements them;
this file is the authority when the two disagree.

One figure per scenario. Nothing is shared between figures.

## 1. Form

1. The left side is a real file tree, rendered the way `tree` renders it —
   `├──`, `└──`, `│` prefixes. **One file or folder per line.** Never collapse a
   path into `a/b/c.md` on a single line.
2. The right side is the chain of thought: one line per step, leaving the file
   that was just read and arriving at the file it names next, routed through a
   vertical lane to the right of the tree. One lane per step, left to right in
   step order.
3. Each scenario gets **its own tree**, cut down to that scenario. Trees are not
   shared or reused across figures.

## 2. What goes in the tree

4. Every file the trace touches is shown, and so is **every folder on the path
   down to it**, one level per line.
5. A folder that is expanded shows: every entry the trace needs, **plus at most
   three** entries it does not need, plus a single `…` line if anything is left
   over.
6. A folder the trace never enters is shown as **one line, not expanded**.
   Whatever is left at that level is closed off with a single `…` line.
7. **Default colour is black** — the same as ordinary text. Grey has exactly one
   meaning: *there is more here that the figure is not showing*, i.e. the `…`
   lines. Nothing else is grey.
8. Real people are always `<name>/`. Same for anything else that would identify a
   person, an employer or an institution.

## 3. Colour

9. Green `#4a7c59`, dark green `#2f5d43` for the active step. **No red anywhere** —
   red reads as an error.

## 4. Interaction

10. Nothing is highlighted by default. The tree is just a tree until the reader
    hovers.
11. Hovering a step highlights the two files it connects **and every folder above
    them, recursively, up to the root**.
12. The two endpoint files also get an outline box. The box wraps **the name
    only** — not the `├── ` prefix in front of it.
13. Every other step fades back.
14. The step number sits at the **midpoint of that step's vertical lane** — not at
    a corner of the path.
15. The explanation is not printed under the figure and does not live in a fixed
    corner. It appears on hover, next to that step's number, and flips to the
    other side of the lane if there is not enough room.

## 5. Writing the explanations

16. Plain words, and long enough to actually explain. Three beats, in order:
    **what this file actually holds → which rule in it fires this time → so which
    file gets opened next.**
17. Everything stated must come from reading the real file. Nothing is invented.
18. No real names, employers, institutions, or account identifiers.
