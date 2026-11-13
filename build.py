#!/usr/bin/env python3
"""Static site generator for the official website of Muhammad Salim Daqiq.
Run:  python3 tools/build.py   (writes HTML, sitemap, robots, manifest into the site root)
Content here is limited to verified information supplied by the family. Do not add
unverified figures, partners or qualifications. No Master's-level qualification is shown by design.
"""
import json, os, random, math, html as H
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "out")) if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == "tools" and os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "out")) else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = os.environ.get("SITE_URL", "https://muhammadsalimdaqiq.github.io").rstrip("/")
PORTRAIT = "assets/images/profile/portrait.svg"     # replace with portrait.jpg when the original photograph is supplied
PORTRAIT_IS_PLACEHOLDER = PORTRAIT.endswith(".svg")
EMAIL = "info@daqiq.af"
DI_URL = "https://daqiq.af"
CM_URL = "https://thechangemakers.daqiq.af"
TODAY = date.today().isoformat()
NAME = "Muhammad Salim Daqiq"

# ---------------------------------------------------------------- icons
I = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "down": '<path d="M12 4v12M6 11l6 6 6-6M5 20h14"/>',
 "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
 "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
 "ship": '<path d="M3 17l2 3h14l2-3M5 17V11l7-3 7 3v6M12 8V3M9 5h6"/>',
 "search": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
 "wheat": '<path d="M12 21V9M12 9c-3 0-4-3-4-5 2 0 4 1 4 5zm0 0c3 0 4-3 4-5-2 0-4 1-4 5zm0 5c-3 0-4-3-4-5 2 0 4 1 4 5zm0 0c3 0 4-3 4-5-2 0-4 1-4 5z"/>',
 "apple": '<path d="M12 7c-2-2-7-1.5-7 4 0 4 3 9 5 9 1 0 1.3-.5 2-.5s1 .5 2 .5c2 0 5-5 5-9 0-5.5-5-6-7-4zM12 7c0-2 1-4 3-4"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
 "boxes": '<path d="M3 8l9-5 9 5-9 5-9-5zM3 8v8l9 5 9-5V8M12 13v8"/>',
 "hand": '<path d="M2 12l4-4 4 2 3-2 3 1 6 5-3 3-3-2-2 2-3-1-2 2-3-2-3 1z"/>',
 "chart": '<path d="M4 20V4M4 20h16M8 16l4-5 3 3 5-7"/>',
 "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 6a3 3 0 0 0 6 0L5 7zm14 0l-3 6a3 3 0 0 0 6 0l-3-6z"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
 "woman": '<circle cx="12" cy="7" r="4"/><path d="M5 21a7 7 0 0 1 14 0M12 11v4"/>',
 "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5zM4 19a2 2 0 0 1 2-2h13"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
 "home": '<path d="M3 11l9-7 9 7M5 9v11h14V9M10 20v-6h4v6"/>',
 "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 "tool": '<path d="M14 6a4 4 0 0 0 5 5l-9 9a2 2 0 0 1-3-3l9-9a4 4 0 0 0-2-2z"/>',
 "coins": '<ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v5c0 1.7 2.7 3 6 3s6-1.3 6-3V7M9 15v2c0 1.7 2.7 3 6 3s6-1.3 6-3v-5c0-1.6-2.4-2.9-5.5-3"/>',
 "heart": '<path d="M12 20s-8-4.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6.5-8 11-8 11z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "pin": '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
 "check": '<path d="M5 12l5 5 9-10"/>',
 "doc": '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6"/>',
 "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "layers": '<path d="M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5M3 17l9 5 9-5"/>',
}
def ic(n, cls=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{(" class=%s" % cls) if cls else ""}>{I[n]}</svg>'

MARK = ('<svg class="{cls}" viewBox="0 0 48 48" fill="none" aria-hidden="true">'
        '<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="48" y2="48"><stop offset="0" stop-color="#9c7a3a"/><stop offset=".45" stop-color="#f3e4bd"/><stop offset="1" stop-color="#c9a45c"/></linearGradient></defs>'
        '<circle cx="24" cy="24" r="22.5" stroke="url(#g{uid})" stroke-width="1"/>'
        '<path d="M17 13v22M17 13h6.5a11 11 0 0 1 0 22H17" stroke="url(#g{uid})" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M24 9.5l1.4 1.4L24 12.3l-1.4-1.4z" fill="#e6d3a3"/></svg>')
_uid = [0]
def mark(cls="brand-mark"):
    _uid[0] += 1
    return MARK.format(cls=cls, uid=_uid[0])

# ---------------------------------------------------------------- generative art (no stock imagery)
def art(kind, w=600, h=600, seed=1, cls="art"):
    r = random.Random(seed)
    g = [f'<svg class="{cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">',
         f'<defs><radialGradient id="rg{seed}" cx="70%" cy="20%" r="80%"><stop offset="0" stop-color="#e6d3a3" stop-opacity=".35"/><stop offset="1" stop-color="#070d1c" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="lg{seed}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9c7a3a"/><stop offset=".5" stop-color="#f3e4bd"/><stop offset="1" stop-color="#c9a45c"/></linearGradient></defs>',
         f'<rect width="{w}" height="{h}" fill="url(#rg{seed})"/>']
    cx, cy = w * .72, h * .28
    if kind == "identity":
        for i in range(14):
            rr = 40 + i * 30
            g.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr}" fill="none" stroke="url(#lg{seed})" stroke-opacity="{.5 - i*.03:.2f}" stroke-width="{1.2 if i%3==0 else .6}" stroke-dasharray="{"2 7" if i%2 else "none"}"/>')
        for i in range(5):
            a = r.uniform(0, 6.28); rr = 70 + r.randint(0, 9) * 30
            g.append(f'<circle cx="{cx+math.cos(a)*rr:.0f}" cy="{cy+math.sin(a)*rr:.0f}" r="3" fill="#f3e4bd"/>')
    elif kind == "enterprise":
        for i in range(-12, 24):
            x = i * 34
            g.append(f'<path d="M{x} {h} Q {x+w*.35:.0f} {h*.45:.0f} {x+w*.9:.0f} 0" fill="none" stroke="#b8c0cc" stroke-opacity="{.06 + (i%4==0)*.18:.2f}" stroke-width=".8"/>')
        for i in range(9):
            y = h * (i + 1) / 10
            g.append(f'<line x1="0" y1="{y:.0f}" x2="{w}" y2="{y:.0f}" stroke="#b8c0cc" stroke-opacity=".06"/>')
        pts = [(r.uniform(w*.2, w*.95), r.uniform(h*.08, h*.6)) for _ in range(9)]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            g.append(f'<path d="M{x1:.0f} {y1:.0f} Q {(x1+x2)/2:.0f} {min(y1,y2)-60:.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="url(#lg{seed})" stroke-opacity=".7" stroke-width="1"/>')
        for x, y in pts:
            g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.2" fill="#e6d3a3"/><circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="none" stroke="#e6d3a3" stroke-opacity=".35"/>')
    elif kind == "impact":
        for ring in range(1, 11):
            n = ring * 9; rr = ring * 34
            for k in range(n):
                a = k / n * 6.283 + ring * .3
                x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
                if -10 < x < w + 10 and -10 < y < h + 10:
                    g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{2.6 - ring*.15:.1f}" fill="#f3e4bd" fill-opacity="{.85 - ring*.07:.2f}"/>')
        g.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="url(#lg{seed})"/>')
    elif kind == "learning":
        for i in range(16):
            y = h * .1 + i * 26
            g.append(f'<line x1="{w*.35:.0f}" y1="{y:.0f}" x2="{w*.35 + r.uniform(.2,.6)*w:.0f}" y2="{y:.0f}" stroke="url(#lg{seed})" stroke-opacity="{r.uniform(.15,.6):.2f}" stroke-width="1.4" stroke-linecap="round"/>')
    elif kind == "harvest":
        for i in range(26):
            x = w * .3 + i * 18; top = h * r.uniform(.12, .4)
            g.append(f'<path d="M{x:.0f} {h} C {x-10:.0f} {h*.7:.0f} {x+14:.0f} {top+60:.0f} {x+4:.0f} {top:.0f}" fill="none" stroke="url(#lg{seed})" stroke-opacity="{r.uniform(.25,.75):.2f}" stroke-width="1.1"/>')
            g.append(f'<ellipse cx="{x+4:.0f}" cy="{top:.0f}" rx="3" ry="7" fill="#e6d3a3" fill-opacity=".7"/>')
    elif kind == "care":
        for i in range(7):
            rr = 30 + i * 36
            g.append(f'<path d="M{cx-rr:.0f} {cy:.0f} a{rr} {rr} 0 0 0 {2*rr} 0" fill="none" stroke="url(#lg{seed})" stroke-opacity="{.7-i*.08:.2f}" stroke-width="1"/>')
        g.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="6" fill="#f3e4bd"/>')
    g.append("</svg>")
    return "".join(g)

# ---------------------------------------------------------------- shell
NAV = [("about.html", "About"), ("experience.html", "Experience"), ("education.html", "Education"), ("leadership.html", "Leadership"),
       ("daqiq-international.html", "DAQIQ International"), ("the-changemakers.html", "The Changemakers"), ("projects.html", "Projects"),
       ("media.html", "Media"), ("contact.html", "Contact")]

PERSON = {
 "@context": "https://schema.org", "@type": "Person", "@id": BASE + "/#person",
 "name": NAME, "alternateName": "DAQIQ", "url": BASE + "/",
 "image": BASE + "/assets/images/og/og-default.png",
 "jobTitle": "Founder & Executive Leader",
 "description": "International entrepreneur, organizational founder and development professional working at the intersection of international business, institutional leadership and social transformation.",
 "nationality": {"@type": "Country", "name": "Afghanistan"},
 "alumniOf": [{"@type": "CollegeOrUniversity", "name": "University of Kandahar"}],
 "knowsLanguage": ["English", "Persian (Dari)", "Turkish", "Hindi"],
 "founder": [{"@id": BASE + "/daqiq-international.html#org"}, {"@id": BASE + "/the-changemakers.html#org"}],
 "email": "mailto:" + EMAIL,
}
ORG_DI = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/daqiq-international.html#org", "name": "DAQIQ INTERNATIONAL",
          "url": DI_URL, "email": EMAIL, "founder": {"@id": BASE + "/#person"},
          "description": "International trading initiative focused on import and export, global sourcing, agricultural commodities, food products, industrial supplies and wholesale distribution."}
