#!/usr/bin/env python3
"""AFNS static site generator. Standard library only.

Usage:  python3 build.py            -> builds ./dist
        python3 build.py --serve    -> builds, then serves dist on http://localhost:8000

Links, assets, the feed, and the sitemap follow site.json "base_url".
The URL path is the mount point: https://amclips.github.io/AFNS serves under
/AFNS/, and a later custom domain (https://example.com) serves at /.
"""
import html, json, re, shutil, sys, datetime
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parent
CONTENT, DIST, ASSETS, STATIC = ROOT / "content", ROOT / "dist", ROOT / "assets", ROOT / "static"
CFG = json.loads((ROOT / "site.json").read_text())
DESKS = {d["slug"]: d for d in CFG["desks"]}
esc = lambda s: html.escape(str(s), quote=True)

# Path prefix from base_url ("/AFNS" or "" at the host root). No trailing slash.
BASE_PATH = urlparse(CFG["base_url"]).path.rstrip("/")

def site_href(path=""):
    """Root-relative URL that includes BASE_PATH. '' -> '/AFNS/' or '/'."""
    if path.startswith(("http://", "https://", "//", "mailto:", "#")):
        return path
    if not path:
        return f"{BASE_PATH}/" if BASE_PATH else "/"
    if not path.startswith("/"):
        path = "/" + path
    if BASE_PATH and path != BASE_PATH and not path.startswith(BASE_PATH + "/"):
        path = BASE_PATH + path
    return path

def site_url(path=""):
    """Absolute URL on base_url, e.g. https://amclips.github.io/AFNS/courts/."""
    if path.startswith(("http://", "https://", "//")):
        return path
    base = CFG["base_url"].rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}" if path else f"{base}/"

# ---------------------------------------------------------------- front matter
def parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    meta, key = {}, None
    for line in fm.strip("\n").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s+-\s+(.*)$", line)
        if m and key:
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                meta[key] = []
            meta[key].append(m.group(1).strip())
            continue
        k, _, v = line.partition(":")
        key, v = k.strip(), v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1].replace('\\"', '"') if v[0] == '"' else v[1:-1]
        if v.lower() in ("true", "false"):
            v = v.lower() == "true"
        meta[key] = v if v != "" else []
    return meta, body

# ---------------------------------------------------------------- tiny markdown
def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", s)
    def link(m):
        href = m.group(2)
        ext = href.startswith(("http://", "https://", "//"))
        attrs = ' rel="noopener" target="_blank"' if ext else ""
        if href.startswith("/") and not href.startswith("//"):
            href = site_href(href)
        return f'<a href="{href}"{attrs}>{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)

def markdown(md):
    out, para, lst, quote_ = [], [], None, []
    def flush():
        nonlocal para, lst, quote_
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"<{lst[0]}>" + "".join(f"<li>{inline(i)}</li>" for i in lst[1]) + f"</{lst[0]}>"); lst = None
        if quote_: out.append("<blockquote><p>" + inline(" ".join(quote_)) + "</p></blockquote>"); quote_ = []
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush(); continue
        if m := re.match(r"^(#{2,4})\s+(.*)", line):
            flush(); n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); continue
        if re.match(r"^(-{3,}|\*{3,})$", line.strip()):
            flush(); out.append("<hr>"); continue
        if line.startswith(">"):
            if para or lst: flush()
            quote_.append(line.lstrip("> ").strip()); continue
        m_ul, m_ol = re.match(r"^\s*[-*]\s+(.*)", line), re.match(r"^\s*\d+[.)]\s+(.*)", line)
        if m_ul or m_ol:
            tag = "ul" if m_ul else "ol"
            if para or quote_ or (lst and lst[0] != tag): flush()
            if not lst: lst = (tag, [])
            lst[1].append((m_ul or m_ol).group(1)); continue
        if lst and raw.startswith("  "):
            lst[1][-1] += " " + line.strip(); continue
        if lst or quote_: flush()
        para.append(line.strip())
    flush()
    return "\n".join(out)

