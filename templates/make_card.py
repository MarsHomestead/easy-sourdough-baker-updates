#!/usr/bin/env python3
"""Fill templates/recipe-card.html from a JSON recipe and write HTML and/or PDF.

Usage:
  make_card.py RECIPE.json OUT.pdf
  make_card.py RECIPE.json OUT.html

Carries no secret. Amounts should be in grams. If a PDF is requested and
Chromium is missing or fails, the HTML is still saved (same name, .html).
"""
import html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE_NAME = "recipe-card.html"

def esc(s):
    return html.escape("" if s is None else str(s), quote=True)

def rich(s):
    """Escape, then turn **bold** into <strong>."""
    t = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)

def link_html(label, url):
    lab, href = esc(label or url or ""), esc(url or "")
    if not href:
        return lab
    return f'<a href="{href}">{lab or href}</a>'

def find_template():
    env = os.environ.get("HIVE_CARD_TEMPLATE")
    if env and Path(env).is_file():
        return Path(env)
    candidates = [
        HERE / TEMPLATE_NAME,
        Path(os.environ.get("HIVE_TEMPLATES") or "") / TEMPLATE_NAME,
    ]
    try:
        exe = Path(sys.argv[0]).resolve().parent
        candidates.append(exe / "templates" / TEMPLATE_NAME)
        if exe.name == "hive-mind":
            candidates.append(exe / "templates" / TEMPLATE_NAME)
    except Exception:
        pass
    for p in candidates:
        if p and p.is_file():
            return p
    return None

def hide_empty(tag_open, inner, default_class=""):
    if not (inner or "").strip():
        # Keep a hidden placeholder so the template tag is consumed.
        if "class=" in tag_open:
            return tag_open.replace('class="', 'class="empty ', 1) + "</" + tag_open.split()[0][1:] + ">"
        return ""
    return None  # caller writes the element

def render_credit(data):
    parts = []
    if data.get("credit"):
        parts.append(rich(data["credit"]))
    for lk in data.get("credit_links") or []:
        if isinstance(lk, dict):
            parts.append(link_html(lk.get("label") or lk.get("url"), lk.get("url")))
    return " ".join(p for p in parts if p)

def render_batch(batch):
    if not batch or not isinstance(batch, dict):
        return ""
    title = esc(batch.get("title") or "Today's batch")
    lede = rich(batch.get("lede") or "")
    rows = []
    for ing in batch.get("ingredients") or []:
        if not isinstance(ing, dict):
            continue
        amt, what = esc(ing.get("amount") or ""), esc(ing.get("item") or ing.get("what") or "")
        if not (amt or what):
            continue
        span = " span" if ing.get("span") else ""
        rows.append(f'<div class="ing{span}"><span class="amt">{amt}</span><span class="what">{what}</span></div>')
    note = rich(batch.get("note") or "")
    html_out = ['<section class="batch">', f"<h2>{title}</h2>"]
    if lede:
        html_out.append(f'<p class="lede">{lede}</p>')
    if rows:
        html_out.append('<div class="ings">')
        html_out.extend(rows)
        html_out.append("</div>")
    if note:
        html_out.append(f'<p class="note">{note}</p>')
    html_out.append("</section>")
    return "\n  ".join(html_out)

def render_section(sec, idx):
    if not sec or not isinstance(sec, dict):
        return ""
    title = esc(sec.get("title") or f"Step {idx}")
    extra = sec.get("class") or "block"
    extra = re.sub(r"[^a-zA-Z0-9_ -]", "", str(extra))
    sid = re.sub(r"[^a-z0-9-]+", "-", (sec.get("id") or f"sec-{idx}").lower()).strip("-") or f"sec-{idx}"
    parts = [f'<section class="card-sec {extra}" id="{esc(sid)}">', f'<h2 class="sec">{title}</h2>']
    if sec.get("goal"):
        parts.append(f'<p class="goal">{rich(sec["goal"])}</p>')
    steps = [s for s in (sec.get("steps") or []) if str(s).strip()]
    if steps:
        parts.append('<ol class="steps">')
        for s in steps:
            parts.append(f"<li>{rich(s)}</li>")
        parts.append("</ol>")
    if sec.get("after"):
        parts.append(f'<p class="goal">{rich(sec["after"])}</p>')
    if sec.get("warn"):
        parts.append(f'<p class="goal warn">{rich(sec["warn"])}</p>')
    folds = [f for f in (sec.get("folds") or []) if isinstance(f, dict) or str(f).strip()]
    if folds:
        parts.append('<div class="folds">')
        for n, f in enumerate(folds, 1):
            if isinstance(f, dict):
                label, text = f.get("label") or f"Fold {n}.", f.get("text") or ""
            else:
                label, text = f"Fold {n}.", str(f)
            parts.append(
                '<label class="fold">'
                f'<input type="checkbox" class="cb" aria-label="{esc(label)}">'
                f'<div><span class="num">{esc(label)}</span> {rich(text)}</div>'
                "</label>"
            )
        parts.append("</div>")
    tips = [t for t in (sec.get("tips") or []) if str(t).strip()]
    if tips:
        parts.append('<div class="tips"><div class="label">Tips</div><ul>')
        for t in tips:
            parts.append(f"<li>{rich(t)}</li>")
        parts.append("</ul></div>")
    parts.append("</section>")
    return "\n  ".join(parts)

