# -*- coding: utf-8 -*-
"""Trace figures for the write-up.

Rules live in docs/figure-spec.md. Read that first.
Run: python docs/trace-figures.py   (rewrites the figures in docs/index.html)
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

CW, RH, X0, Y0 = 7.83, 21, 30, 74      # char width, row height, left pad, top pad
RUN, LANE, BR = 30, 20, 8.5            # gap after tree, lane pitch, badge radius
ELLIPSIS = "\u2026"


# ---------------------------------------------------------------- tree spec --
def d(name, kids=None, key=None):
    return (name, kids, key)


def f(name, key=None):
    return (name, None, key)


ELL = f(ELLIPSIS)


def flatten(spec, root):
    """spec -> (rows, chain, namelen). rows = [(key, prefixed line, is_ellipsis)]"""
    rows = [(None, root, False)]
    chain, namelen = {}, {0: len(root)}

    def walk(nodes, prefix, anc):
        for i, (name, kids, key) in enumerate(nodes):
            last = i == len(nodes) - 1
            r = len(rows)
            rows.append((key, prefix + ("└── " if last else "├── ") + name,
                         name == ELLIPSIS))
            namelen[r] = len(name)
            if key:
                chain[key] = anc + [r]
            if kids:
                walk(kids, prefix + ("    " if last else "│   "), anc + [r])

    walk(spec, "", [0])
    return rows, chain, namelen


# ------------------------------------------------------------------- render --
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(sc):
    rows, chain, namelen = flatten(sc["tree"], sc.get("root", ".copilot/"))
    idx = {k: i for i, (k, _, _) in enumerate(rows) if k}
    steps = sc["steps"]

    for a, b, _ in steps:
        for k in (a, b):
            if k not in idx:
                raise KeyError("%s: step key %r not in tree" % (sc["id"], k))

    rowy = lambda i: Y0 + i * RH
    right = lambda i: X0 + len(rows[i][1]) * CW + 14
    lane0 = X0 + max(len(t) for _, t, _ in rows) * CW + RUN
    W = int(lane0 + LANE * len(steps) + 24)
    H = rowy(len(rows)) + 10

    def label(k):
        parts = [rows[r][1].split("── ")[-1] for r in chain[k][1:]]
        return "".join(parts[-3:])

    o = ['<svg class="trace-map" viewBox="0 0 %d %d" style="max-width:%.0fpx" '
         'role="img" aria-label="%s">' % (W, H, W * 1.15, sc["aria"]),
         '<defs><marker id="tr-%s" viewBox="0 0 8 8" refX="7" refY="4" '
         'markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">'
         '<path d="M0 1L7 4L0 7z"/></marker>'
         '<marker id="tr-%s-on" viewBox="0 0 8 8" refX="7" refY="4" '
         'markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">'
         '<path d="M0 1L7 4L0 7z"/></marker></defs>' % (sc["id"], sc["id"]),
         '<text class="trace-prompt" x="%d" y="32">&#8220;%s&#8221;</text>'
         % (X0, sc["prompt"])]

    for i, (_, line, is_ell) in enumerate(rows):
        y = rowy(i)
        nx = X0 + (len(line) - namelen[i]) * CW
        o.append('<g class="trow%s" data-row="%d">'
                 '<rect class="thl" x="%d" y="%d" width="%.0f" height="19" rx="3"/>'
                 '<rect class="tbox" x="%.0f" y="%d" width="%.0f" height="19" rx="3"/>'
                 '<text x="%d" y="%d" xml:space="preserve">%s</text></g>'
                 % (" tell" if is_ell else "", i, X0 - 9, y - 14,
                    len(line) * CW + 18, nx - 7, y - 14, namelen[i] * CW + 14,
                    X0, y, esc(line)))

    for n, (a, b, why) in enumerate(steps):
        i0, i1 = idx[a], idx[b]
        y0, y1 = rowy(i0) - 8, rowy(i1) - 3
        lx = lane0 + n * LANE
        path = "M %.0f %d H %.0f V %d H %.0f" % (right(i0), y0, lx, y1, right(i1))
        o.append('<g class="thop" data-step="%d" data-rows="%s" data-ends="%d,%d" '
                 'data-src="%s" data-dst="%s" data-why="%s">'
                 '<path class="twire" d="%s" fill="none" marker-end="url(#tr-%s)"/>'
                 '<path class="thit" d="%s" fill="none"/>'
                 '<circle class="tbadge" cx="%.0f" cy="%.0f" r="%s"/>'
                 '<text class="tnum" x="%.0f" y="%.0f" text-anchor="middle">%d</text>'
                 '</g>'
                 % (n + 1, ",".join(map(str, chain[a] + chain[b])), i0, i1,
                    esc(label(a)), esc(label(b)), why, path, sc["id"], path,
                    lx, (y0 + y1) / 2, BR, lx, (y0 + y1) / 2 + 4, n + 1))

    return "\n".join(o) + "</svg>"


def figure(sc):
    return ('<!--TRACE:%s-->\n<figure class="system-figure trace-figure">\n'
            '<div class="trace" data-trace="%s"><div class="trace-tip" '
            'role="status"></div>\n%s\n</div>\n'
            '<figcaption class="map-caption">%s</figcaption>\n</figure>\n'
            '<!--/TRACE:%s-->' % (sc["id"], sc["id"], svg(sc), sc["caption"], sc["id"]))


# ----------------------------------------------------------------- scenarios --
from trace_scenarios import SCENARIOS  # noqa: E402


def patch(html):
    for sc in SCENARIOS:
        new = figure(sc)
        marker = re.compile(r"<!--TRACE:%s-->.*?<!--/TRACE:%s-->" % (sc["id"], sc["id"]),
                            re.S)
        if marker.search(html):
            html = marker.sub(lambda _: new, html, count=1)
            continue
        old = re.compile(
            r'<figure class="system-figure">\s*<svg class="routing-map"[^>]*'
            r'aria-label="%s".*?</figure>' % re.escape(sc["replaces"]), re.S)
        hits = len(old.findall(html))
        if hits != 1:
            raise SystemExit("%s: matched %d figures, expected 1" % (sc["id"], hits))
        html = old.sub(lambda _: new, html, count=1)
    return html


if __name__ == "__main__":
    p = os.path.join(HERE, "index.html")
    src = io.open(p, encoding="utf-8").read()
    out = patch(src)
    io.open(p, "w", encoding="utf-8").write(out)
    for sc in SCENARIOS:
        rows, _, _ = flatten(sc["tree"], sc.get("root", ".copilot/"))
        print("%-12s %2d rows  %2d steps" % (sc["id"], len(rows), len(sc["steps"])))