# ---------------------------------------------------------------- load articles
def load_articles():
    arts = []
    for f in sorted(CONTENT.glob("*/*.md")):
        if f.name.startswith("_"):
            continue
        meta, body = parse_front_matter(f.read_text(encoding="utf-8"))
        desk = meta.get("desk") or f.parent.name
        if desk not in DESKS:
            print(f"!! skipping {f}: unknown desk '{desk}'"); continue
        if meta.get("draft") is True:
            continue
        date = datetime.date.fromisoformat(str(meta.get("date", "2000-01-01"))[:10])
        sources = []
        for s in meta.get("sources", []) or []:
            title, _, url = s.rpartition("|") if "|" in s else (s, "", s)
            sources.append({"title": title.strip() or url.strip(), "url": url.strip()})
        arts.append({
            "title": meta.get("title", f.stem), "slug": meta.get("slug") or f.stem, "desk": desk,
            "date": date, "summary": meta.get("summary", ""), "byline": meta.get("byline") or CFG["byline"],
            "sample": meta.get("sample") is True, "status": meta.get("status") or "", "featured": meta.get("featured") is True,
            "desk_lead": meta.get("desk_lead") is True,
            "image": meta.get("image") or "", "image_alt": meta.get("image_alt", ""),
            "image_credit": meta.get("image_credit", ""), "image_source_url": meta.get("image_source_url", ""),
            "image_license": meta.get("image_license", ""),
            "key_points": meta.get("key_points", []) or [], "sources": sources,
            "path": f, "body": markdown(body), "words": len(re.findall(r"\w+", body)),
        })
    arts.sort(key=lambda a: (a["date"], a["featured"]), reverse=True)
    return arts

def url_of(a):  # site-relative path, no leading slash
    return f"{a['desk']}/{a['slug']}/"

def fmt_date(d):
    return d.strftime("%B %-d, %Y")

# ---------------------------------------------------------------- layout
X_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18"><path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'

def layout(title, body, *, desc=None, canonical="", og_type="website", active="", og_image=None, og_alt=None):
    full_title = f"{title} | {CFG['short_name']}" if title else f"{CFG['name']} — {CFG['tagline']}"
    desc = desc or CFG["description"]
    canon = site_url(canonical)
    if og_image:  # (site-relative path, width, height)
        img_url, img_w, img_h = site_url(og_image[0]), og_image[1], og_image[2]
    else:
        img_url, img_w, img_h = site_url("assets/og-image.jpg"), 1200, 630
    img_alt = og_alt or f"{CFG['name']} — {CFG['tagline']}"
    nav = "".join(
        f'<li><a href="{site_href(d["slug"] + "/")}"{" aria-current=\"page\"" if active == d["slug"] else ""}>{esc(d["name"])}</a></li>'
        for d in CFG["desks"])
    today = datetime.date.today().strftime("%A, %B %-d, %Y")
    xph = ' data-placeholder="true"' if CFG.get("x_is_placeholder") else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<meta property="og:site_name" content="{esc(CFG['name'])}">
<meta property="og:title" content="{esc(title or CFG['name'])}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{esc(canon)}">
<meta property="og:image" content="{esc(img_url)}">
<meta property="og:image:width" content="{img_w}">
<meta property="og:image:height" content="{img_h}">
<meta property="og:image:alt" content="{esc(img_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title or CFG['name'])}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(img_url)}">
<meta name="twitter:image:alt" content="{esc(img_alt)}">
<meta name="twitter:site" content="{esc(CFG['x_handle'])}">
<meta name="theme-color" content="#0a1630">
<link rel="icon" href="{site_href('assets/favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{site_href('assets/favicon-32.png')}">
<link rel="apple-touch-icon" href="{site_href('assets/apple-touch-icon.png')}">
<link rel="alternate" type="application/rss+xml" title="{esc(CFG['name'])}" href="{site_href('feed.xml')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{site_href('css/style.css')}">
<script src="{site_href('js/site.js')}" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap topbar-inner">
  <span class="topbar-date">{today}</span>
  <span class="topbar-tag">{esc(CFG['tagline'])}</span>
  <a class="topbar-x" href="{esc(CFG['x_url'])}" rel="noopener" target="_blank"{xph}>{X_ICON}<span>Follow {esc(CFG['x_handle'])}</span></a>