def render_aside(aside):
    if not aside or not isinstance(aside, dict):
        return ""
    items = [x for x in (aside.get("items") or []) if str(x).strip()]
    if not items and not aside.get("title"):
        return ""
    title = esc(aside.get("title") or "Baker's notes")
    parts = [f'<section class="aside"><h2 class="sec">{title}</h2><ul>']
    for it in items:
        parts.append(f"<li>{rich(it)}</li>")
    parts.append("</ul></section>")
    return "\n  ".join(parts)

def render_history(history):
    rows = [h for h in (history or []) if isinstance(h, dict) and (h.get("why") or h.get("change"))]
    if not rows:
        return ""
    parts = ['<section class="aside history"><h2 class="sec">Adjustments</h2><ul>']
    for h in rows:
        why = rich(h.get("why") or "")
        change = rich(h.get("change") or "")
        at = esc(h.get("at") or "")
        bit = []
        if at:
            bit.append(f"<strong>{at}</strong>")
        if why:
            bit.append(f'<span class="why">{why}</span>')
        if change:
            bit.append(change)
        parts.append("<li>" + " — ".join(bit) + "</li>")
    parts.append("</ul></section>")
    return "\n  ".join(parts)

def render_notes(data):
    title = data.get("notes_title")
    n = data.get("notes_lines")
    if title is None and n is None:
        title, n = "My notes", 6
    if n == 0:
        return ""
    try:
        n = max(0, int(n if n is not None else 6))
    except (TypeError, ValueError):
        n = 6
    if n == 0:
        return ""
    parts = [f'<section class="notes"><h2 class="sec">{esc(title or "My notes")}</h2>']
    parts.extend(['<div class="line"></div>'] * n)
    parts.append("</section>")
    return "\n  ".join(parts)

def render_footer(data):
    bits = []
    if data.get("footer"):
        bits.append(rich(data["footer"]))
    for lk in data.get("footer_links") or []:
        if isinstance(lk, dict):
            bits.append(link_html(lk.get("label") or lk.get("url"), lk.get("url")))
    return " &nbsp;·&nbsp; ".join(bits)

def fill(template, data):
    batch = render_batch(data.get("batch"))
    sections = "\n\n  ".join(
        render_section(sec, i) for i, sec in enumerate(data.get("sections") or [], 1) if sec
    )
    mapping = {
        "title": esc(data.get("title") or "Recipe card"),
        "subtitle": rich(data.get("subtitle") or ""),
        "credit": render_credit(data),
        "batch": batch,
        "sections": sections,
        "aside": render_aside(data.get("aside")),
        "history": render_history(data.get("history")),
        "notes": render_notes(data),
        "footer": render_footer(data),
    }
    def repl(m):
        key = m.group(1)
        return mapping.get(key, m.group(0))
    out = re.sub(r"\{\{(title|subtitle|credit|batch|sections|aside|history|notes|footer)\}\}", repl, template)
    # Hide empty subtitle, credit, footer tags
    out = re.sub(r'<p class="subtitle">\s*</p>', "", out)
    out = re.sub(r'<p class="credit">\s*</p>', "", out)
    out = re.sub(r'<p class="links">\s*</p>', "", out)
    return out

def warn_units(data, err=sys.stderr):
    blob = json.dumps(data)
    if re.search(r"\b(cups?|ounces?|oz\.?|tbsp|tsp|tablespoons?|teaspoons?)\b", blob, re.I):
        print("note: amounts should be in grams; this recipe may still list other units.", file=err)

def find_chrome():
    env = os.environ.get("HIVE_CHROME") or os.environ.get("CHROME")
    if env and shutil.which(env):
        return env
    for name in ("google-chrome-stable", "google-chrome", "chromium-browser", "chromium", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    return None

def html_to_pdf(html_path, pdf_path):
    chrome = find_chrome()
    if not chrome:
        return False, "no browser"
    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--disable-dev-shm-usage", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and pdf_path.is_file() and pdf_path.stat().st_size > 0:
            return True, "ok"
        return False, (r.stderr or r.stdout or f"chrome exit {r.returncode}")[:240]
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, str(e)[:240]

def render_file(recipe_path, out_path, template_path=None):
    recipe_path = Path(recipe_path)
    out_path = Path(out_path)
    data = json.loads(recipe_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("recipe JSON must be an object")
    warn_units(data)
    tmpl_path = Path(template_path) if template_path else find_template()
    if not tmpl_path or not tmpl_path.is_file():
        raise SystemExit("could not find templates/recipe-card.html")
    html_out = fill(tmpl_path.read_text(encoding="utf-8"), data)
    want_pdf = out_path.suffix.lower() == ".pdf"
    html_path = out_path.with_suffix(".html") if want_pdf else out_path
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html_out, encoding="utf-8")
    if not want_pdf:
        return {"html": str(html_path), "pdf": None, "ok": True, "note": "wrote HTML"}
    ok, note = html_to_pdf(html_path, out_path)
    if ok:
        return {"html": str(html_path), "pdf": str(out_path), "ok": True, "note": "wrote PDF and HTML"}
    return {"html": str(html_path), "pdf": None, "ok": False, "note": f"saved HTML only ({note})"}

def main(argv):
    if len(argv) != 3 or argv[1] in ("-h", "--help"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    result = render_file(argv[1], argv[2])
    print(result["note"])
    print("html:", result["html"])
    if result["pdf"]:
        print("pdf:", result["pdf"])
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
