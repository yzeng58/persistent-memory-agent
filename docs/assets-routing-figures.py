# -*- coding: utf-8 -*-
H = 42

def box(x, y, w, label, kind, sub=None):
    cls = {"mod": "g-mod", "file": "g-file", "req": "g-req",
           "rule": "g-rule", "off": "g-off"}[kind]
    t = f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{H}" rx="5"/>'
    cx = x + w / 2
    if sub is None:
        t += f'<text x="{cx:.0f}" y="{y+26}" text-anchor="middle">{label}</text>'
    else:
        t += f'<text x="{cx:.0f}" y="{y+18}" text-anchor="middle">{label}</text>'
        t += f'<text class="g-sub" x="{cx:.0f}" y="{y+33}" text-anchor="middle">{sub}</text>'
    return t + '</g>'

def elbow(x1, ybot, x2, ytop, off=False):
    ym = (ybot + ytop) / 2
    c = "g-edge g-edge-off" if off else "g-edge"
    return f'<path class="{c}" d="M {x1} {ybot} V {ym:.0f} H {x2} V {ytop}"/>'

DEFS = ('<defs><marker id="arw" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 1 L 7 4 L 0 7 z" fill="#b0b8b3"/></marker></defs>')

def svg(w, h, parts, label):
    return (f'<svg class="routing-map" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{label}">' + DEFS + "".join(parts) + '</svg>')

# ---------- Figure: booking a flight ----------
def fig_flight():
    e, n = [], []
    n.append(box(255, 18, 390, '&#8220;book me a flight to the conference&#8221;', 'req'))
    n.append(box(370, 100, 160, 'travel-ops', 'mod'))
    n.append(box(120, 184, 250, 'flights/money-saving.md', 'file', 'points vs cash, nearby airports'))
    n.append(box(510, 184, 250, 'travel/README.md', 'file', 'preferences + source table'))
    n.append(box(44, 268, 186, 'finance/', 'file', 'card benefits'))
    n.append(box(250, 268, 180, 'account-ops', 'mod', 'airline numbers'))
    n.append(box(450, 268, 220, 'identity_documents/', 'file', 'passport'))
    n.append(box(690, 268, 180, 'network/&hellip;/', 'file', 'other travellers'))
    n.append(box(330, 352, 240, 'travel/trips/&lt;trip&gt;/', 'file', 'the booking, written back'))
    e.append(elbow(450, 60, 450, 100))
    e.append(elbow(450, 142, 245, 184)); e.append(elbow(450, 142, 635, 184))
    for cx in (137, 340, 560, 780):
        e.append(elbow(635, 226, cx, 268))
    e.append('<path class="g-edge g-edge-loop" marker-end="url(#arw)" d="M 370 121 H 16 V 373 H 326"/>')
    return svg(900, 410, e + n, 'Routing map for booking a flight')

# ---------- Figure: the second experiment ----------
def fig_experiment():
    e, n = [], []
    n.append(box(265, 18, 370, '&#8220;now implement the second experiment&#8221;', 'req'))
    n.append(box(360, 100, 180, 'experiment-ops', 'mod'))
    n.append(box(250, 184, 400, 'search for an existing metric before writing one', 'rule', 'step 2, run before any code is written'))
    n.append(box(110, 268, 300, 'the evaluation already written', 'file', 'imported, not rewritten'))
    n.append(box(490, 268, 300, 'written once, in one file', 'file', 'every later experiment calls it'))
    e.append(elbow(450, 60, 450, 100))
    e.append(elbow(450, 142, 450, 184))
    e.append(elbow(450, 226, 260, 268)); e.append(elbow(450, 226, 640, 268))
    return svg(900, 326, e + n, 'Routing map for reusing an evaluation')

# ---------- Figure: saving an idea ----------
def fig_idea():
    e, n = [], []
    n.append(box(285, 18, 330, '&#8220;save this idea for later&#8221;', 'req'))
    n.append(box(330, 100, 240, 'system-maintenance', 'mod', 'the only module that creates files'))
    n.append(box(330, 184, 240, 'file-directory.md', 'file', 'where things go'))
    n.append(box(110, 268, 290, 'the file that holds the idea', 'file', 'one location, decided by the tree'))
    n.append(box(500, 268, 290, 'a pointer from the project', 'file', 'so the file is named somewhere'))
    e.append(elbow(450, 60, 450, 100))
    e.append(elbow(450, 142, 450, 184))
    e.append(elbow(450, 226, 255, 268)); e.append(elbow(450, 226, 645, 268))
    return svg(900, 326, e + n, 'Routing map for saving an idea')

# ---------- Figure: air fryer ----------
def fig_fryer():
    e, n = [], []
    n.append(box(255, 18, 390, '&#8220;which air fryer should I get my parents&#8221;', 'req'))
    n.append(box(370, 100, 160, 'purchase-ops', 'mod'))
    n.append(box(90, 184, 300, 'network/family/parents/', 'file', 'whose kitchen this is for'))
    n.append(box(510, 184, 300, 'living/', 'off', 'my apartment &mdash; no edge leads here'))
    e.append(elbow(450, 60, 450, 100))
    e.append(elbow(450, 142, 240, 184))
    e.append(elbow(450, 142, 660, 184, off=True))
    return svg(900, 242, e + n, 'Routing map for a purchase made for someone else')

# ---------- Figure: what gets stored ----------
def fig_storage():
    e, n = [], []
    n.append(box(310, 18, 280, 'something I tell the assistant', 'req'))
    n.append(box(330, 100, 240, 'file-directory.md', 'file', 'decides where it goes'))
    n.append(box(15, 184, 270, 'references/personal/&hellip;', 'file', 'true until I change it'))
    n.append(box(310, 184, 280, 'reminders.json', 'file', 'carries its own end date'))
    n.append(box(615, 184, 275, 'not stored at all', 'off', 'fetched from the source when needed'))
    e.append(elbow(450, 60, 450, 100))
    for cx in (150, 450, 752):
        e.append(elbow(450, 142, cx, 184))
    return svg(900, 242, e + n, 'Where an incoming fact is stored')

# ---------- Figure: negotiation ----------
def fig_negotiation():
    e, n = [], []
    n.append(box(255, 18, 390, '&#8220;how do I push back on the rent increase&#8221;', 'req'))
    n.append(box(375, 100, 150, 'negotiation', 'mod'))
    n.append(box(140, 184, 250, 'rent.md', 'file', 'what applies to a lease'))
    n.append(box(510, 184, 250, 'framework.md', 'file', 'prepare, open, explore, propose'))
    n.append(box(280, 268, 340, 'books/', 'file', 'the three sources the framework is built on'))
    n.append(box(280, 352, 340, 'anti-patterns.md', 'rule', 'the draft is checked and rewritten until it passes'))
    e.append(elbow(450, 60, 450, 100))
    e.append(elbow(450, 142, 265, 184)); e.append(elbow(450, 142, 635, 184))
    e.append(elbow(265, 226, 450, 268)); e.append(elbow(635, 226, 450, 268))
    e.append(elbow(450, 310, 450, 352))
    e.append('<path class="g-edge g-edge-loop" marker-end="url(#arw)" d="M 620 373 H 800 V 205 H 766"/>')
    return svg(900, 410, e + n, 'Routing map for a negotiation question')

FIGS = {
    "flight": fig_flight(), "experiment": fig_experiment(), "idea": fig_idea(),
    "fryer": fig_fryer(), "storage": fig_storage(), "negotiation": fig_negotiation(),
}