ORG_CM = {"@context": "https://schema.org", "@type": "NGO", "@id": BASE + "/the-changemakers.html#org", "name": "The Changemakers",
          "alternateName": ["Change in Youths Social Assembly", "+CYSA", "CYSA"], "foundingDate": "2015",
          "foundingLocation": {"@type": "Place", "name": "Kandahar, Afghanistan"}, "founder": {"@id": BASE + "/#person"},
          "description": "Afghanistan-based civil society organization founded in 2015 as Change in Youths Social Assembly (+CYSA), working for education, women's empowerment, youth development and community well-being."}

def head(page, title, desc, extra_ld=None, og="og-default.png"):
    url = BASE + "/" + ("" if page == "index.html" else page)
    lds = [PERSON] + (extra_ld or [])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<meta name="author" content="{NAME}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#070d1c">
<meta property="og:type" content="{'profile' if page == 'index.html' else 'website'}">
<meta property="og:site_name" content="{NAME} — Official Website">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/images/og/{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME} — Building enterprises. Empowering communities. Creating opportunities.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{H.escape(title)}">
<meta name="twitter:description" content="{H.escape(desc)}">
<meta name="twitter:image" content="{BASE}/assets/images/og/{og}">
<link rel="icon" href="assets/icons/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
<link rel="manifest" href="manifest.json">
<link rel="preload" href="assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/animations.css">
<link rel="stylesheet" href="assets/css/responsive.css">
<script>document.documentElement.classList.replace('no-js','js')</script>
{ld}
</head>
'''

def header(page):
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == page else ""}>{t}</a>' for h, t in NAV)
    mob = "".join(f'<a href="{h}"{" aria-current=page" if h == page else ""}><small>{i+1:02d}</small>{t}</a>' for i, (h, t) in enumerate([("index.html", "Home")] + NAV + [("download-profile.html", "Download Profile")]))
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="header" role="banner">
 <div class="wrap">
  <a class="brand" href="index.html" aria-label="{NAME} — home">{mark()}<span>DAQIQ<small>MUHAMMAD SALIM DAQIQ</small></span></a>
  <nav class="nav" aria-label="Primary">{links}<a class="btn btn-gold" href="download-profile.html">Profile {ic("down")}</a></nav>
  <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button>
 </div>
</header>
<nav class="mobile-menu" id="mobile-menu" aria-label="Mobile" aria-hidden="true">{mob}</nav>
'''

def footer():
    return f'''<footer class="footer" role="contentinfo">
 <div class="wrap">
  <div class="footer-sign" aria-hidden="true">Muhammad Salim Daqiq</div>
  <div class="footer-top">
   <div><a class="brand" href="index.html">{mark()}<span>DAQIQ<small>OFFICIAL WEBSITE</small></span></a>
    <p class="muted small" style="margin-top:20px;max-width:34ch">Building enterprises. Empowering communities. Creating opportunities.</p></div>
   <div><p class="footer-h">Profile</p><ul><li><a href="about.html">About</a></li><li><a href="experience.html">Experience</a></li><li><a href="education.html">Education</a></li><li><a href="leadership.html">Leadership</a></li></ul></div>
   <div><p class="footer-h">Initiatives</p><ul><li><a href="daqiq-international.html">DAQIQ International</a></li><li><a href="the-changemakers.html">The Changemakers</a></li><li><a href="projects.html">Projects</a></li><li><a href="media.html">Media &amp; Publications</a></li></ul></div>
   <div><p class="footer-h">Connect</p><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{DI_URL}" rel="noopener" target="_blank">daqiq.af</a></li><li><a href="contact.html">Contact</a></li><li><a href="download-profile.html">Download profile</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>&copy; <span data-year>{date.today().year}</span> {NAME}. All rights reserved.</span><span>Official personal website</span></div>
 </div>
</footer>
<button class="to-top" aria-label="Back to top">{ic("up")}</button>
<script src="assets/js/navigation.js" defer></script>
<script src="assets/js/interactions.js" defer></script>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''

def page_hero(crumb, eyebrow, title, lead, kind="identity", seed=3):
    return f'''<section class="page-hero">
 <div class="bg-art" data-parallax=".08">{art(kind, 760, 760, seed, "")}</div>
 <div class="wrap">
  <p class="crumbs" data-reveal><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</p>
  <h1 class="display" data-reveal style="--d:.08s">{title}</h1>
  <p class="eyebrow" data-reveal style="--d:.16s">{eyebrow}</p>
  <p class="lead" data-reveal style="--d:.22s;margin-top:22px">{lead}</p>
 </div>
