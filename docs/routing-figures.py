# -*- coding: utf-8 -*-
"""Routing figures for the write-up. Paths are relative to ~/.copilot/."""

W = 1000
ROW_H = 58
ROW_GAP = 42
CHAR_DIR = 6.35   # 10.5px monospace
CHAR_BASE = 7.85  # 13px monospace
CHAR_SUB = 6.2    # 10.5px sans
PAD = 26

DEFS = ('<defs><marker id="arw" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 1 L 7 4 L 0 7 z" fill="#b0b8b3"/></marker></defs>')


class Node:
    def __init__(self, path, kind, sub=None, plain=None):
        self.path, self.kind, self.sub, self.plain = path, kind, sub, plain
        if plain is not None:
            self.dir, self.base = "", plain
        elif path.endswith("/"):
            i = path.rfind("/", 0, len(path) - 1)
            self.dir, self.base = path[:i + 1], path[i + 1:]
        elif "/" in path:
            i = path.rfind("/")
            self.dir, self.base = path[:i + 1], path[i + 1:]
        else:
            self.dir, self.base = "", path
        w = max(len(self.dir) * CHAR_DIR, len(self.base) * CHAR_BASE,
                len(sub or "") * CHAR_SUB) + 2 * PAD
        self.w = max(150, round(w))
        self.x = self.y = 0

    def svg(self):
        cls = {"mod": "g-mod", "file": "g-file", "req": "g-req",
               "rule": "g-rule", "off": "g-off"}[self.kind]
        cx, x, y, w = self.x + self.w / 2, self.x, self.y, self.w
        lines = [l for l in (self.dir, self.base, self.sub) if l]
        t = f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{ROW_H}" rx="5"/>'
        if len(lines) == 1:
            t += f'<text class="g-base" x="{cx:.0f}" y="{y+34}" text-anchor="middle">{self.base}</text>'
        elif len(lines) == 2 and not self.dir:
            t += f'<text class="g-base" x="{cx:.0f}" y="{y+26}" text-anchor="middle">{self.base}</text>'
            t += f'<text class="g-sub" x="{cx:.0f}" y="{y+43}" text-anchor="middle">{self.sub}</text>'
        elif len(lines) == 2:
            t += f'<text class="g-dir" x="{cx:.0f}" y="{y+24}" text-anchor="middle">{self.dir}</text>'
            t += f'<text class="g-base" x="{cx:.0f}" y="{y+41}" text-anchor="middle">{self.base}</text>'
        else:
            t += f'<text class="g-dir" x="{cx:.0f}" y="{y+19}" text-anchor="middle">{self.dir}</text>'
            t += f'<text class="g-base" x="{cx:.0f}" y="{y+35}" text-anchor="middle">{self.base}</text>'
            t += f'<text class="g-sub" x="{cx:.0f}" y="{y+49}" text-anchor="middle">{self.sub}</text>'
        return t + '</g>'

    @property
    def cx(self): return self.x + self.w / 2
    @property
    def top(self): return self.y
    @property
    def bot(self): return self.y + ROW_H


def mod(p, sub=None): return Node(p, "mod", sub)
def fil(p, sub=None): return Node(p, "file", sub)
def off(p, sub=None): return Node(p, "off", sub)
def req(text): return Node("", "req", plain=text)
def rule(text, sub=None): return Node("", "rule", sub, plain=text)
def rulep(path, sub=None): return Node(path, "rule", sub)


def lay(rows, gaps=None):
    """Centre each row horizontally; return total height."""
    y = 18
    for r, row in enumerate(rows):
        gap = (gaps or {}).get(r, 30)
        total = sum(n.w for n in row) + gap * (len(row) - 1)
        x = (W - total) / 2
        for n in row:
            n.x, n.y = round(x), y
            x += n.w + gap
        y += ROW_H + ROW_GAP
    return y - ROW_GAP + 12


def edge(a, b, off_=False):
    ym = (a.bot + b.top) / 2
    c = "g-edge g-edge-off" if off_ else "g-edge"
    return f'<path class="{c}" d="M {a.cx:.0f} {a.bot} V {ym:.0f} H {b.cx:.0f} V {b.top}"/>'


def render(rows, edges, h, label):
    nodes = [n for row in rows for n in row]
    return (f'<svg class="routing-map" viewBox="0 0 {W} {h}" role="img" '
            f'aria-label="{label}">' + DEFS + "".join(edges)
            + "".join(n.svg() for n in nodes) + '</svg>')


# ---------------- figures ----------------

def fig_email():
    q = req('&#8220;email my collaborator about the draft&#8221;')
    root = mod('copilot-instructions.md', 'top-level routing table')
    po = mod('skills/people-ops/SKILL.md')
    eo = mod('skills/email-ops/SKILL.md')
    net = fil('references/personal/network/README.md', 'lookup table')
    snd = fil('skills/email-ops/references/sender-routing.md', 'which account')
    wg = fil('skills/email-ops/references/writing-guide.md', 'tone and register')
    ao = mod('skills/account-ops/SKILL.md')
    person = fil('references/personal/network/work/&lt;name&gt;/README.md', 'address, history')
    vault = fil('vault.json', 'encrypted')
    rows = [[q], [root], [po, eo], [net, snd, wg, ao], [person, vault]]
    h = lay(rows, {2: 300, 3: 16, 4: 300})
    e = [edge(q, root), edge(root, po), edge(root, eo), edge(po, net),
         edge(eo, snd), edge(eo, wg), edge(eo, ao),
         edge(net, person), edge(ao, vault)]
    return render(rows, e, h, 'Routing map for a single email request')