</div></div>
<header class="masthead">
  <div class="wrap masthead-inner">
    <a class="brand" href="{site_href()}" aria-label="{esc(CFG['name'])} home">
      <picture><source srcset="{site_href('assets/logo-192.webp')}" type="image/webp"><img src="{site_href('assets/logo-96.png')}" alt="" width="64" height="64"></picture>
      <span class="brand-text"><span class="brand-abbr">AFNS</span><span class="brand-name">America First News Syndicate</span></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span class="sr-only">Menu</span><span class="bars" aria-hidden="true"></span></button>
  </div>
  <nav id="site-nav" class="site-nav" aria-label="Sections"><div class="wrap"><ul>
    <li><a href="{site_href()}"{' aria-current="page"' if active == 'home' else ''}>Home</a></li>{nav}
    <li class="nav-secondary"><a href="{site_href('about/')}"{' aria-current="page"' if active == 'about' else ''}>About</a></li>
  </ul></div></nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <picture><source srcset="{site_href('assets/seal.webp')}" type="image/webp"><img src="{site_href('assets/seal.png')}" alt="America First News Syndicate seal" width="150" height="165" loading="lazy"></picture>
      <p class="footer-tag">Real News. Real America.<br>Fair. Fearless. Fact-Based.<br>For America. Not the Agenda.</p>
    </div>
    <div><h2 class="footer-h">Desks</h2><ul class="footer-links">{"".join(f'<li><a href="{site_href(d["slug"] + "/")}">{esc(d["name"])}</a></li>' for d in CFG["desks"])}</ul></div>
    <div><h2 class="footer-h">AFNS</h2><ul class="footer-links">
      <li><a href="{site_href('about/')}">About &amp; Mission</a></li>
      <li><a href="{site_href('standards/')}">Sources &amp; Corrections</a></li>
      <li><a href="{site_href('contact/')}">Contact</a></li>
      <li><a href="{site_href('feed.xml')}">RSS Feed</a></li>
      <li><a href="{esc(CFG['x_url'])}" rel="noopener" target="_blank"{xph}>X / {esc(CFG['x_handle'])}</a></li>
    </ul></div>
  </div>
  <div class="footer-bottom"><div class="wrap">&copy; {datetime.date.today().year} {esc(CFG['name'])}. America First. Truth First. America Always.</div></div>
</footer>
</body>
</html>
"""

LICENSE_URLS = {
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/", "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/", "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
}

def card(a, size=""):
    d = DESKS[a["desk"]]
    img = (f'<img src="{esc(site_href(a["image"]))}" alt="{esc(a["image_alt"])}" loading="lazy">' if a["image"]
           else f'<span class="thumb-fallback" aria-hidden="true"><span>{esc(d["name"])}</span></span>')
    sample = '<span class="badge-sample">Sample — placeholder</span>' if a["sample"] else ""
    if a["status"]: sample += f'<span class="badge-status">{esc(a["status"])}</span>'
    return f"""<article class="card {size}">
  <a class="card-thumb desk-{a['desk']}" href="{site_href(url_of(a))}" tabindex="-1" aria-hidden="true">{img}</a>
  <div class="card-body">
    <a class="desk-tag" href="{site_href(a['desk'] + '/')}">{esc(d['name'])}</a>{sample}
    <h3 class="card-title"><a href="{site_href(url_of(a))}">{esc(a['title'])}</a></h3>
    <p class="card-summary">{esc(a['summary'])}</p>
    <p class="meta"><time datetime="{a['date'].isoformat()}">{fmt_date(a['date'])}</time> · {esc(a['byline'])}</p>
  </div>