</section>'''

def cta(title="Let’s build what comes next.", text="For business inquiries, institutional partnerships and collaboration.", primary=("contact.html", "Let’s connect"), secondary=("download-profile.html", "Download profile")):
    return f'''<section class="section" style="padding-top:40px"><div class="wrap"><div class="cta-band" data-reveal="scale">
  <span class="eyebrow">Collaboration</span><h2 class="h2">{title}</h2><p class="lead" style="margin:0 auto">{text}</p>
  <div class="hero-cta" style="justify-content:center"><a class="btn btn-gold" href="{primary[0]}">{primary[1]} {ic("arrow")}</a><a class="btn btn-ghost" href="{secondary[0]}">{secondary[1]} {ic("down")}</a></div>
 </div></div></section>'''

def card(icon, title, text, d=0, tilt=True):
    return f'<article class="card"{" data-tilt" if tilt else ""} data-reveal style="--d:{d:.2f}s"><div class="ico">{ic(icon)}</div><h3 class="h3">{title}</h3><p>{text}</p></article>'

def portrait(cls=""):
    tag = "<span><b>Muhammad Salim Daqiq</b>Founder &middot; Executive Leader</span>"
    return f'''<div class="portrait-wrap {cls}"><figure class="portrait" data-tilt="5" style="margin:0">
 <img src="{PORTRAIT}" alt="Portrait of Muhammad Salim Daqiq" width="800" height="1000" loading="eager" decoding="async">
 <figcaption class="portrait-tag">{tag}<span>DAQIQ</span></figcaption></figure></div>'''

def write(page, body):
    with open(os.path.join(ROOT, page), "w", encoding="utf-8") as f:
        f.write(body)

# ================================================================= CONTENT
EXPERIENCE = [
 dict(date="2015 — Present", title="Founder & Organizational Leader", org="The Changemakers &middot; Change in Youths Social Assembly (+CYSA)",
      text="Founded a youth-led civil society initiative in Kandahar in 2015, formally registered in 2018, and guided its adaptation into The Changemakers after August 2021.",
      resp=["Set the organization’s mission across human rights, youth leadership, women’s empowerment, girls’ education and community development",
            "Built a volunteer-driven institution and its working relationships with community elders, women-led groups and local authorities",
            "Led community programmes in education, hygiene and health promotion, and outreach to nomadic and vulnerable families",
            "Now leading institutional renewal: governance, partnerships and a women’s economic-empowerment initiative in development"],
      tags=["Institution building", "Human rights", "Youth leadership", "Women’s empowerment"]),
 dict(date="Founder", title="Founder & Executive Leader", org="DAQIQ INTERNATIONAL",
      text="Leads an international trading initiative focused on import and export, global sourcing, agricultural and food products, industrial supplies and wholesale distribution.",
      resp=["Sets commercial direction, partnership strategy and business development",
            "Builds sourcing relationships and the company’s professional standards for due diligence and compliance",
            "Represents the company to prospective partners, suppliers and buyers"],
      tags=["International trade", "Global sourcing", "Business development"]),
 dict(date="May 2025 — Present", title="Psychosocial Support Counsellor", org="MMRCA",
      text="Provides psychosocial support with a beneficiary-centred, dignity-first approach, working within the organization’s procedures and referral arrangements.",
      resp=["Beneficiary-centred communication and active listening",
            "Community engagement and awareness on psychosocial well-being",
            "Respect for confidentiality, dignity and safeguarding standards",
            "Coordination and referral with colleagues and partner services where appropriate"],
      tags=["Psychosocial support", "Community engagement", "Human dignity"]),
 dict(date="Jul 2024 — Apr 2025", title="Executive Officer & Secretary", org="Kandahar Directorate of Public Health",
      text="Supported the directorate’s leadership through executive coordination, institutional administration and official communication.",
      resp=["Executive coordination and scheduling for senior leadership",
            "Drafting, tracking and filing of official correspondence",
            "Documentation, records management and administrative support",
            "Liaison between offices, departments and external stakeholders"],
      tags=["Executive coordination", "Administration", "Official communication"]),
 dict(date="Nov 2021 — May 2024", title="Logistics Assistant", org="World Food Programme (WFP)",
      text="Supported humanitarian logistics operations, contributing to the movement of assistance with accuracy, documentation and accountability.",
      resp=["Operational coordination of logistics activities",
            "Supply-chain support, including tracking of consignments and stock",
            "Preparation and control of logistics documentation",
            "Reporting and data accuracy in line with accountability standards"],
      tags=["Humanitarian logistics", "Supply chain", "Reporting", "Accountability"]),
 dict(date="Educational entrepreneurship", title="Founder & Co-Founder", org="English-Language and Computer-Training Academies",
      text="Founded and helped develop more than five academies in southern Afghanistan offering English-language learning and computer training to young people.",
      resp=["Opened access to English-language learning and digital literacy",
            "Developed courses that improve youth employability and confidence",
            "Built teams of instructors and the administration behind them"],
      tags=["Education access", "Digital literacy", "Youth skills"]),
]

EDUCATION = [
 ("Bachelor of Science", "Agricultural Science", "University of Kandahar", "2013 — 2017", "Undergraduate degree"),
 ("Diploma", "Business Administration", "Sherzai Institute", "2017 — 2018", "Professional diploma"),
 ("Diploma", "Computer &amp; Information Technology", "Afghan Educational Foundation", "", "Professional diploma"),
 ("Baccalaureate", "Secondary Education", "Ahmad Shah Baba Educational Center", "", "Secondary qualification"),
]

DI_AREAS = [("ship", "International import &amp; export", "Moving goods across borders through reliable partners and compliant trade processes."),
 ("search", "Global sourcing", "Identifying, comparing and verifying suppliers that meet the buyer’s specification, price and quality needs."),
 ("wheat", "Agricultural commodities", "Trade in agricultural commodities, grounded in the founder’s training in agricultural science."),
 ("apple", "Food &amp; agricultural products", "Processed and fresh food products, with attention to quality, packaging and handling."),
 ("gear", "Industrial supplies", "Equipment, machinery and industrial inputs for businesses and producers."),
 ("boxes", "Wholesale distribution", "Supplying businesses at volume through dependable distribution arrangements."),
 ("hand", "Commercial partnerships", "Long-term relationships with suppliers, buyers and service providers built on trust."),
 ("chart", "Business development", "Opening new markets and product lines through research and disciplined execution."),
 ("globe", "International trade", "Connecting Afghan and regional markets with international supply and demand.")]

CM_THEMES = [("scale", "Human rights"), ("users", "Youth leadership"), ("woman", "Women’s empowerment"), ("book", "Girls’ education"),
 ("shield", "Child protection"), ("home", "Community development"), ("link", "Social inclusion"), ("tool", "Capacity building"),
 ("coins", "Women’s economic empowerment"), ("heart", "Humanitarian &amp; development initiatives")]

BIO_25 = "Muhammad Salim Daqiq is an Afghan entrepreneur and organizational founder: Founder of DAQIQ INTERNATIONAL and of The Changemakers, formerly Change in Youths Social Assembly (+CYSA)."
BIO_60 = ("Muhammad Salim Daqiq is an entrepreneur, organizational founder and development professional from Afghanistan. He founded Change in Youths Social Assembly (+CYSA) in 2015, now The Changemakers, and leads DAQIQ INTERNATIONAL, an international trading initiative. "
          "His career includes humanitarian logistics with the World Food Programme and executive administration at the Kandahar Directorate of Public Health.")
BIO_150 = ("Muhammad Salim Daqiq is an entrepreneur, organizational founder and development professional working at the intersection of international business, institutional leadership and social transformation. "
           "In 2015 he founded Change in Youths Social Assembly (+CYSA) in Kandahar, a youth-led civil society organization that was formally registered in 2018 and works for human rights, youth leadership, women’s empowerment and girls’ education; after August 2021 it continued as The Changemakers. "
           "He is Founder and Executive Leader of DAQIQ INTERNATIONAL, an international trading initiative in import and export, global sourcing, agricultural and food products and industrial supplies. "
           "His professional experience includes humanitarian logistics with the World Food Programme (2021–2024), executive coordination at the Kandahar Directorate of Public Health (2024–2025) and psychosocial support work. "
           "He has founded more than five English-language and computer-training academies. He holds a Bachelor of Science in Agricultural Science from the University of Kandahar.")

# ================================================================= PAGES
def home():
    p = "index.html"
    chips = "".join(f'<button class="btn btn-ghost" style="padding:10px 16px;font-size:11px" data-focus="{k}" type="button" aria-describedby="globe-note"><span class="gold">{n}</span>&nbsp;{t}</button>'
                    for k, n, t in [("identity", "01", "Identity"), ("enterprise", "02", "Enterprise"), ("impact", "03", "Impact")])
    journey = [("2013–2017", "Bachelor of Science in Agricultural Science, University of Kandahar"),
               ("2015", "Founds Change in Youths Social Assembly (+CYSA) in Kandahar"),
               ("2017–2018", "Diploma in Business Administration, Sherzai Institute"),
               ("2018", "+CYSA formally registered"),
               ("2021", "+CYSA continues as The Changemakers after August 2021"),
               ("2021–2024", "Logistics Assistant, World Food Programme"),
               ("2024–2025", "Executive Officer &amp; Secretary, Kandahar Directorate of Public Health"),
               ("Today", "Leading DAQIQ INTERNATIONAL and the renewal of The Changemakers")]
    jrows = "".join(f'<div class="t-item"><div class="t-date">{d}</div><div class="t-body"><p style="color:var(--white);font-size:18px;margin:0">{t}</p></div></div>' for d, t in journey)
    body = head(p, f"{NAME} — Official Website | Entrepreneur, Founder & Executive Leader",
                f"Official website of {NAME}: founder of DAQIQ INTERNATIONAL and The Changemakers (+CYSA). International entrepreneur, executive leader and development strategist.") + header(p) + f'''
<div class="loader" aria-hidden="true"><div class="loader-inner">{mark("loader-mark")}<div class="loader-word">DAQIQ</div><div class="loader-bar"><i></i></div></div></div>
<nav class="rail" aria-label="Chapters">
 <a href="#vision"><span>Vision</span><i></i></a><a href="#journey"><span>Journey</span><i></i></a><a href="#enterprise"><span>Enterprise</span><i></i></a><a href="#impact"><span>Impact</span><i></i></a><a href="#future"><span>Future</span><i></i></a>
</nav>
<main id="main">
<section class="hero" aria-labelledby="hero-title">
 <div id="globe" data-land="assets/data/land.json" data-static="assets/images/backgrounds/globe-static.webp"></div>
 <div class="hero-vignette"></div>
 <div class="wrap">
  <div>
   <p class="hero-name" data-reveal="fade">MUHAMMAD SALIM DAQIQ</p>
   <h1 id="hero-title" class="display"><span class="line"><span>Building enterprises.</span></span><span class="line"><span><em class="gold">Empowering</em> communities.</span></span><span class="line"><span>Creating opportunities.</span></span></h1>
   <p class="hero-sub">An entrepreneur, organizational founder and development professional working at the intersection of international business, institutional leadership and social transformation.</p>
   <div class="hero-cta" data-reveal style="--d:.62s"><a class="btn btn-gold" href="#pillars">Explore my world {ic("arrow")}</a><a class="btn btn-ghost" href="contact.html">Let’s connect {ic("arrow")}</a></div>
   <div class="hero-meta" data-reveal style="--d:.75s"><span><b>Founder</b> &middot; DAQIQ International</span><span><b>Founder</b> &middot; The Changemakers</span></div>
   <div class="hero-cta" data-reveal style="margin-top:26px;gap:8px;--d:.85s">{chips}</div>
   <p id="globe-note" class="small muted" style="margin-top:12px">The globe is an illustration of a global outlook. It does not mark operating locations.</p>
  </div>
  <div data-reveal="scale" style="--d:.3s;justify-self:end;align-self:end;width:100%;max-width:340px">{portrait()}</div>
 </div>
 <div class="scroll-cue" aria-hidden="true">SCROLL<i></i></div>
</section>