def fig_flight():
    q = req('&#8220;book me a flight to the conference&#8221;')
    to = mod('skills/travel-ops/SKILL.md')
    ms = fil('skills/travel-ops/flights/money-saving.md', 'points vs cash, nearby airports')
    pref = fil('references/personal/travel/README.md', 'preferences + source table')
    fin = fil('references/personal/finance/', 'card benefits')
    ao = mod('skills/account-ops/SKILL.md', 'airline numbers')
    ids = fil('references/personal/identity_documents/', 'passport')
    ppl = fil('references/personal/network/', 'other travellers')
    trip = fil('references/personal/travel/trips/&lt;trip&gt;/', 'the booking, written back')
    rows = [[q], [to], [ms, pref], [fin, ao, ids, ppl], [trip]]
    h = lay(rows, {2: 60, 3: 14})
    e = [edge(q, to), edge(to, ms), edge(to, pref)] \
        + [edge(pref, n) for n in (fin, ao, ids, ppl)]
    e.append(f'<path class="g-edge g-edge-loop" marker-end="url(#arw)" '
             f'd="M {to.x} {to.y+29:.0f} H 14 V {trip.y+29:.0f} H {trip.x-4}"/>')
    return render(rows, e, h, 'Routing map for booking a flight')


def fig_experiment():
    q = req('&#8220;now implement the second experiment&#8221;')
    eo = mod('skills/experiment-ops/SKILL.md')
    r = rule('search for an existing metric before writing one',
             'a step in the module, run before any code is written')
    a = fil('the evaluation already written', 'imported, not rewritten')
    b = fil('written once, in one file', 'every later experiment calls it')
    rows = [[q], [eo], [r], [a, b]]
    h = lay(rows, {3: 90})
    return render(rows, [edge(q, eo), edge(eo, r), edge(r, a), edge(r, b)], h,
                  'Routing map for reusing an evaluation')


def fig_idea():
    q = req('&#8220;save this idea for later&#8221;')
    sm = mod('skills/system-maintenance/SKILL.md', 'the only module that creates files')
    fd = mod('skills/system-maintenance/file-directory.md', 'where things go')
    a = fil('the file that holds the idea', 'one location, decided by the tree')
    b = fil('a pointer from the project', 'so the file is named somewhere')
    rows = [[q], [sm], [fd], [a, b]]
    h = lay(rows, {3: 90})
    return render(rows, [edge(q, sm), edge(sm, fd), edge(fd, a), edge(fd, b)], h,
                  'Routing map for saving an idea')


def fig_fryer():
    q = req('&#8220;which air fryer should I get my parents&#8221;')
    po = mod('skills/purchase-ops/SKILL.md')
    par = fil('references/personal/network/family/parents/', 'whose kitchen this is for')
    liv = off('references/personal/living/', 'my apartment &mdash; no edge leads here')
    rows = [[q], [po], [par, liv]]
    h = lay(rows, {2: 70})
    return render(rows, [edge(q, po), edge(po, par), edge(po, liv, True)], h,
                  'Routing map for a purchase made for someone else')


def fig_storage():
    q = req('something I tell the assistant')
    fd = mod('skills/system-maintenance/file-directory.md', 'decides where it goes')
    a = fil('references/personal/', 'true until I change it')
    b = fil('references/personal/reminders.json', 'carries its own end date')
    c = off('not stored at all', 'fetched from the source when needed')
    rows = [[q], [fd], [a, b, c]]
    h = lay(rows, {2: 22})
    return render(rows, [edge(q, fd), edge(fd, a), edge(fd, b), edge(fd, c)], h,
                  'Where an incoming fact is stored')


def fig_negotiation():
    q = req('&#8220;how do I push back on the rent increase&#8221;')
    ng = mod('skills/negotiation/SKILL.md')
    rent = fil('skills/negotiation/references/rent.md', 'what applies to a lease')
    fw = fil('skills/negotiation/references/framework.md', 'prepare, open, explore, propose')
    bk = fil('skills/negotiation/references/books/', 'the three sources it is built on')
    ap = rulep('skills/negotiation/references/anti-patterns.md',
                'the draft is checked and rewritten until it passes')
    rows = [[q], [ng], [rent, fw], [bk], [ap]]
    h = lay(rows, {2: 60})
    e = [edge(q, ng), edge(ng, rent), edge(ng, fw), edge(rent, bk), edge(fw, bk),
         edge(bk, ap)]
    e.append(f'<path class="g-edge g-edge-loop" marker-end="url(#arw)" '
             f'd="M {ap.x+ap.w} {ap.y+29:.0f} H {W-14} V {fw.y+29:.0f} H {fw.x+fw.w+4}"/>')
    return render(rows, e, h, 'Routing map for a negotiation question')


FIGS = {"email": fig_email(), "flight": fig_flight(), "experiment": fig_experiment(),
        "idea": fig_idea(), "fryer": fig_fryer(), "storage": fig_storage(),
        "negotiation": fig_negotiation()}