</article>"""

def x_callout():
    ph = '<p class="note">Our X account is launching soon. This link will go live once the handle is confirmed.</p>' if CFG.get("x_is_placeholder") else ""
    return f"""<section class="x-callout" aria-labelledby="x-h"><div class="wrap x-inner">
  <div class="x-icon">{X_ICON.replace('width="18" height="18"', 'width="44" height="44"')}</div>
  <div class="x-copy"><h2 id="x-h">Follow AFNS on X</h2>
  <p>Get every new research report, court ruling breakdown, and desk update as it publishes.</p>{ph}</div>
  <a class="btn btn-gold" href="{esc(CFG['x_url'])}" rel="noopener" target="_blank">Follow {esc(CFG['x_handle'])}</a>
</div></section>"""

def signup():
    return """<section class="signup" aria-labelledby="signup-h"><div class="wrap signup-inner">
  <div><p class="kicker">Coming soon</p><h2 id="signup-h">The AFNS Daily Brief</h2>
  <p>A once-a-day email with the top research from every desk. Sign-up opens soon.</p></div>
  <form class="signup-form" onsubmit="return false" aria-describedby="signup-note">
    <label for="signup-email" class="sr-only">Email address</label>
    <input id="signup-email" type="email" placeholder="you@example.com" disabled>
    <button class="btn btn-red" type="submit" disabled>Coming soon</button>
    <p id="signup-note" class="note">Email sign-up isn't live yet. No data is collected.</p>
  </form>
</div></section>"""

def section_head(title, href=None, more="More"):
    link = f'<a class="section-more" href="{href}">{more} &rarr;</a>' if href else ""
    return f'<div class="section-head"><h2>{title}</h2>{link}</div>'

# ---------------------------------------------------------------- pages
def write(rel, content):
    p = DIST / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def build_home(arts):
    lead = next((a for a in arts if a["featured"]), arts[0] if arts else None)
    # Newest featured story is the lead. Other featured stories head the side list.
    rest = [a for a in arts if a is not lead and a["featured"]] + [a for a in arts if a is not lead and not a["featured"]]
    hero = f"""<section class="hero" aria-label="America First News Syndicate">
  <div class="hero-media"><img src="{site_href('assets/hero-banner.jpg')}" alt="AFNS — America First News Syndicate. America First. Truth First. America Always." width="1168" height="784" fetchpriority="high"></div>
  <div class="hero-pillars wrap"><ul>
    <li><strong>Real News.</strong> Real America.</li>
    <li><strong>Fair.</strong> Fearless. Fact-Based.</li>
    <li><strong>For America.</strong> Not the Agenda.</li>
  </ul></div>
</section>"""
    top = ""
    if lead:
        side = "".join(card(a, "card-compact") for a in rest[:4])
        top = f"""<section class="wrap top-stories" aria-labelledby="latest-h">
  {section_head('<span id="latest-h">Latest Research</span>')}
  <div class="top-grid"><div class="lead">{card(lead, "card-lead")}</div><div class="side">{side}</div></div>
  <div class="grid-3">{"".join(card(a) for a in rest[4:7])}</div>
</section>"""
    desks = []
    for d in CFG["desks"]:
        da = [a for a in arts if a["desk"] == d["slug"]][:3]
        items = "".join(card(a, "card-compact") for a in da) or '<p class="empty">New research from this desk is coming soon.</p>'
        desks.append(f"""<section class="desk-block" aria-labelledby="desk-{d['slug']}-h">
  {section_head(f'<a id="desk-{d["slug"]}-h" href="{site_href(d["slug"] + "/")}">{esc(d["name"])}</a>', site_href(d["slug"] + "/"), "More")}
  <p class="desk-blurb">{esc(d['blurb'])}</p>
  <div class="desk-list">{items}</div>