<section class="section" id="pillars" aria-labelledby="pillars-title">
 <div class="wrap">
  <div class="section-head"><span class="eyebrow" data-reveal>Three pillars &middot; One purpose</span>
   <h2 id="pillars-title" class="h2" data-reveal style="--d:.08s">A person, an enterprise and an institution, built around <em class="gold">opportunity</em>.</h2></div>
  <div class="pillars">
   <a class="pillar p1" href="about.html" data-tilt="6" data-reveal>{art("identity", 600, 700, 11)}<span class="no">01</span><div><h3>Muhammad Salim Daqiq</h3><p>Personal identity, professional journey, leadership and the values behind the work.</p><span class="link">Discover the profile {ic("arrow")}</span></div></a>
   <a class="pillar p2" href="daqiq-international.html" data-tilt="6" data-reveal style="--d:.1s">{art("enterprise", 600, 700, 12)}<span class="no">02</span><div><h3>DAQIQ International</h3><p>International business, trading, global sourcing and commercial partnerships.</p><span class="link">Enter the enterprise {ic("arrow")}</span></div></a>
   <a class="pillar p3" href="the-changemakers.html" data-tilt="6" data-reveal style="--d:.2s">{art("impact", 600, 700, 13)}<span class="no">03</span><div><h3>The Changemakers</h3><p>Human rights, social development, youth leadership and women’s empowerment.</p><span class="link">See the impact {ic("arrow")}</span></div></a>
  </div>
 </div>
</section>

<section class="section" id="vision" aria-labelledby="vision-title">
 <div class="wrap" style="position:relative">
  <span class="chapter-no" aria-hidden="true">01</span>
  <div class="split">
   <div><span class="eyebrow" data-reveal>Chapter 01 &middot; The Vision</span>
    <h2 id="vision-title" class="h2" data-reveal style="--d:.08s;margin:22px 0 28px">Enterprise and social purpose are <em class="gold">one</em> ambition.</h2>
    <p class="lead" data-reveal style="--d:.16s">Salim Daqiq builds businesses and institutions with the same conviction: that opportunity, created responsibly and shared widely, changes lives. His work moves between international trade and community development, and each informs the other.</p>
    <a class="link" href="about.html" data-reveal style="--d:.24s">Read the biography {ic("arrow")}</a></div>
   <div class="quote-wrap" data-reveal="scale"><p class="quote">“Opportunity is the most practical form of dignity.”</p><span class="eyebrow">Guiding principle</span></div>
  </div>
  <div class="facts" style="margin-top:clamp(60px,8vw,110px)">
   <div class="fact" data-reveal><b>2015</b><span>Founded +CYSA</span></div>
   <div class="fact" data-reveal style="--d:.08s"><b>5+</b><span>Training academies founded</span></div>
   <div class="fact" data-reveal style="--d:.16s"><b>2½ yrs</b><span>Humanitarian logistics, WFP</span></div>
   <div class="fact" data-reveal style="--d:.24s"><b>2</b><span>Organizations founded and led</span></div>
  </div>
 </div>
</section>

<section class="section" id="journey" aria-labelledby="journey-title">
 <div class="wrap" style="position:relative">
  <span class="chapter-no" aria-hidden="true">02</span>
  <div class="section-head"><span class="eyebrow" data-reveal>Chapter 02 &middot; The Journey</span>
   <h2 id="journey-title" class="h2" data-reveal style="--d:.08s">From Kandahar’s classrooms to international operations.</h2></div>
  <div class="timeline"><span class="fill"></span>{jrows}</div>
  <div style="margin-top:56px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn btn-ghost" href="experience.html">Full experience {ic("arrow")}</a><a class="btn btn-ghost" href="education.html">Education {ic("arrow")}</a></div>
 </div>
</section>

<section class="section" id="enterprise" aria-labelledby="ent-title">
 <div class="wrap" style="position:relative">
  <span class="chapter-no" aria-hidden="true">03</span>
  <div class="split">
   <div class="card" data-reveal="scale" style="padding:0;overflow:hidden;aspect-ratio:1/1;border-radius:28px">{art("enterprise", 700, 700, 21, "")}</div>
   <div><span class="eyebrow" data-reveal>Chapter 03 &middot; The Enterprise</span>
    <h2 id="ent-title" class="h2" data-reveal style="--d:.08s;margin:22px 0 28px">DAQIQ <em class="gold">International</em></h2>
    <p class="lead" data-reveal style="--d:.16s">An international trading initiative in import and export, global sourcing, agricultural commodities, food products, industrial supplies and wholesale distribution, built on reliable partnerships.</p>
    <ul class="tags" data-reveal style="--d:.22s"><li>Import &amp; export</li><li>Global sourcing</li><li>Agricultural commodities</li><li>Industrial supplies</li><li>Wholesale distribution</li><li>Partnerships</li></ul>
    <div data-reveal style="margin-top:34px;display:flex;gap:14px;flex-wrap:wrap;--d:.3s"><a class="btn btn-gold" href="daqiq-international.html">Explore DAQIQ International {ic("arrow")}</a><a class="btn btn-ghost" href="{DI_URL}" target="_blank" rel="noopener">daqiq.af {ic("ext")}</a></div></div>
  </div>
 </div>
</section>

<section class="section" id="impact" aria-labelledby="imp-title">
 <div class="wrap" style="position:relative">
  <span class="chapter-no" aria-hidden="true">04</span>
  <div class="split">
   <div><span class="eyebrow" data-reveal>Chapter 04 &middot; The Impact</span>
    <h2 id="imp-title" class="h2" data-reveal style="--d:.08s;margin:22px 0 28px">The <em class="gold">Changemakers</em></h2>
    <p class="lead" data-reveal style="--d:.16s">Founded in Kandahar in 2015 as Change in Youths Social Assembly (+CYSA) and formally registered in 2018, the organization brought young people together for education, rights awareness and community service. After August 2021 it adapted and continued as The Changemakers.</p>
    <ul class="tags" data-reveal style="--d:.22s"><li>Human rights</li><li>Youth leadership</li><li>Women’s empowerment</li><li>Girls’ education</li><li>Child protection</li><li>Community development</li></ul>
    <div style="margin-top:34px" data-reveal><a class="btn btn-gold" href="the-changemakers.html">Explore The Changemakers {ic("arrow")}</a></div></div>
   <div class="card" data-reveal="scale" style="padding:0;overflow:hidden;aspect-ratio:1/1;border-radius:28px">{art("impact", 700, 700, 31, "")}</div>
  </div>
 </div>
</section>

<section class="section" id="future" aria-labelledby="fut-title">
 <div class="wrap" style="position:relative">
  <span class="chapter-no" aria-hidden="true">05</span>
  <div class="section-head"><span class="eyebrow" data-reveal>Chapter 05 &middot; The Future</span>
   <h2 id="fut-title" class="h2" data-reveal style="--d:.08s">Commitments for the decade ahead.</h2></div>
  <div class="grid g4">
   {card("compass", "Entrepreneurship", "Growing DAQIQ International into a trusted, compliant partner in international trade.", 0)}
   {card("spark", "Innovation", "Bringing better tools, processes and standards to businesses and institutions.", .08)}
   {card("hand", "Partnerships", "Building long-term alliances with companies, institutions and development partners.", .16)}
   {card("coins", "Sustainable opportunity", "Creating livelihoods, especially for women and young people, that last beyond any single project.", .24)}
  </div>
 </div>
