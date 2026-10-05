"""Helpers for writing Module 1 slides. One-off authoring aid, not a generator:
the produced HTML is the hand-edited source from then on."""
import html, json, re

def esc(s):
    return html.escape(s, quote=True)

# ---------- flow diagrams ----------
def N(id, label, kind=None, x=0, y=0, w=240, h=70, flag=None):
    d = {"id": id, "label": label, "x": x, "y": y, "w": w, "h": h}
    if kind: d["kind"] = kind
    if flag: d["flag"] = flag
    return d

def E(id, frm, to, label="", **kw):
    d = {"id": id, "from": frm, "to": to, "label": label}
    d.update(kw)
    return d

def S(show=(), run=(), set=None):
    return {"show": list(show), "run": list(run), "set": set or {}}

def spec(width, height, nodes, edges, steps, legend=False, flags=None):
    d = {"width": width, "height": height, "nodes": nodes, "edges": edges, "steps": steps, "legend": legend}
    if flags: d["flags"] = flags
    return d

def static_spec(width, height, nodes, edges, set=None, legend=False, flags=None):
    """One step that shows everything: for a picture that does not change."""
    ids = [n["id"] for n in nodes] + [e["id"] for e in edges]
    return spec(width, height, nodes, edges, [S(ids, [], set)], legend, flags)

def flow_static(sp):
    return '<div class="lu-flow"><script type="application/json" class="lu-flow__spec">%s</script></div>' % json.dumps(sp)

def flow_walk(label, sp, captions):
    """captions: list of (short, long_html). Steps in sp must match."""
    assert len(sp["steps"]) == len(captions), (label, len(sp["steps"]), len(captions))
    steps = "".join(
        '<div data-walk-step="%d" data-caption-short="%s" data-caption="%s"%s></div>'
        % (i + 1, esc(short), esc("<b>Step %d.</b> %s" % (i + 1, cap)), "" if i == 0 else " hidden")
        for i, (short, cap) in enumerate(captions))
    return ('<div class="lu-walk" data-label="%s"><div class="lu-walk__view"><div class="lu-flow">'
            '<script type="application/json" class="lu-flow__spec">%s</script></div>%s</div></div>'
            % (esc(label), json.dumps(sp), steps))

def code_walk(label, steps_code, captions):
    """steps_code: list of (filename, code_text). Plain code walkthrough."""
    out = []
    for i, ((name, text), (short, cap)) in enumerate(zip(steps_code, captions)):
        out.append('<div data-walk-step="%d" data-caption-short="%s" data-caption="%s"%s>%s</div>'
                   % (i + 1, esc(short), esc("<b>Step %d.</b> %s" % (i + 1, cap)), "" if i == 0 else " hidden", code(name, text)))
    return '<div class="lu-walk" data-label="%s"><div class="lu-walk__view">%s</div></div>' % (esc(label), "".join(out))

# ---------- code with light highlighting ----------
_TOK = re.compile(r'(#[^\n]*|//[^\n]*)|("(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\')')
def highlight(text):
    out, pos = [], 0
    for m in _TOK.finditer(text):
        out.append(esc(text[pos:m.start()]))
        cls = "tok-com" if m.group(1) else "tok-str"
        out.append('<span class="%s">%s</span>' % (cls, esc(m.group(0))))
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)

def code(name, text, sm=True, style=""):
    return ('<div class="lu-code%s" data-name="%s"%s><pre><code>%s</code></pre></div>'
            % (" lu-code--sm" if sm else "", esc(name), (' style="%s"' % style) if style else "", highlight(text.strip("\n"))))

# ---------- blocks ----------
def callout(label, body, concept=True):
    return ('<div class="lu-callout%s"><span class="lu-callout__label">%s</span><p class="lu-sub">%s</p></div>'
            % (" lu-callout--concept" if concept else "", label, body))

def table(head, rows, cls="lu-table", style=""):
    h = "".join("<th>%s</th>" % c for c in head)
    r = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in row) for row in rows)
    return '<table class="%s"%s><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (cls, (' style="%s"' % style) if style else "", h, r)

def slide(label, section, minutes, eyebrow, title, body, notes, tint=False, h2cls="lu-h2", h2style=""):
    cls = "slide slide--tint" if tint else "slide"
    tight = ' style="--lu-s5:12px"' if ('lu-walk' in body and 'lu-callout' in body) else ""
    head = ""
    if eyebrow: head += '<div class="lu-eyebrow">%s</div>\n  ' % eyebrow
    if title: head += '<h2 class="%s"%s>%s</h2>\n  ' % (h2cls, (' style="%s"' % h2style) if h2style else "", title)
    return ('<section class="%s" data-label="%s" data-section="%s" data-minutes="%d"%s>\n  %s%s\n  <template data-notes>%s</template>\n</section>\n'
            % (cls, esc(label), section, minutes, tight, head, body, notes))

def divider(label, section, minutes, eyebrow, title, lead, notes):
    return ('<section class="slide slide--night" data-chrome="none" data-label="%s" data-section="%s" data-minutes="%d">\n'
            '  <div class="slide__body lu-center" style="gap:var(--lu-s5)">\n'
            '    <div class="lu-eyebrow">%s</div>\n'
            '    <h2 class="lu-display-xl" style="max-width:22ch">%s</h2>\n'
            '    <p class="lu-lead" style="max-width:44ch">%s</p>\n  </div>\n  <template data-notes>%s</template>\n</section>\n'
            % (esc(label), section, minutes, eyebrow, title, lead, notes))

def html_walk(label, step_html, captions):
    """A walkthrough whose steps are arbitrary HTML (tables, code, anything)."""
    out = []
    for i, (h, (short, cap)) in enumerate(zip(step_html, captions)):
        out.append('<div data-walk-step="%d" data-caption-short="%s" data-caption="%s"%s>%s</div>'
                   % (i + 1, esc(short), esc("<b>Step %d.</b> %s" % (i + 1, cap)), "" if i == 0 else " hidden", h))
    return '<div class="lu-walk" data-label="%s"><div class="lu-walk__view">%s</div></div>' % (esc(label), "".join(out))

def figure(src, alt, caption, maxh=300, style=""):
    """A real figure cropped from a paper, with a caption naming its source."""
    return ('<figure class="lu-figure" style="align-items:center;%s"><img src="%s" alt="%s" '
            'style="display:block;width:auto;height:auto;max-width:100%%;max-height:%dpx;border-radius:var(--lu-r3)">'
            '<figcaption>%s &middot; <a href="%s" target="_blank" rel="noopener">Open full size</a></figcaption></figure>' % (style, src, esc(alt), maxh, caption, src))