</section>""")
    body = hero + top + x_callout() + f'<div class="wrap desks-grid">{"".join(desks)}</div>' + signup()
    write("index.html", layout("", body, active="home"))

def build_desks(arts):
    for d in CFG["desks"]:
        da = [a for a in arts if a["desk"] == d["slug"]]
        lead = next((a for a in da if a["desk_lead"]), None)
        if lead:  # desk lead story goes first, marked as the lead
            da = [lead] + [a for a in da if a is not lead]
        items = "".join(card(a, "card-row card-desk-lead" if a is lead else "card-row") for a in da) or '<p class="empty">New research from this desk is coming soon.</p>'
        body = f"""<header class="page-head desk-{d['slug']}"><div class="wrap">
  <p class="kicker">AFNS Desk</p><h1>{esc(d['name'])}</h1><p class="lede">{esc(d['blurb'])}</p></div></header>
<div class="wrap desk-page"><div class="desk-feed">{items}</div>
<aside class="sidebar">{sidebar(arts, exclude_desk=d['slug'])}</aside></div>"""
        write(f"{d['slug']}/index.html", layout(d["name"], body, desc=d["blurb"], canonical=f"{d['slug']}/", active=d["slug"]))

def sidebar(arts, exclude_desk=None, exclude=None):
    others = [a for a in arts if a["desk"] != exclude_desk and a is not exclude][:5]
    lis = "".join(f'<li><a href="{site_href(url_of(a))}"><span class="desk-tag-sm">{esc(DESKS[a["desk"]]["name"])}</span>{esc(a["title"])}</a></li>' for a in others)
    return f"""<div class="side-box"><h2 class="side-h">Across the Desks</h2><ol class="side-list">{lis}</ol></div>
<div class="side-box side-x"><h2 class="side-h">Follow AFNS</h2><p>New research posts to X first.</p>
<a class="btn btn-gold btn-block" href="{esc(CFG['x_url'])}" rel="noopener" target="_blank">{X_ICON} Follow {esc(CFG['x_handle'])}</a></div>"""

def build_articles(arts):
    for a in arts:
        d = DESKS[a["desk"]]
        canon = site_url(url_of(a))
        share_text = f"{a['title']} — via {CFG['x_handle']}"
        share = f"https://x.com/intent/post?text={quote(share_text)}&url={quote(canon, safe='')}"
        sample = ('<div class="sample-banner" role="note"><strong>Sample article — placeholder.</strong> '
                  'This page demonstrates the article layout. It is not real reporting.</div>') if a["sample"] else ""
        kp = "".join(f"<li>{inline(k)}</li>" for k in a["key_points"])
        summary = f"""<aside class="summary-box" aria-label="Summary"><h2>Summary</h2><p>{esc(a['summary'])}</p>{f'<ul>{kp}</ul>' if kp else ''}</aside>"""
        srcs = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["title"])}</a> <span class="src-url">{esc(re.sub(r"^https?://(www\\.)?", "", s["url"]).split("/")[0])}</span></li>' for s in a["sources"])
        sources = f'<section class="sources" aria-labelledby="src-h"><h2 id="src-h">Sources</h2><ol>{srcs}</ol><p class="note">See our <a href="{site_href("standards/")}">sourcing &amp; corrections standards</a>.</p></section>' if srcs else ""
        mins = max(1, round(a["words"] / 230))
        og = OG_CARDS.get(a["slug"])
        if a["image"]:
            credit = ""
            if a["image_credit"]:
                lic = a["image_license"]
                lic_url = LICENSE_URLS.get(lic)
                lic_html = f'<a href="{esc(lic_url)}" rel="license noopener" target="_blank">{esc(lic)}</a>' if lic_url else esc(lic)
                who = f'<a href="{esc(a["image_source_url"])}" rel="noopener" target="_blank">{esc(a["image_credit"])}</a>' if a["image_source_url"] else esc(a["image_credit"])
                credit = f'<figcaption class="photo-credit">Photo: {who}{", " + lic_html if lic else ""}{" (cropped)" if lic.startswith("CC BY") else ""}</figcaption>'
            hero = f'<figure class="article-hero"><img src="{esc(site_href(a["image"]))}" alt="{esc(a["image_alt"])}" width="1200" height="675" fetchpriority="high">{credit}</figure>'
        elif og:
            hero = f'<figure class="article-hero"><img src="{site_href(og)}" alt="{esc(a["title"])}: {esc(d["name"])}, AFNS share card" width="1200" height="675" fetchpriority="high"></figure>'
        else:
            hero = ""
        # Branded share card stays the link-preview image. JSON-LD below uses the photo.
        og_meta = (og, 1200, 675) if og else ((a["image"], 1200, 675) if a["image"] else None)
        related = [x for x in arts if x["desk"] == a["desk"] and x is not a][:3]
        rel_html = f'<section class="wrap related">{section_head("More from " + esc(d["name"]), site_href(a["desk"] + "/"), "All")}<div class="grid-3">{"".join(card(x) for x in related)}</div></section>' if related else ""
        share_image = a["image"] or og or "assets/og-image.jpg"
        ld = json.dumps({"@context": "https://schema.org", "@type": "NewsArticle", "headline": a["title"],
                         "datePublished": a["date"].isoformat(), "author": {"@type": "Organization", "name": a["byline"]},
                         "image": site_url(share_image),
                         "publisher": {"@type": "Organization", "name": CFG["name"], "logo": {"@type": "ImageObject", "url": site_url("assets/logo-512.png")}},
                         "articleSection": d["name"], "description": a["summary"], "mainEntityOfPage": canon})
        body = f"""<div class="wrap article-layout">