</section>
{cta()}
</main>
''' + footer()
    write(p, body)

def about():
    p = "about.html"
    body = head(p, f"About {NAME} — Biography, Leadership & Vision", f"Executive biography of {NAME}: founder of DAQIQ INTERNATIONAL and The Changemakers (+CYSA), with experience in humanitarian logistics, public administration and community development.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("About", "Executive biography", "A builder of <em class='gold'>enterprises</em> and institutions.", "Entrepreneur, organizational founder and development professional working at the intersection of international business, institutional leadership and social transformation.", "identity", 41)}
<section class="section" style="padding-top:20px"><div class="wrap split top">
 <div style="position:sticky;top:110px" data-reveal="scale">{portrait()}</div>
 <div class="prose">
  <span class="eyebrow" data-reveal>Biography</span>
  <p data-reveal style="margin-top:26px">Muhammad Salim Daqiq is an Afghan entrepreneur and founder whose work spans international trade, institution building and community development. He is the Founder and Executive Leader of DAQIQ INTERNATIONAL and the founder of The Changemakers, the organization he established in 2015 as Change in Youths Social Assembly (+CYSA).</p>
  <p data-reveal>Trained in agricultural science at University of Kandahar and in business administration at the Sherzai Institute, he combines an understanding of agriculture and commodities with practical management. Early on he turned that combination toward education, founding and developing more than five English-language and computer-training academies that gave young people in southern Afghanistan access to language skills and digital literacy.</p>
  <h3 data-reveal>Founder of a youth movement</h3>
  <p data-reveal>In 2015 he brought together young volunteers in Kandahar to form +CYSA, which was formally registered in 2018. The organization worked for human rights awareness, youth leadership, women’s empowerment and girls’ education, and ran community programmes in education, hygiene and health promotion. After the changes in Afghanistan in August 2021 it adapted its identity and approach and continued as The Changemakers.</p>
  <h3 data-reveal>Operational discipline</h3>
  <p data-reveal>His professional career has given him operational and institutional depth. From 2021 to 2024 he served as a Logistics Assistant with the World Food Programme, supporting humanitarian supply chains with careful documentation, reporting and accountability. From 2024 to 2025 he was Executive Officer and Secretary at the Kandahar Directorate of Public Health, responsible for executive coordination, official communication and administration. Since 2025 he has worked in psychosocial support, with a focus on dignity and beneficiary-centred communication.</p>
  <h3 data-reveal>The enterprise</h3>
  <p data-reveal>Through DAQIQ INTERNATIONAL he is building an international trading initiative in import and export, global sourcing, agricultural and food products, industrial supplies and wholesale distribution, grounded in trust, compliance and long-term partnerships.</p>
 </div>
</div></section>
<hr class="divider">
<section class="section"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Professional identity</span><h2 class="h2" data-reveal style="--d:.08s">Five roles. <em class="gold">One</em> direction.</h2></div>
 <div class="grid g3">
  {card("globe", "International Entrepreneur", "Builds cross-border commercial relationships through DAQIQ International.", 0)}
  {card("layers", "Founder", "Founded +CYSA / The Changemakers and more than five training academies.", .06)}
  {card("compass", "Executive Leader", "Leads organizations with clear structure, accountability and direction.", .12)}
  {card("scale", "Human Rights Advocate", "Champions dignity, inclusion and equal opportunity for women and young people.", .18)}
  {card("chart", "Development Strategist", "Links livelihoods, education and institution-building into practical plans.", .24)}
  {card("heart", "Humanitarian Professional", "Experience in humanitarian logistics, public administration and psychosocial support.", .3)}
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split top">
 <div><span class="eyebrow" data-reveal>Leadership philosophy</span><h2 class="h2" data-reveal style="--d:.08s;margin-top:22px">Listen first. Build to <em class="gold">last</em>.</h2></div>
 <div class="rows">
  <div class="row" data-reveal><span class="n">I.</span><h3>Opportunity creates dignity</h3><p>The most lasting help is a skill, a job or a business that people own themselves.</p></div>
  <div class="row" data-reveal><span class="n">II.</span><h3>Communities lead</h3><p>Solutions work when the people they serve help to design and deliver them.</p></div>
  <div class="row" data-reveal><span class="n">III.</span><h3>Trust is built on records</h3><p>Accurate documentation, clear accounts and honest reporting are the base of every partnership.</p></div>
  <div class="row" data-reveal><span class="n">IV.</span><h3>Institutions outlast individuals</h3><p>Good governance and shared ownership let an organization keep its purpose through change.</p></div>
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split">
 <div><span class="eyebrow" data-reveal>Personal vision</span><p class="quote" data-reveal style="margin-top:26px;max-width:24ch">To build enterprises and institutions that open doors for the next generation of Afghan women and men.</p></div>
 <div><span class="eyebrow" data-reveal>Languages</span><div class="lang" data-reveal style="margin-top:22px"><span>English</span><span>Persian (Dari)</span><span>Turkish</span><span>Hindi</span></div>
  <p class="note" data-reveal style="margin-top:26px">Working languages as listed in his professional profile.</p></div>
</div></section>
{cta()}
</main>''' + footer()
    write(p, body)

def experience():
    p = "experience.html"
    items = ""
    for i, e in enumerate(EXPERIENCE):
        resp = "".join(f"<li>{r}</li>" for r in e["resp"])
        tags = "".join(f"<li>{t}</li>" for t in e["tags"])
        items += f'''<div class="t-item"><div class="t-date">{e["date"]}</div><div class="t-body" data-reveal>
  <h3>{e["title"]}</h3><span class="t-org">{e["org"]}</span><p>{e["text"]}</p>
  <details{" open" if i < 1 else ""}><summary>Responsibilities</summary><ul class="resp">{resp}</ul></details><ul class="tags">{tags}</ul></div></div>'''
    body = head(p, f"Experience — {NAME} | WFP, Public Health, Founder Roles", f"Professional experience of {NAME}: founder roles, World Food Programme logistics, Kandahar Directorate of Public Health and psychosocial support.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("Experience", "Professional journey", "Experience built in the <em class='gold'>field</em>.", "Humanitarian logistics, public administration, psychosocial support and more than a decade of founding and leading organizations.", "enterprise", 51)}
<section class="section" style="padding-top:20px"><div class="wrap">
 <div class="timeline"><span class="fill"></span>{items}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Core capabilities</span><h2 class="h2" data-reveal style="--d:.08s">What the experience adds up to.</h2></div>
 <div class="grid g4">
  {card("boxes", "Logistics &amp; supply chain", "Humanitarian logistics, documentation and stock and consignment tracking.", 0)}
  {card("doc", "Executive administration", "Coordination, official correspondence, records and scheduling for leadership.", .06)}
  {card("users", "Community engagement", "Mobilizing volunteers, elders and women-led groups around shared goals.", .12)}
  {card("layers", "Institution building", "Founding organizations and giving them structure, purpose and continuity.", .18)}
 </div>
</div></section>
{cta()}
</main>''' + footer()
    write(p, body)

def education():
    p = "education.html"
    seal = '<svg class="seal" viewBox="0 0 64 64" fill="none" aria-hidden="true"><circle cx="32" cy="32" r="30" stroke="#c9a45c" stroke-opacity=".6"/><circle cx="32" cy="32" r="24" stroke="#c9a45c" stroke-opacity=".35" stroke-dasharray="2 4"/><path d="M20 30l12-6 12 6-12 6-12-6zM25 33v6c4 3 10 3 14 0v-6" stroke="#e6d3a3" stroke-width="1.3" stroke-linejoin="round"/></svg>'
    cards = "".join(f'''<article class="card" data-tilt data-reveal style="--d:{i*.08:.2f}s">{seal}<span class="level">{lvl}</span><h3>{field}</h3><p class="muted">{kind}</p>
      <div class="inst"><b>{inst}</b><span>{yrs}</span></div></article>''' for i, (lvl, field, inst, yrs, kind) in enumerate(EDUCATION))
    body = head(p, f"Education — {NAME} | University of Kandahar, Business Administration, IT", f"Academic qualifications of {NAME}: BSc Agricultural Science (University of Kandahar), Diploma in Business Administration (Sherzai Institute), Diploma in Computer & IT.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("Education", "Academic qualifications", "Knowledge with <em class='gold'>purpose</em>.", "A foundation in agricultural science, business administration and information technology, the disciplines behind his work in trade, management and education.", "learning", 61)}
<section class="section" style="padding-top:20px"><div class="wrap"><div class="edu">{cards}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap split top">
 <div><span class="eyebrow" data-reveal>Professional development</span><h2 class="h2" data-reveal style="--d:.08s;margin-top:22px">Learning that <em class="gold">compounds</em>.</h2>
  <p class="lead" data-reveal style="--d:.16s;margin-top:24px">Beyond formal study, his development has come from practice: humanitarian operations, public administration and years of building organizations.</p></div>
 <div class="rows">
  <div class="row" data-reveal><span class="n">01</span><h3>Project management</h3><p>Planning, coordination and delivery of community and organizational projects.</p></div>
  <div class="row" data-reveal><span class="n">02</span><h3>Proposal writing</h3><p>Preparing project concepts and proposals for partners and donors.</p></div>
  <div class="row" data-reveal><span class="n">03</span><h3>Women’s empowerment</h3><p>Training in approaches that widen women’s participation and economic opportunity.</p></div>
  <div class="row" data-reveal><span class="n">04</span><h3>Humanitarian operations</h3><p>Logistics, documentation and accountability standards learned with the World Food Programme.</p></div>
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="cta-band" data-reveal="scale" style="text-align:left;justify-items:start">
 <span class="eyebrow">Educator</span><h2 class="h2">Founder of more than five English-language and computer-training academies.</h2>
 <p class="lead" style="margin:0">Education has been a constant thread: opening English-language learning and digital literacy to young people who would otherwise go without.</p>
 <a class="btn btn-ghost" href="leadership.html">The founder journey {ic("arrow")}</a></div></div></section>
</main>''' + footer()
    write(p, body)

def leadership():
    p = "leadership.html"
    steps = ["Listen", "Identify", "Design", "Mobilize", "Implement", "Coordinate", "Document", "Learn", "Adapt"]
    stepshtml = "".join(f'<li class="card" data-reveal style="--d:{i*.05:.2f}s;padding:22px"><span class="badge">{i+1:02d}</span><h3 class="h3" style="margin-top:14px">{s}</h3></li>' for i, s in enumerate(steps))
    journey = [("2015", "The first assembly", "Young volunteers in Kandahar come together as Change in Youths Social Assembly (+CYSA), focused on education, rights awareness and community service."),
               ("2015 — 2018", "From initiative to institution", "Volunteer mobilization, English and computer classes, human-rights awareness and relationships with women-led groups lead to organizational systems and formal registration in 2018."),
               ("2018 — 2021", "Community practice", "Programmes in hygiene and sanitation advocacy, a free community learning centre, health promotion with nomadic communities and a volunteer network."),
               ("2021", "Adaptation", "After August 2021, direct community activities were interrupted. The organization reviewed its identity and approach and continued as The Changemakers."),
               ("Parallel path", "Academies and enterprise", "More than five English-language and computer-training academies; and today DAQIQ International, applying the same founder discipline to international trade."),
               ("Now", "Renewal", "Strengthening governance and partnerships, and developing a women’s economic-empowerment initiative.")]
    jh = "".join(f'<div class="t-item"><div class="t-date">{d}</div><div class="t-body" data-reveal><h3>{t}</h3><p style="margin-top:12px">{x}</p></div></div>' for d, t, x in journey)
    body = head(p, f"Leadership — {NAME} | Founder Journey & Principles", f"The founder journey and leadership principles of {NAME}: building +CYSA / The Changemakers, training academies and DAQIQ INTERNATIONAL.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("Leadership", "Founder journey", "Leadership is <em class='gold'>institution</em> building.", "A founder’s path through youth mobilization, education, humanitarian work and enterprise, and the principles that hold it together.", "identity", 71)}
<section class="section" style="padding-top:20px"><div class="wrap"><div class="timeline"><span class="fill"></span>{jh}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Leadership principles</span><h2 class="h2" data-reveal style="--d:.08s">Six principles behind every organization he builds.</h2></div>
 <div class="grid g3">
  {card("users", "Shared ownership", "Organizations belong to their volunteers, members and communities, not to one person.", 0)}
  {card("shield", "Integrity &amp; accountability", "Accurate records and honest reporting, internally and to every partner.", .06)}
  {card("woman", "Inclusion", "Women and young people are designed in from the start, not added later.", .12)}
  {card("heart", "Human dignity", "Every programme and transaction respects the people it touches.", .18)}
  {card("book", "Continuous learning", "Measure outcomes, not only attendance, and adapt to what is learned.", .24)}
  {card("coins", "Sustainability", "Favour livelihoods and institutions that can stand on their own.", .3)}
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Method</span><h2 class="h2" data-reveal style="--d:.08s">The community practice cycle.</h2>
  <p class="lead" data-reveal style="--d:.16s">The working cycle drawn from +CYSA’s community programmes, from listening to a community through to adapting the next round.</p></div>
 <ol class="grid g3" style="list-style:none;padding:0;margin:0">{stepshtml}</ol>
</div></section>
{cta()}
</main>''' + footer()
    write(p, body)

def daqiq():
    p = "daqiq-international.html"
    areas = "".join(card(i, t, x, k * .04) for k, (i, t, x) in enumerate(DI_AREAS))
    body = head(p, "DAQIQ INTERNATIONAL — International Trade, Sourcing & Distribution | Founder Muhammad Salim Daqiq",
                "DAQIQ INTERNATIONAL, founded and led by Muhammad Salim Daqiq: international import and export, global sourcing, agricultural commodities, food products, industrial supplies and wholesale distribution.",
                [ORG_DI]) + header(p) + f'''
<main id="main" class="page-enter">
<section class="page-hero">
 <div class="bg-art" data-parallax=".08">{art("enterprise", 760, 760, 81, "")}</div>
 <div class="wrap">
  <p class="crumbs" data-reveal><a href="index.html">Home</a> &nbsp;/&nbsp; DAQIQ International</p>
  <h1 class="display" data-reveal style="--d:.08s">DAQIQ <em class="gold">International</em></h1>
  <p class="eyebrow" data-reveal style="--d:.16s">Pillar 02 &middot; The Enterprise</p>
  <p class="lead" data-reveal style="--d:.22s;margin-top:22px">An international trading initiative connecting markets through import and export, global sourcing and dependable partnerships.</p>
  <div class="hero-cta" data-reveal style="margin-top:36px;--d:.3s"><a class="btn btn-gold" href="#partner">Partner with us {ic("arrow")}</a><a class="btn btn-ghost" href="{DI_URL}" target="_blank" rel="noopener">Visit daqiq.af {ic("ext")}</a></div>
 </div>
</section>
<section class="section" style="padding-top:20px"><div class="wrap split">
 <div><span class="eyebrow" data-reveal>Overview</span><h2 class="h2" data-reveal style="--d:.08s;margin:22px 0 26px">Trade built on <em class="gold">trust</em>.</h2>
  <p class="lead" data-reveal style="--d:.16s">DAQIQ International is the entrepreneurial and international trading initiative founded and led by Muhammad Salim Daqiq. It brings together sourcing, supply and distribution for businesses that need reliable partners across borders.</p></div>
 <div class="facts" style="grid-template-columns:1fr 1fr;border:1px solid var(--line-2);border-radius:22px;overflow:hidden" data-reveal="scale">
  <div class="fact"><b style="font-size:30px">Founder</b><span>Muhammad Salim Daqiq</span></div>
  <div class="fact" style="border-right:0"><b style="font-size:30px">Focus</b><span>International trade</span></div>
  <div class="fact" style="border-top:1px solid var(--line-2)"><b style="font-size:30px">Web</b><span>daqiq.af</span></div>
  <div class="fact" style="border-top:1px solid var(--line-2);border-right:0"><b style="font-size:30px">Email</b><span>{EMAIL}</span></div>
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Business areas</span><h2 class="h2" data-reveal style="--d:.08s">Nine areas of commercial focus.</h2></div>
 <div class="grid g3">{areas}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split top">
 <div><span class="eyebrow" data-reveal>How we work</span><h2 class="h2" data-reveal style="--d:.08s;margin-top:22px">Standards before <em class="gold">volume</em>.</h2></div>
 <div class="rows">
  <div class="row" data-reveal><span class="n">01</span><h3>Specification first</h3><p>Every engagement starts with the buyer’s exact requirements: product, quality, quantity, timing and budget.</p></div>
  <div class="row" data-reveal><span class="n">02</span><h3>Verified suppliers</h3><p>Suppliers are compared and checked before any commitment, so partners know who they are dealing with.</p></div>
  <div class="row" data-reveal><span class="n">03</span><h3>Compliance</h3><p>Counterparties are screened against international sanctions lists, and every transaction follows applicable trade rules.</p></div>
  <div class="row" data-reveal><span class="n">04</span><h3>Transparent relationships</h3><p>Clear terms, clear documentation and open communication from enquiry to delivery.</p></div>
 </div>
</div></section>
<section class="section" id="partner" style="padding-top:0"><div class="wrap"><div class="cta-band" data-reveal="scale">
 <span class="eyebrow">Commercial opportunities</span><h2 class="h2">Suppliers, buyers and partners are welcome.</h2>
 <p class="lead" style="margin:0 auto">For sourcing requests, supply offers, distribution or partnership proposals, write to DAQIQ International.</p>
 <div class="hero-cta" style="justify-content:center"><a class="btn btn-gold" href="mailto:{EMAIL}?subject=DAQIQ%20International%20%E2%80%94%20Business%20inquiry">{EMAIL} {ic("mail")}</a><a class="btn btn-ghost" href="contact.html">Contact form {ic("arrow")}</a></div>
</div></div></section>
</main>''' + footer()
    write(p, body)

def changemakers():
    p = "the-changemakers.html"
    themes = "".join(f'<li class="card" data-reveal style="--d:{k*.04:.2f}s;padding:22px;display:flex;gap:16px;align-items:center"><div class="ico" style="margin:0;flex:none">{ic(i)}</div><h3 class="h3" style="margin:0;font-size:18px">{t}</h3></li>' for k, (i, t) in enumerate(CM_THEMES))
    story = [("2015", "Founded", "Established in Kandahar by young people working in the development sector, as Change in Youths Social Assembly (+CYSA)."),
             ("2018", "Registered", "Formally registered in Afghanistan, with organizational systems and administrative structures in place."),
             ("2018 — 2021", "Community practice", "Hygiene and sanitation advocacy; a free community education and learning centre; health promotion with nomadic communities; a volunteer and activist network; youth participation and advocacy."),
             ("Aug 2021", "Transition", "Direct community activities were interrupted. The organization reviewed its identity and operating approach."),
             ("Since 2021", "The Changemakers", "Continuing the journey under a new public identity, with a broader social and community-service orientation."),
             ("Today", "Renewal", "Rebuilding around women’s livelihoods, learning and skills, child protection, community well-being and stronger governance.")]
    sh = "".join(f'<div class="t-item"><div class="t-date">{d}</div><div class="t-body" data-reveal><h3>{t}</h3><p style="margin-top:12px">{x}</p></div></div>' for d, t, x in story)
    body = head(p, "The Changemakers (+CYSA) — Change in Youths Social Assembly | Founded by Muhammad Salim Daqiq",
                "The Changemakers, founded in Kandahar in 2015 as Change in Youths Social Assembly (+CYSA) by Muhammad Salim Daqiq: human rights, youth leadership, women's empowerment, girls' education and community development.",
                [ORG_CM]) + header(p) + f'''
<main id="main" class="page-enter">
<section class="page-hero">
 <div class="bg-art" data-parallax=".08">{art("impact", 760, 760, 91, "")}</div>
 <div class="wrap">
  <p class="crumbs" data-reveal><a href="index.html">Home</a> &nbsp;/&nbsp; The Changemakers</p>
  <h1 class="display" data-reveal style="--d:.08s">The <em class="gold">Changemakers</em></h1>
  <p class="eyebrow" data-reveal style="--d:.16s">Pillar 03 &middot; Formerly Change in Youths Social Assembly (+CYSA)</p>
  <p class="lead" data-reveal style="--d:.22s;margin-top:22px">A community-rooted civil society organization, founded in Kandahar in 2015, working for education, human rights, women’s empowerment and youth development.</p>
 </div>
</section>
<section class="section" style="padding-top:20px"><div class="wrap">
 <div class="facts" data-reveal>
  <div class="fact"><b>2015</b><span>Founded in Kandahar</span></div>
  <div class="fact"><b>2018</b><span>Formally registered</span></div>
  <div class="fact"><b>2021</b><span>Became The Changemakers</span></div>
  <div class="fact"><b>Founder</b><span>Muhammad Salim Daqiq</span></div>
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split">
 <div><span class="eyebrow" data-reveal>Our story</span><h2 class="h2" data-reveal style="--d:.08s;margin:22px 0 26px">Founded by youth. Sustained by <em class="gold">community</em>.</h2>
  <p class="lead" data-reveal style="--d:.16s">The Changemakers is the continuing institutional journey of Change in Youths Social Assembly (+CYSA). Its history belongs to the volunteers, members, community groups and partners who built it alongside its founder.</p></div>
 <div class="quote-wrap" data-reveal="scale"><p class="quote" style="font-size:clamp(26px,3vw,42px)">Change &middot; Youth &middot; Social &middot; Assembly &middot; Action</p><span class="eyebrow">Organizational philosophy</span></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="timeline"><span class="fill"></span>{sh}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Thematic areas</span><h2 class="h2" data-reveal style="--d:.08s">Ten areas of historical and current work.</h2></div>
 <ul class="grid g2" style="list-style:none;padding:0;margin:0">{themes}</ul>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split top">
 <div><span class="eyebrow" data-reveal>Vision &amp; mission</span><h2 class="h2" data-reveal style="--d:.08s;margin-top:22px">Opportunity, knowledge and <em class="gold">dignity</em> for everyone.</h2></div>
 <div class="rows">
  <div class="row" data-reveal><span class="n">V</span><h3>Vision</h3><p>A society in which every person, whatever their social or economic circumstances, has access to opportunity, knowledge, dignity and participation, and the means to create positive change.</p></div>
  <div class="row" data-reveal><span class="n">M</span><h3>Mission</h3><p>To empower young people, women and underserved communities through education, capacity building, volunteerism, rights awareness, community participation and sustainable livelihoods.</p></div>
  <div class="row" data-reveal><span class="n">&#10022;</span><h3>Values</h3><p>Human dignity &middot; Inclusion and equal opportunity &middot; Volunteerism and participation &middot; Integrity and accountability &middot; Learning &middot; Sustainability</p></div>
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
 <div class="cta-band" data-reveal="scale" style="text-align:left;justify-items:start">
  <span class="badge proposed">Proposed initiative</span>
  <h2 class="h2">Women’s Economic Empowerment through Fruit Drying &amp; Processing, Kandahar.</h2>
  <p class="lead" style="margin:0">A women-centred production unit planned for an initial group of 20 women, with training in drying and processing, hygiene and food safety, packaging, business skills and market access. The initiative is in development and seeking partners; it is not yet funded or operating.</p>
  <div class="hero-cta"><a class="btn btn-gold" href="contact.html">Discuss partnership {ic("arrow")}</a><a class="btn btn-ghost" href="projects.html">All projects {ic("arrow")}</a></div>
 </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split top">
 <div><span class="eyebrow" data-reveal>Safeguarding</span><h2 class="h3" data-reveal style="margin-top:18px;font-family:var(--serif);font-weight:500;font-size:clamp(28px,2.6vw,38px)">Protecting the people we serve.</h2></div>
 <p class="lead" data-reveal>We do not publish the names or identifiable images of beneficiaries, women or children. Figures for past reach are the organization’s own and are shared with partners together with their evidence status on request.</p>
</div></section>
{cta("Partner with The Changemakers.", "Development partners, foundations and institutions are invited to collaborate on education, livelihoods and community well-being.", ("contact.html", "Start a conversation"), ("projects.html", "View projects"))}
</main>''' + footer()
    write(p, body)

PROJECTS = [
 ("harvest", "community proposed", "badge proposed", "Proposed", "Women’s Fruit Drying &amp; Processing Unit", "The Changemakers &middot; Kandahar",
  "A women-centred unit planned for an initial 20 women, producing dried and processed fruit products with commercial dehydration equipment, training in food safety, packaging and business skills, and links to markets.", "Seeking partners &middot; not yet funded"),
 ("enterprise", "enterprise", "badge", "In development", "Sourcing &amp; Supplier Verification Services", "DAQIQ International",
  "Helping businesses source products internationally with clear specifications, compared suppliers and verification before commitment.", "Business line in development"),
 ("learning", "community education", "badge hist", "2019 — 2021", "Free Community Education &amp; Learning Centre", "+CYSA &middot; Kandahar City",
  "Free classes for young people, including girls from local schools, with outreach to children in street work and child labour.", "Historical &middot; organization-reported"),
 ("care", "community", "badge hist", "2020 — 2021", "Nomadic Community Sanitation &amp; Health Promotion", "+CYSA &middot; Arghandab",
  "Practical hygiene, sanitation and health-promotion sessions for women and men in nomadic communities, with flexible outreach for mobile families.", "Historical &middot; organization-reported"),
 ("impact", "community", "badge hist", "2018 — 2019", "Community Hygiene &amp; Sanitation Advocacy", "+CYSA &middot; Kandahar",
  "Awareness and community dialogue on hygiene and sanitation, with volunteer mobilization and coordination with the provincial public-health authority.", "Historical &middot; organization-reported"),
 ("identity", "community", "badge hist", "2015 — 2021", "Volunteer &amp; Activist Network", "+CYSA &middot; Kandahar",
  "Recruiting, training and coordinating young volunteers as learners, mobilizers and advocates in their own communities.", "Historical &middot; organization-reported"),
 ("learning", "education", "badge", "Founder", "English-Language &amp; Computer-Training Academies", "Educational entrepreneurship",
  "More than five academies founded and developed to give young people access to English-language learning and digital literacy.", "Education &middot; youth skills"),
]

def projects():
    p = "projects.html"
    cards = "".join(f'''<article class="card project" data-cat="{cat}" data-tilt="4" data-reveal style="--d:{(k%2)*.08:.2f}s">
 <div class="pv">{art(kind, 800, 400, 100+k, "")}</div>
 <div class="pb"><div class="meta"><span class="{bc}">{bl}</span><span>{org}</span></div><h3>{t}</h3><p style="color:var(--soft);margin:0">{x}</p><p class="small muted" style="margin:auto 0 0;padding-top:10px">{st}</p></div></article>'''
                    for k, (kind, cat, bc, bl, t, org, x, st) in enumerate(PROJECTS))
    body = head(p, f"Projects — {NAME} | Enterprise, Education & Community Initiatives", f"Initiatives led by {NAME}: DAQIQ International business development, +CYSA community programmes, training academies and a proposed women's fruit-processing unit.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("Projects", "Portfolio", "Initiatives that create <em class='gold'>opportunity</em>.", "Enterprise, education and community initiatives. Each is labelled clearly as historical, in development or proposed.", "harvest", 111)}
<section class="section" style="padding-top:20px"><div class="wrap">
 <div class="filters" role="group" aria-label="Filter projects">
  <button type="button" data-filter="all" aria-pressed="true">All</button><button type="button" data-filter="enterprise" aria-pressed="false">Enterprise</button>
  <button type="button" data-filter="community" aria-pressed="false">Community</button><button type="button" data-filter="education" aria-pressed="false">Education</button>
  <button type="button" data-filter="proposed" aria-pressed="false">Proposed</button></div>
 <p id="filter-status" class="sr" aria-live="polite"></p>
 <div class="projects">{cards}</div>
 <p class="note" style="margin-top:40px">Historical +CYSA initiatives are described as reported by the organization. Figures and supporting records are shared with partners on request. Proposed initiatives are not yet funded or operating.</p>
</div></section>
{cta("Have a project in mind?", "Partners for enterprise, education and community initiatives are welcome.")}
</main>''' + footer()
    write(p, body)

def media():
    p = "media.html"
    gal = [("identity", "Pillar 01 — Identity: key visual"), ("enterprise", "Pillar 02 — Enterprise: key visual"), ("impact", "Pillar 03 — Impact: key visual")]
    galhtml = "".join(f'<figure style="margin:0"><button type="button" data-lightbox="assets/images/pillars/{k}.svg" data-caption="{c}" aria-label="Open image: {c}"><img src="assets/images/pillars/{k}.svg" alt="{c}" loading="lazy" width="1200" height="900"><figcaption>{c}</figcaption></button></figure>' for k, c in gal)
    bios = "".join(f'''<article class="card bio" data-reveal style="--d:{i*.06:.2f}s"><button class="copy" type="button" data-copy="bio-{n}">Copy</button><span class="badge">{n} words</span><p id="bio-{n}">{t}</p></article>'''
                   for i, (n, t) in enumerate([("25", BIO_25), ("60", BIO_60), ("150", BIO_150)]))
    body = head(p, f"Media & Publications — {NAME} | Press Kit & Official Biographies", f"Media resources for {NAME}: official biographies, press kit, downloadable profile, brand visuals and publications.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("Media &amp; Publications", "Press &amp; media", "Media <em class='gold'>&amp;</em> publications.", "Official biographies, brand visuals, downloadable documents and statements for journalists, partners and event organizers.", "identity", 121)}
<section class="section" style="padding-top:20px"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Official biographies</span><h2 class="h2" data-reveal style="--d:.08s">Approved descriptions for media use.</h2></div>
 <div class="grid" style="gap:18px">{bios}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
 <div class="section-head"><span class="eyebrow" data-reveal>Gallery</span><h2 class="h2" data-reveal style="--d:.08s">Visual identity.</h2>
  <p class="lead" data-reveal style="--d:.16s">Key visuals for the three pillars. A curated photographic archive of professional and organizational activities is being prepared and will be published here.</p></div>
 <div class="gallery">{galhtml}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap grid g3">
 <article class="card" data-reveal><div class="ico">{ic("doc")}</div><h3 class="h3">Publications</h3><p>Articles and papers will be listed here as they are published.</p></article>
 <article class="card" data-reveal style="--d:.06s"><div class="ico">{ic("users")}</div><h3 class="h3">Interviews</h3><p>For interview requests, please use the contact page and choose “Media”.</p></article>
 <article class="card" data-reveal style="--d:.12s"><div class="ico">{ic("spark")}</div><h3 class="h3">Official statements</h3><p>Official statements from Muhammad Salim Daqiq, DAQIQ International and The Changemakers will be published on this page.</p></article>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="card doc" data-reveal>
 <div class="pdf">PDF</div><div><h3>Executive profile &amp; biography</h3><p>Download the official CV and biography for media and partners.</p></div>
 <a class="btn btn-gold" href="download-profile.html">Downloads {ic("down")}</a></div></div></section>
</main>''' + footer()
    write(p, body)

def contact():
    p = "contact.html"
    body = head(p, f"Contact {NAME} — Business Inquiries & Partnerships", f"Contact {NAME} for business inquiries with DAQIQ INTERNATIONAL, organizational partnerships with The Changemakers, media and collaboration.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("Contact", "Let’s connect", "Start a <em class='gold'>conversation</em>.", "Business inquiries, organizational partnerships, media requests and collaboration.", "care", 131)}
<section class="section" style="padding-top:20px"><div class="wrap contact-grid">
 <div class="channels">
  <a class="card channel" href="mailto:{EMAIL}" data-reveal><div class="ico">{ic("mail")}</div><div><b>Email</b><span>{EMAIL}</span></div></a>
  <a class="card channel" href="{DI_URL}" target="_blank" rel="noopener" data-reveal style="--d:.06s"><div class="ico">{ic("globe")}</div><div><b>DAQIQ International</b><span>daqiq.af</span></div></a>
  <a class="card channel" href="{CM_URL}" target="_blank" rel="noopener" data-reveal style="--d:.12s"><div class="ico">{ic("users")}</div><div><b>The Changemakers</b><span>thechangemakers.daqiq.af</span></div></a>
  <div class="card channel" data-reveal style="--d:.18s"><div class="ico">{ic("pin")}</div><div><b>Based in</b><span>Afghanistan &middot; working internationally</span></div></div>
 </div>
 <form class="card contact" data-to="{EMAIL}" novalidate data-reveal="scale">
  <div class="field"><label for="f-topic">Topic</label><select id="f-topic" name="topic" required>
   <option>Business inquiry — DAQIQ International</option><option>Partnership — The Changemakers</option><option>Media</option><option>Collaboration</option><option>Other</option></select></div>
  <div class="grid g2" style="gap:18px"><div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
   <div class="field"><label for="f-org">Organization</label><input id="f-org" name="org" autocomplete="organization"></div></div>
  <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required></textarea></div>
  <button class="btn btn-gold" type="submit" style="justify-self:start">Compose email {ic("arrow")}</button>
  <p class="form-note">This opens your email app with the message ready to send. Nothing is stored on this website.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
</div></section>
</main>''' + footer()
    write(p, body)

def download():
    p = "download-profile.html"
    body = head(p, f"Download Profile — {NAME} | Executive CV & Biography (PDF)", f"Download the official executive CV and biography of {NAME} in PDF format.") + header(p) + f'''
<main id="main" class="page-enter">
{page_hero("Download Profile", "Documents", "The official <em class='gold'>profile</em>.", "An executive CV and a professional biography, prepared from verified information.", "identity", 141)}
<section class="section" style="padding-top:20px"><div class="wrap grid" style="gap:18px">
 <div class="card doc" data-reveal><div class="pdf">PDF</div><div><h3>Executive CV</h3><p>Experience, founder roles, education and capabilities. 2 pages.</p></div>
  <a class="btn btn-gold" href="assets/documents/cv/Muhammad-Salim-Daqiq-Executive-CV.pdf" download>Download {ic("down")}</a></div>
 <div class="card doc" data-reveal style="--d:.08s"><div class="pdf">PDF</div><div><h3>Professional biography</h3><p>Short, medium and full-length official biographies. 1 page.</p></div>
  <a class="btn btn-gold" href="assets/documents/cv/Muhammad-Salim-Daqiq-Biography.pdf" download>Download {ic("down")}</a></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split top">
 <div><span class="eyebrow" data-reveal>At a glance</span><h2 class="h2" data-reveal style="--d:.08s;margin-top:22px">Profile summary.</h2></div>
 <div class="rows">
  <div class="row" data-reveal><span class="n">01</span><h3>Founder</h3><p>DAQIQ International &middot; The Changemakers (+CYSA, 2015) &middot; more than five training academies</p></div>
  <div class="row" data-reveal><span class="n">02</span><h3>Experience</h3><p>World Food Programme (2021–2024) &middot; Kandahar Directorate of Public Health (2024–2025) &middot; Psychosocial support (2025–)</p></div>
  <div class="row" data-reveal><span class="n">03</span><h3>Education</h3><p>BSc Agricultural Science, University of Kandahar &middot; Diplomas in Business Administration and Computer &amp; IT</p></div>
  <div class="row" data-reveal><span class="n">04</span><h3>Contact</h3><p><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></p></div>
 </div>
</div></section>
</main>''' + footer()
    write(p, body)

def notfound():
    p = "404.html"
    body = head(p, f"Page not found — {NAME}", "The page you are looking for could not be found.").replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    # absolute asset paths so the 404 works at any depth on GitHub Pages
    body = body.replace('href="assets/', 'href="/assets/').replace('href="manifest.json"', 'href="/manifest.json"')
    sh = header(p).replace('href="', 'href="/').replace('href="/#', 'href="#').replace('href="/http', 'href="http')
    ft = footer().replace('href="', 'href="/').replace('href="/mailto', 'href="mailto').replace('href="/http', 'href="http').replace('src="assets', 'src="/assets')
    body += sh + f'''<main id="main" class="err"><div class="wrap">
 <div class="num gold">404</div><h1 class="h2" style="margin:10px 0 18px">This page has moved, or never existed.</h1>
 <p class="lead" style="margin:0 auto 34px">Let’s get you back on course.</p>
 <div class="hero-cta" style="justify-content:center"><a class="btn btn-gold" href="/">Return home {ic("arrow")}</a><a class="btn btn-ghost" href="/contact.html">Contact {ic("arrow")}</a></div>
</div></main>''' + ft
    write(p, body)

def meta_files():
    pages = ["index.html", "about.html", "experience.html", "education.html", "leadership.html", "daqiq-international.html", "the-changemakers.html", "projects.html", "media.html", "contact.html", "download-profile.html"]
    pri = {"index.html": "1.0", "about.html": "0.9", "daqiq-international.html": "0.9", "the-changemakers.html": "0.9"}
    urls = "".join(f'<url><loc>{BASE}/{"" if pg == "index.html" else pg}</loc><lastmod>{TODAY}</lastmod><priority>{pri.get(pg, "0.7")}</priority></url>\n' for pg in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    write("manifest.json", json.dumps({"name": f"{NAME} — Official Website", "short_name": "DAQIQ", "start_url": "./", "display": "standalone",
        "background_color": "#070d1c", "theme_color": "#070d1c", "icons": [{"src": "assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    write(".nojekyll", "")
    # standalone pillar visuals for the media gallery
    for k, s in [("identity", 201), ("enterprise", 202), ("impact", 203)]:
        svg = art(k, 1200, 900, s, "").replace('<svg class=""', '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" style="background:#070d1c"')
        write(f"assets/images/pillars/{k}.svg", svg)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "assets/images/pillars"), exist_ok=True)
    for f in (home, about, experience, education, leadership, daqiq, changemakers, projects, media, contact, download, notfound, meta_files):
        f()
    print("built into", ROOT)