<article class="article">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{site_href()}">Home</a> / <a href="{site_href(a['desk'] + '/')}">{esc(d['name'])}</a></nav>
  {sample}
  <a class="desk-tag" href="{site_href(a['desk'] + '/')}">{esc(d['name'])}</a>{f' <span class="badge-status">Status: {esc(a["status"])}</span>' if a["status"] else ""}
  <h1 class="headline">{esc(a['title'])}</h1>
  <div class="byline-row">
    <p class="meta"><span class="byline">By {esc(a['byline'])}</span> · <time datetime="{a['date'].isoformat()}">{fmt_date(a['date'])}</time> · {mins} min read</p>
    <div class="share"><a class="btn btn-x" href="{esc(share)}" rel="noopener" target="_blank">{X_ICON} Share on X</a>
    <button class="btn btn-ghost copy-link" type="button" data-url="{esc(canon)}">Copy link</button></div>
  </div>
  {hero}
  {summary}
  <div class="prose">{a['body']}</div>
  {sources}
  <div class="article-foot"><a class="btn btn-x" href="{esc(share)}" rel="noopener" target="_blank">{X_ICON} Share on X</a>
  <p class="note">Spotted an error? <a href="{site_href('contact/')}">Tell us</a> — see our <a href="{site_href('standards/')}">corrections policy</a>.</p></div>
</article>
<aside class="sidebar">{sidebar(arts, exclude=a)}</aside>
</div>
{rel_html}
<script type="application/ld+json">{ld}</script>"""
        write(f"{url_of(a)}index.html", layout(a["title"], body, desc=a["summary"], canonical=url_of(a), og_type="article", active=a["desk"],
                                                 og_image=og_meta, og_alt=f'{a["title"]} | {d["name"]} | {CFG["short_name"]}'))

def static_page(slug, title, inner, desc, wide=False):
    body = f"""<header class="page-head"><div class="wrap"><p class="kicker">AFNS</p><h1>{title}</h1></div></header>
<div class="wrap static-page{' wide' if wide else ''}">{inner}</div>"""
    write(f"{slug}/index.html", layout(title, body, desc=desc, canonical=f"{slug}/", active=slug))

def build_static():
    desks_li = "".join(f'<li><a href="{site_href(d["slug"] + "/")}"><strong>{esc(d["name"])}</strong></a> — {esc(d["blurb"])}</li>' for d in CFG["desks"])
    static_page("about", "About AFNS", f"""
<div class="about-grid"><div class="prose">
<p class="lede">America First News Syndicate is an independent research and news outlet built on one principle: <strong>America First. Truth First. America Always.</strong></p>
<h2>Our mission</h2>
<p><strong>Real News. Real America.</strong> We publish research on the stories that matter to working Americans: the decisions coming out of our courts, how public money is spent, what Washington is actually doing, and how events abroad affect us at home.</p>
<p><strong>Fair. Fearless. Fact-Based.</strong> Every report is tied to its sources. We link to the court opinions, government filings, official records, and on-the-record statements behind what we publish, so readers can check the work themselves.</p>
<p><strong>For America. Not the Agenda.</strong> We report what the record shows, and we correct ourselves openly when we get something wrong.</p>
<h2>Our desks</h2><ul>{desks_li}</ul>
<h2>How we work</h2>
<p>AFNS research is compiled by the <strong>AFNS Research Desk</strong> using research tools and reviewed before publication. Read our <a href="{site_href('standards/')}">sourcing and corrections standards</a>.</p>
</div><div class="about-seal"><picture><source srcset="{site_href('assets/seal.webp')}" type="image/webp"><img src="{site_href('assets/seal.png')}" alt="America First News Syndicate seal" width="382" height="420"></picture></div></div>""",
        "About America First News Syndicate: our mission, desks, and how we work.")
    static_page("standards", "Sources &amp; Corrections", f"""<div class="prose">
<h2>Sourcing standards</h2>
<ul>
<li><strong>Primary sources first.</strong> We link to court opinions, dockets, government reports, official statements, and data wherever they exist.</li>
<li><strong>Every article lists its sources</strong> at the bottom of the page so readers can verify claims.</li>
<li><strong>Facts and analysis are labeled.</strong> Summaries state what the record shows. Analysis and opinion are marked as such.</li>
<li><strong>Anonymous claims are not treated as fact.</strong> When something is unconfirmed, we say so.</li>
</ul>
<h2>Corrections policy</h2>
<p>When we get something wrong, we fix it and say so. Corrected articles carry a dated note at the bottom describing what changed. Typos and formatting fixes may be made without a note.</p>
<p>To request a correction, use our <a href="{site_href('contact/')}">contact page</a> and include the article link and the source that shows the error.</p>
<h2>Research tools</h2>
<p>AFNS uses automated research tools to gather and organize public records. Material is reviewed before it is published under the AFNS Research Desk byline.</p>
</div>""", "AFNS sourcing standards and corrections policy.")
    static_page("contact", "Contact AFNS", f"""<div class="contact-grid"><div class="prose">
<p class="lede">Tips, corrections, and questions are welcome.</p>
<p><strong>Corrections:</strong> include the article link and the source showing the error.<br><strong>Tips:</strong> documents and primary sources help us move fastest.</p>
<p><strong>Email:</strong> <span class="placeholder-text">{esc(CFG['contact_email'])}</span> <em>(placeholder, not monitored yet)</em></p>
<p><strong>X:</strong> <a href="{esc(CFG['x_url'])}" rel="noopener" target="_blank">{esc(CFG['x_handle'])}</a></p>
</div>
<form class="contact-form" onsubmit="return false" aria-describedby="contact-note">
  <p class="kicker">Contact form · Coming soon</p>
  <label for="c-name">Name</label><input id="c-name" type="text" disabled>
  <label for="c-email">Email</label><input id="c-email" type="email" placeholder="you@example.com" disabled>
  <label for="c-msg">Message</label><textarea id="c-msg" rows="5" disabled></textarea>
  <button class="btn btn-red" type="submit" disabled>Coming soon</button>
  <p id="contact-note" class="note">This form isn't connected yet. No data is collected.</p>
</form></div>""", "Contact America First News Syndicate.")
    home = site_href()
    write("404.html", layout("Page not found", f"""<header class="page-head"><div class="wrap"><p class="kicker">404</p><h1>Page not found</h1>
<p class="lede">That page doesn't exist. <a href="{home}">Return to the homepage</a>.</p></div></header>"""))

def build_feeds(arts):
    items = "".join(f"""<item><title>{esc(a['title'])}</title><link>{site_url(url_of(a))}</link><guid>{site_url(url_of(a))}</guid>
<pubDate>{datetime.datetime.combine(a['date'], datetime.time(12)).strftime('%a, %d %b %Y %H:%M:%S -0500')}</pubDate>
<category>{esc(DESKS[a['desk']]['name'])}</category><description>{esc(a['summary'])}</description></item>""" for a in arts[:50])
    write("feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(CFG['name'])}</title>
<link>{site_url()}</link><description>{esc(CFG['description'])}</description><language>en-us</language>{items}</channel></rss>""")
    urls = [""] + [f"{d['slug']}/" for d in CFG["desks"]] + ["about/", "standards/", "contact/"] + [url_of(a) for a in arts]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{site_url(u)}</loc></url>" for u in urls) + "</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {site_url('sitemap.xml')}\n")

OG_CARDS = {}  # slug -> site-relative path, e.g. og/<slug>.png

def build_og_cards(arts):
    """Publish static/og/<slug>.png for every non-sample article.

    Story photos do not replace the branded card. Committed cards are used as-is when
    Pillow is not installed. When it is, a card is redrawn only if it is older than
    the article, site.json, or tools/og_cards.py.
    """
    OG_CARDS.clear()
    og_mod = None
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import og_cards as og_mod
    except ImportError as e:
        print(f"!! share cards not regenerated (needs Pillow: pip install pillow): {e}")
    gen_mtime = 0
    if og_mod is not None:
        gen_mtime = max(Path(og_mod.__file__).stat().st_mtime, (ROOT / "site.json").stat().st_mtime)
    made = 0
    for a in arts:
        if a["sample"]:
            continue
        out = STATIC / "og" / f"{a['slug']}.png"
        if og_mod is not None:
            src_mtime = a["path"].stat().st_mtime if a.get("path") else 0
            if not out.exists() or out.stat().st_mtime < max(src_mtime, gen_mtime):
                og_mod.make_card(a["title"], DESKS[a["desk"]]["name"], a["status"], out)
                made += 1
        if out.exists():
            OG_CARDS[a["slug"]] = f"og/{a['slug']}.png"
        else:
            print(f"!! no share card for {a['slug']}")
    print(f"Share cards: {len(OG_CARDS)} ({made} regenerated)")

def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    arts = load_articles()
    build_og_cards(arts)
    shutil.copytree(ASSETS, DIST / "assets")
    shutil.copytree(STATIC, DIST, dirs_exist_ok=True)
    build_home(arts); build_desks(arts); build_articles(arts); build_static(); build_feeds(arts)
    print(f"Built {len(arts)} articles across {len(DESKS)} desks -> {DIST} ({site_url()})")
    if "--serve" in sys.argv:
        import functools, http.server, tempfile
        if BASE_PATH:
            mount = Path(tempfile.mkdtemp(prefix="afns-serve-"))
            dest = mount.joinpath(*BASE_PATH.strip("/").split("/"))
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(DIST, target_is_directory=True)
            directory, url = mount, f"http://localhost:8000{BASE_PATH}/"
        else:
            directory, url = DIST, "http://localhost:8000/"
        h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
        print(f"Serving on {url}")
        http.server.ThreadingHTTPServer(("", 8000), h).serve_forever()

if __name__ == "__main__":
    main()
