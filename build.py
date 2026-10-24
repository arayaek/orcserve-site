"""ORCSERVE marketing site — static-site generator (standard library only).

Why a generator instead of hand-edited HTML: the site chrome (head, header/nav, footer) and
the brand identity are defined ONCE here, and every page is composed from shared pieces. That
keeps pages consistent and makes site-wide changes a one-line edit — including the product
name, which lives in a single ``BRAND`` constant so ORCSERVE <-> ORCHSERVE (or any rename) is
one change plus a rebuild.

    python build.py            # writes ./site/*.html and copies ./assets -> ./site/assets

Then open ``site/index.html`` or host the ``site/`` folder on any static host.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "site"

# ---------------------------------------------------------------------------------------
# Brand — the single source of truth. Rename here, rebuild, done.
# ---------------------------------------------------------------------------------------
BRAND = {
    "name": "ORCSERVE",
    "lead": "ORC",          # bold navy part of the wordmark
    "tail": "SERVE",        # accent part of the wordmark
    "tagline": "Connect. Synchronize. Empower.",
    "promise": "Your enterprise systems manage the business. ArcGIS manages the field. "
               "ORCSERVE connects the two.",
    "email": "info@orcserve.com",
    "location": "McLean, Virginia",
}

NAV = [
    ("platform.html", "Platform"),
    ("how-it-works.html", "How It Works"),
    ("solutions.html", "Solutions"),
    ("where-we-fit.html", "Where We Fit"),
    ("workflow-assessment.html", "Workflow Assessment"),
    ("resources.html", "Resources"),
    ("about.html", "About"),
]

# ---------------------------------------------------------------------------------------
# Reusable SVG pieces
# ---------------------------------------------------------------------------------------
LOGO_SVG = """<svg class="mark" viewBox="0 0 80 80" fill="none" aria-hidden="true">
<circle cx="30" cy="28" r="16" stroke="var(--blue)" stroke-width="7"/>
<circle cx="50" cy="28" r="16" stroke="var(--navy)" stroke-width="7"/>
<circle cx="40" cy="49" r="16" stroke="var(--green)" stroke-width="7"/></svg>"""


def wordmark(cls: str = "") -> str:
    return (f'<a class="brand {cls}" href="index.html" aria-label="{BRAND["name"]} home">'
            f'{LOGO_SVG}<span class="wm"><b>{BRAND["lead"]}</b>{BRAND["tail"]}</span></a>')


# Animated enterprise -> ORCSERVE -> ArcGIS -> field -> back diagram (pure inline SVG/CSS).
HERO_DIAGRAM = """
<svg class="flowdiagram" viewBox="0 0 780 470" role="img"
     aria-label="Data flows from enterprise systems through ORCSERVE into ArcGIS field
     operations, and field updates synchronize back to the system of record.">
  <defs>
    <linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d4890"/><stop offset="1" stop-color="#082a52"/>
    </linearGradient>
    <marker id="ah" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--green)"/>
    </marker>
    <marker id="ah2" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--blue)"/>
    </marker>
  </defs>

  <!-- flowing connectors -->
  <path class="flowline" d="M232,150 H300" marker-end="url(#ah2)"/>
  <path class="flowline d2" d="M548,150 H616" marker-end="url(#ah)"/>
  <!-- return loop -->
  <path class="flowline back" d="M690,300 V372 H90 V196" marker-end="url(#ah2)"/>

  <!-- Enterprise systems -->
  <g>
    <rect x="70" y="70" width="162" height="160" rx="14" class="node"/>
    <text x="151" y="96" class="node-title">ENTERPRISE SYSTEMS</text>
    <text x="151" y="124" class="node-line">CRM &middot; ERP</text>
    <text x="151" y="148" class="node-line">Asset Management</text>
    <text x="151" y="172" class="node-line">Work Management</text>
    <text x="151" y="196" class="node-line">Permitting &middot; 311</text>
  </g>

  <!-- ORCSERVE core -->
  <g>
    <rect x="300" y="60" width="248" height="180" rx="16" class="core"/>
    <text x="424" y="92" class="core-title">ORCSERVE</text>
    <text x="424" y="114" class="core-sub">INTEGRATION &amp; SYNC PLATFORM</text>
    <line x1="324" y1="128" x2="524" y2="128" class="hair"/>
    <text x="424" y="152" class="core-line">Configurable Connectors</text>
    <text x="424" y="176" class="core-line">Canonical Data Model</text>
    <text x="424" y="200" class="core-line">Bi-directional Sync Engine</text>
    <text x="424" y="224" class="core-line">Validation &middot; Monitoring</text>
  </g>

  <!-- ArcGIS -->
  <g>
    <rect x="616" y="70" width="150" height="160" rx="14" class="node arc"/>
    <text x="691" y="96" class="node-title">ARCGIS ONLINE</text>
    <text x="691" y="124" class="node-line">Feature Layers</text>
    <text x="691" y="148" class="node-line">Field Maps</text>
    <text x="691" y="172" class="node-line">Dashboards</text>
    <text x="691" y="196" class="node-line">Survey123</text>
  </g>

  <!-- return label -->
  <g>
    <rect x="250" y="348" width="300" height="48" rx="12" class="ret"/>
    <text x="400" y="370" class="ret-title">UPDATES &amp; STATUS</text>
    <text x="400" y="386" class="ret-sub">Status &middot; Photos &middot; Notes &middot; Inspections &rarr; back to source</text>
  </g>
</svg>"""


def loop_svg() -> str:
    """The vertical 'How ORCSERVE works' loop used on the How It Works page."""
    steps = [
        ("System of Record", "src"), ("Query work data", ""),
        ("ORCSERVE", "core"), ("ArcGIS Feature Layers", "arc"),
        ("Field Maps &middot; Dashboards &middot; Experience Builder &middot; Survey123", "arc"),
        ("Field Workforce", ""), ("Status &middot; Photos &middot; Notes &middot; Inspections", ""),
        ("Synchronize back", ""), ("System of Record", "src"),
    ]
    rows = "".join(
        f'<li class="loop-step {cls}"><span>{i+1}</span><p>{label}</p></li>'
        for i, (label, cls) in enumerate(steps))
    return f'<ol class="looplist">{rows}</ol>'


# ---------------------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------------------
def page(slug: str, title: str, description: str, body: str) -> str:
    nav = "".join(f'<a href="{href}">{label}</a>' for href, label in NAV)
    year_ph = '<span data-year></span>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0b2f5c">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body data-page="{slug}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container bar">
    {wordmark()}
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" class="nav">{nav}<a class="btn btn-sm" href="contact.html">Request Demo</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container foot-grid">
    <div class="foot-brand">
      {wordmark("on-dark")}
      <p>{BRAND["promise"]}</p>
    </div>
    <div><h4>Platform</h4><a href="platform.html">Platform</a><a href="how-it-works.html">How It Works</a><a href="where-we-fit.html">Where We Fit</a><a href="workflow-assessment.html">Workflow Assessment</a></div>
    <div><h4>Company</h4><a href="about.html">About</a><a href="solutions.html">Solutions</a><a href="resources.html">Resources</a></div>
    <div><h4>Contact</h4><a href="mailto:{BRAND['email']}">{BRAND['email']}</a><span>{BRAND['location']}</span><a href="contact.html">Request a demo</a></div>
  </div>
  <div class="container foot-bottom">
    <span>&copy; {year_ph} {BRAND['name']}. Draft site — pre-launch.</span>
    <span>{BRAND['tagline']}</span>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>"""


# ---------------------------------------------------------------------------------------
# Section helpers
# ---------------------------------------------------------------------------------------
def eyebrow(t): return f'<p class="eyebrow">{t}</p>'


def head(title, sub="", eb="", center=True):
    c = " center" if center else ""
    e = eyebrow(eb) if eb else ""
    p = f"<p>{sub}</p>" if sub else ""
    return f'<div class="head{c}">{e}<h2>{title}</h2>{p}</div>'


# ---------------------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------------------
def home():
    approaches = [
        ("Manual processes", ["Source system", "Excel", "Printed sheets", "Manual re-entry"],
         ["Duplicate entry and avoidable errors", "Delayed updates, poor visibility",
          "Hard to monitor or scale", "No integrated GIS workflow"]),
        ("Commercial field platforms", ["Source system", "Vendor platform", "Vendor app"],
         ["High license and implementation cost", "Limited fit for unique workflows",
          "Vendor lock-in", "Doesn't unlock the full ArcGIS ecosystem"]),
        ("Custom integration code", ["Source system", "Custom code", "ArcGIS"],
         ["Expensive to build", "Heavy maintenance burden",
          "Knowledge trapped with a few developers", "Every workflow a new project"]),
    ]
    cards = ""
    for i, (title, flow, trades) in enumerate(approaches, 1):
        chips = '<i>&darr;</i>'.join(f"<span>{s}</span>" for s in flow)
        li = "".join(f"<li>{t}</li>" for t in trades)
        cards += (f'<article class="approach"><span class="tag">Approach {i:02d}</span>'
                  f'<h3>{title}</h3><div class="mini-flow">{chips}</div>'
                  f'<ul class="trade">{li}</ul></article>')

    steps = [
        ("Connect", "Query work from the source system",
         "ORCSERVE reads from CRM, ERP, asset, work-management, permitting, and custom systems "
         "through approved APIs or databases — you pick the records and fields that matter.",
         ["Select the records that matter", "Map and standardize source fields",
          "Validate before anything is published"]),
        ("Empower", "Put the work on the ArcGIS map",
         "Work becomes live ArcGIS features, so teams can run real field workflows across the "
         "platform they already own.",
         ["Field Maps, online and offline", "Dashboards and live visibility",
          "Experience Builder, Survey123, routing, analytics"]),
        ("Synchronize", "Keep the system of record current",
         "Field updates are validated and written back to the enterprise system — automatically, "
         "with loop prevention and an audit trail.",
         ["Status and completion dates", "Notes, photos, inspections",
          "Crew, asset, and custom fields"]),
    ]
    step_cards = ""
    for i, (kick, t, p, items) in enumerate(steps, 1):
        li = "".join(f"<li>{x}</li>" for x in items)
        step_cards += (f'<article class="step reveal"><strong>Step {i} &middot; {kick}</strong>'
                       f'<h3>{t}</h3><p>{p}</p><ul>{li}</ul></article>')

    deploy = [
        ("&#9635;", "On-premises", "Runs on customer-managed infrastructure inside the agency network."),
        ("&#9729;", "Azure", "Deploys in the customer's Microsoft Azure tenant."),
        ("AWS", "AWS", "Deploys in an approved AWS environment."),
        ("&#10003;", "Customer-controlled", "Credentials, data, and logs stay in the approved environment."),
    ]
    dep = "".join(f'<article class="card"><div class="ic">{ic}</div><h3>{t}</h3><p>{p}</p></article>'
                  for ic, t, p in deploy)

    inds = [
        ("Public Works", "311, sanitation, streets, signs, litter, bulk pickup, inspections."),
        ("Utilities", "Water, wastewater, electric, gas, outages, maintenance, assets."),
        ("Transportation", "Roads, rail, traffic assets, incidents, signs, signals."),
        ("Campuses & Facilities", "Universities, airports, hospitals, ports, industrial sites."),
    ]
    ind = "".join(f'<article class="industry"><h3>{t}</h3><p>{p}</p></article>' for t, p in inds)

    return f"""
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      {eyebrow("Enterprise integration for ArcGIS field operations")}
      <h1>Unlock the full power of ArcGIS&mdash;<span class="grad">without replacing your enterprise systems.</span></h1>
      <p class="lead">ORCSERVE queries work from your system of record, puts it on the ArcGIS map to
      power real field workflows, and synchronizes field updates back to the source&mdash;automatically.</p>
      <div class="actions">
        <a class="btn" href="contact.html">Request a Demo &rarr;</a>
        <a class="btn btn-ghost" href="how-it-works.html">See how it works</a>
      </div>
      <ul class="proof">
        <li>Working two-way sync, proven against ArcGIS Online</li>
        <li>Configuration over custom code</li>
        <li>Customer-hosted by default</li>
      </ul>
    </div>
    <div class="hero-visual reveal">{HERO_DIAGRAM}</div>
  </div>
  <div class="valuebar"><div class="container valuegrid">
    <div><b>01</b> Query work from source systems</div>
    <div><b>02</b> Put work on the ArcGIS map</div>
    <div><b>03</b> Run field workflows</div>
    <div><b>04</b> Sync updates back</div>
  </div></div>
</section>

<section class="section">
  <div class="container">
    {head("Three ways agencies manage field work today &mdash; and where each falls short",
          "Most organizations rely on one of these approaches. Each can work; each carries real trade-offs.",
          "The problem ORCSERVE solves")}
    <div class="approach-grid">{cards}</div>
    <div class="orc-callout reveal">
      <div>
        {eyebrow("A better approach")}
        <h3>{BRAND['promise']}</h3>
        <p>Use the systems you already own, activate the full ArcGIS ecosystem, and keep the
        system of record current through configurable two-way synchronization.</p>
        <a class="btn" href="how-it-works.html">Explore the workflow &rarr;</a>
      </div>
      {loop_svg()}
    </div>
  </div>
</section>

<section class="section soft">
  <div class="container">
    {head("Connect. Empower. Synchronize.", "", "Simple to understand")}
    <div class="steps">{step_cards}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    {head("Your workflows aren't one-size-fits-all. Your software shouldn't be either.",
          "No two cities run service requests the same way &mdash; and inside one city, a pothole, "
          "an illegal-dumping report, a downed sign, and a missed pickup each follow a different path.",
          "Built for your workflows")}
    <div class="split">
      <div>
        <p>All-in-one platforms bring their <em>own</em> fixed process and ask your operation to
        conform to it &mdash; the workflows that make your city run don't fit the box.</p>
        <p><strong>OrcServe adapts to the workflows you already run &mdash; per request type &mdash;
        and keeps your system of record in charge. The map fits your work.</strong></p>
        <ul class="check"><li>Configurable per request type</li><li>Keeps your system of record
        &mdash; no rip-and-replace</li><li>Your process, made spatial and field-ready</li></ul>
      </div>
      <div class="ways">
        <article class="way"><span class="way-tag">Migration</span><p>Adopt a platform's built-in
        process and reshape your operation around it.</p></article>
        <article class="way orc"><span class="way-tag">Integration</span><p>Keep your systems and
        workflows &mdash; and connect them to ArcGIS. <strong>OrcServe is the integration.</strong></p></article>
      </div>
    </div>
  </div>
</section>

<section class="signature"><div class="container">
  <p class="statement">ORCSERVE turns enterprise records into intelligent, map-based field
  workflows&mdash;and keeps the system of record up to date.</p>
</div></section>

<section class="section dark">
  <div class="container">
    {head("Run ORCSERVE where your organization prefers.",
          "Keep credentials and operational data in an approved, customer-controlled environment.",
          "Deployment flexibility")}
    <div class="grid4">{dep}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    {head("One platform. Many field workflows.", "", "Built for distributed operations")}
    <div class="grid4 industries">{ind}</div>
    <div class="actions center"><a class="btn btn-ghost" href="solutions.html">Explore solutions</a></div>
  </div>
</section>

<section class="cta"><div class="container cta-grid">
  <div>{eyebrow("Start a conversation")}
    <h2>Ready to connect your systems and empower your field teams?</h2>
    <p>Tell us how work reaches the field today&mdash;we'll help you evaluate a more connected approach.</p></div>
  <div class="actions">
    <a class="btn btn-light" href="contact.html">Request Demo</a>
    <a class="btn btn-outline" href="workflow-assessment.html">Workflow Assessment</a>
  </div>
</div></section>
"""


def pagehero(eb, title, lead):
    return (f'<section class="pagehero"><div class="container">{eyebrow(eb)}'
            f'<h1>{title}</h1><p class="lead">{lead}</p></div></section>')


def platform():
    caps = ["Connector framework for enterprise source systems",
            "Configurable source-to-target field mappings", "Canonical work-item data model",
            "Bi-directional synchronization engine",
            "Validation, retry, reconciliation, and exception handling",
            "Monitoring, logging, and operational health", "Flexible customer-hosted deployment"]
    layers = ["Connectors & APIs", "Configuration & Mapping Engine", "Canonical Work Model",
              "Synchronization & Rules Engine", "Monitoring, Logging & Reconciliation",
              "ArcGIS Feature Layers & Applications"]
    cap_li = "".join(f"<li>{c}</li>" for c in caps)
    lay = "".join(f"<div>{l}</div>" for l in layers)
    cards = [("&harr;", "Reusable connectors",
              "Build a connection pattern once, then configure it for new customers and workflows."),
             ("&#9881;", "Customer-specific configuration",
              "Support unique fields, statuses, rules, schedules, and ArcGIS layers without redesigning the platform."),
             ("&#43;", "ArcGIS-only fields",
              "Let field teams use operational fields (equipment, payment status) without forcing every field back to the source.")]
    c = "".join(f'<article class="card reveal"><div class="ic">{i}</div><h3>{t}</h3><p>{p}</p></article>'
                for i, t, p in cards)
    return (pagehero("The ORCSERVE platform",
                     "Reusable integration architecture for ArcGIS field operations.",
                     "ORCSERVE replaces repeated one-off integrations with a configurable platform for "
                     "connecting enterprise systems, standardizing work, synchronizing ArcGIS layers, and "
                     "operating reliable field workflows.")
            + f"""<section class="section"><div class="container split">
        <div>{eyebrow("Core capabilities")}<h2>Configuration where customers differ. Reusable software where they don't.</h2>
        <ul class="check">{cap_li}</ul></div>
        <div class="diagram"><div class="layers">{lay}</div></div></div></section>
        <section class="section soft"><div class="container">
        {head("From one workflow to an enterprise integration foundation.", "", "Designed to scale")}
        <div class="grid3">{c}</div></div></section>""")


def how_it_works():
    steps = [("Connect", "Query the source system",
              "Connect through approved APIs, databases, or integration endpoints and select the records and fields each workflow needs."),
             ("Empower", "Publish to ArcGIS",
              "Create or update ArcGIS features so teams work spatially with Field Maps, Dashboards, Experience Builder, Survey123, routing, and analysis."),
             ("Synchronize", "Return field updates",
              "Validate completed work and synchronize status, dates, notes, photos, inspections, and crew data back to the system of record.")]
    sc = "".join(f'<article class="step reveal"><strong>{k}</strong><h3>{t}</h3><p>{p}</p></article>'
                 for k, t, p in steps)
    checks = ["Spatially aware assignments and routing", "Mobile and offline field execution",
              "Real-time dashboards and management visibility",
              "Photos, notes, inspections, and evidence", "Automatic updates to the system of record"]
    ch = "".join(f"<li>{c}</li>" for c in checks)
    return (pagehero("How it works", "From system of record to field workflow&mdash;and back.",
                     "ORCSERVE automates the full operational loop while preserving each platform's role: "
                     "the enterprise system stays the system of record, and ArcGIS becomes the field environment.")
            + f"""<section class="section"><div class="container"><div class="steps">{sc}</div></div></section>
        <section class="section soft"><div class="container split">
        {loop_svg()}
        <div>{eyebrow("Closed-loop operations")}<h2>Not just points on a map.</h2>
        <p>ORCSERVE runs a managed operational loop: assign work, prioritize geographically, work offline,
        capture evidence, monitor progress, and keep the enterprise system as the official record.</p>
        <ul class="check">{ch}</ul></div></div></section>""")


def solutions():
    inds = [("Municipal Public Works", "311 requests, sanitation, bulk collection, street cleaning, signs, litter, illegal dumping, vegetation, inspections."),
            ("Water & Wastewater", "Leaks, meters, hydrants, valves, inspections, preventive maintenance, service orders, emergency response."),
            ("Electric & Gas Utilities", "Outages, inspections, vegetation management, field construction, safety, asset updates."),
            ("Transportation", "Roads, bridges, rail, incidents, signs, signals, pavement, infrastructure inspections."),
            ("Airports & Ports", "Runways, lighting, facilities, work orders, environmental operations, safety response."),
            ("Universities & Campuses", "Buildings, grounds, utilities, housing, safety, facilities, service requests."),
            ("Telecommunications", "Field service, network assets, inspections, construction, outage response."),
            ("Industrial Operations", "Manufacturing, pipelines, environmental compliance, asset-intensive facilities, distributed inspections.")]
    cards = "".join(f'<article class="industry reveal"><h3>{t}</h3><p>{p}</p></article>' for t, p in inds)
    return (pagehero("Solutions", "Built for organizations managing geographically distributed work.",
                     "Wherever enterprise work records, assets, inspections, and service requests must become "
                     "actionable on a map, ORCSERVE connects the source system to ArcGIS field operations.")
            + f'<section class="section"><div class="container"><div class="grid4 industries">{cards}</div></div></section>')


def where_we_fit():
    cats = [
        ("Enterprise waste platforms", "Routeware / Rubicon, AMCS",
         "Purpose-built to run an entire waste operation end to end — recurring collection routing, "
         "fleet and in-cab technology, service verification, billing, and compliance — proven at scale.",
         "These are systems of record and operations platforms. OrcServe connects them — or your CRM / "
         "311 — to ArcGIS Field Maps, adding flexible, per-request-type service-request workflows and "
         "two-way sync. It complements the platform; it doesn't replace it."),
        ("Route optimization", "RouteSmart, WorkWave, OptimoRoute",
         "Sophisticated route optimization, especially for recurring, high-density collection. "
         "RouteSmart in particular is built on Esri ArcGIS and excels at large-scale routing.",
         "OrcServe isn't a routing engine. For ad-hoc service-request work it surfaces ArcGIS's own "
         "routing, and it integrates cleanly with a dedicated optimizer when you run one."),
        ("Spatial integration / ETL", "FME (Safe Software)",
         "The most powerful general-purpose toolkit for moving data in and out of ArcGIS — capable of "
         "building virtually any integration a GIS engineer can design.",
         "OrcServe is the turnkey, supported solution for one specific workflow — service requests to "
         "Field Maps and back — with the operational logic already built. No build project, no "
         "dedicated GIS-engineering time. It coexists with FME."),
        ("Public-works asset & work management", "Cityworks, OpenGov / Cartegraph",
         "Robust, GIS-centric management of assets and work orders. Cityworks is Esri-native and deeply "
         "capable for public-works operations.",
         "OrcServe bridges external systems of record — 311, CRM, permitting — into your ArcGIS and "
         "field environment, complementing an asset or work-management platform rather than duplicating it."),
        ("311 & CRM (systems of record)", "Salesforce, SeeClickFix, city-native 311",
         "Where citizen requests and customer data live and are managed — the authoritative system of "
         "record for the work.",
         "OrcServe keeps these as the system of record and makes their work spatial, field-ready, and "
         "two-way in ArcGIS — no migration, no rip-and-replace."),
    ]
    items = "".join(
        f'<article class="fititem"><h3>{name}</h3><p class="ex">{ex}</p>'
        f'<div class="fitcols"><div><span class="lbl">What they do well</span><p>{good}</p></div>'
        f'<div><span class="lbl orc">Where OrcServe fits</span><p>{fit}</p></div></div></article>'
        for name, ex, good, fit in cats)
    return (pagehero("Where OrcServe fits", "Built to work with the tools you already trust.",
                     "OrcServe doesn't replace the platforms your city has invested in — it connects "
                     "them to ArcGIS field operations and adapts to how you actually work. Here's how "
                     "we fit with the technologies you may already know.")
            + f'<section class="section"><div class="container"><div class="fitlist">{items}</div></div></section>'
            + '<section class="section soft"><div class="container">'
            + head("We didn't build OrcServe in a vacuum.",
                   "Across this landscape of capable platforms, one gap remains: connecting the system a "
                   "city already runs to ArcGIS field operations, adapted to how that city actually works "
                   "— turnkey, two-way, and supported. That's the gap OrcServe fills.", "Why we built it")
            + '<div class="actions center"><a class="btn" href="contact.html">Request a demo</a></div>'
            + '</div></section>')


def workflow_assessment():
    phases = [("1", "Discovery", "Interview business, GIS, IT, dispatch, supervisors, and field staff."),
              ("2", "Current-state mapping", "Document systems, handoffs, spreadsheets, delays, and duplication."),
              ("3", "Gap analysis", "Identify operational, data, integration, security, and reporting gaps."),
              ("4", "Future-state roadmap", "Recommend workflows, architecture, priorities, ROI, and phases.")]
    pc = "".join(f'<article class="card reveal"><div class="ic">{n}</div><h3>{t}</h3><p>{p}</p></article>'
                 for n, t, p in phases)
    deliv = ["Current-state workflow diagrams", "Systems and data inventory",
             "Pain-point and risk assessment", "Future-state operating model",
             "Recommended ArcGIS workflows", "Integration and deployment architecture",
             "Phased implementation roadmap", "Expected benefits and ROI framework"]
    dl = "".join(f"<li>{d}</li>" for d in deliv)
    outs = ["Clear priorities", "Reduced implementation risk", "Business and IT alignment",
            "Realistic scope and roadmap", "Stronger procurement decisions"]
    ol = "".join(f"<div>{o}</div>" for o in outs)
    return (pagehero("Workflow assessment", "Understand the process before selecting the technology.",
                     "An independent engagement that documents how work moves from request to completion, "
                     "identifies gaps, and defines a practical future-state roadmap.")
            + f"""<section class="section"><div class="container"><div class="grid4">{pc}</div></div></section>
        <section class="section soft"><div class="container split">
        <div>{eyebrow("Typical deliverables")}<h2>A decision-ready view of the opportunity.</h2>
        <ul class="check">{dl}</ul></div>
        <div class="diagram"><h3>Assessment outcomes</h3><div class="layers">{ol}</div></div></div></section>""")


def resources():
    items = [("Overview", "Executive Product Overview", "What ORCSERVE does, why it matters, and where it fits in an enterprise architecture."),
             ("Guide", "ArcGIS Field Operations Architecture Guide", "Patterns for connecting enterprise systems, feature layers, mobile workflows, dashboards, and the system of record."),
             ("Guide", "Field Workflow Modernization Guide", "How to weigh manual, commercial-platform, and custom-integration approaches."),
             ("Deploy", "Customer-Hosted Deployment Guide", "Security, infrastructure, operations, monitoring, responsibilities, and options.")]
    rl = "".join(f'<article class="resource reveal"><div class="rtag">{tag}</div>'
                 f'<div><h3>{t}</h3><p>{p}</p><span class="pill">Planned resource</span></div></article>'
                 for tag, t, p in items)
    return (pagehero("Resources", "Practical guidance for modernizing field operations.",
                     "The starting outline for ORCSERVE's thought-leadership and customer-enablement library.")
            + f'<section class="section"><div class="container resource-list">{rl}</div></section>')


def about():
    return (pagehero("About ORCSERVE", "Helping organizations get more value from the systems they already own.",
                     "ORCSERVE is an independently developed integration platform, built from public standards "
                     "(Open311, the ArcGIS REST API) to connect enterprise systems of record with ArcGIS field operations.")
            + f"""<section class="section"><div class="container split">
        <div>{eyebrow("Our belief")}<h2>Enterprise systems and ArcGIS should work together.</h2></div>
        <div><p>Organizations have invested heavily in CRMs, ERPs, work- and asset-management systems, and ArcGIS.
        Yet field workflows are often disconnected, manual, expensive, or locked inside one-off custom software.</p>
        <p>ORCSERVE closes that gap with a configurable integration platform that keeps the enterprise system as the
        system of record while unlocking ArcGIS for field execution, visibility, and analysis.</p>
        <blockquote>{BRAND['promise']}</blockquote></div></div></section>
        <section class="section soft"><div class="container"><div class="grid3">
        <article class="card"><h3>Mission</h3><p>Make enterprise-to-field integration configurable, reusable, secure, and accessible to more organizations.</p></article>
        <article class="card"><h3>Product philosophy</h3><p>Leverage what customers already own. Configure where organizations differ. Reuse architecture wherever possible.</p></article>
        <article class="card"><h3>Initial focus</h3><p>Municipal public works and other organizations with distributed work, operational data, and strong ArcGIS investments.</p></article>
        </div></div></section>""")


def contact():
    checks = ["Enterprise system and integration options", "ArcGIS Online and Field Maps environment",
              "Current manual or vendor-supported workflow", "Data synchronization and system-of-record needs",
              "Security and deployment requirements"]
    ch = "".join(f"<li>{c}</li>" for c in checks)
    return (pagehero("Contact", "Let's discuss how work reaches your field teams.",
                     "Share your current enterprise system, ArcGIS environment, workflow challenges, and objectives.")
            + f"""<section class="section"><div class="container contact-box">
        <div><h2>Start with your current workflow.</h2>
        <p>ORCSERVE can support an initial discussion, a structured workflow assessment, or planning for a pilot.</p>
        <ul class="check">{ch}</ul>
        <p><strong>Email:</strong> <a href="mailto:{BRAND['email']}">{BRAND['email']}</a></p></div>
        <form class="form" action="mailto:{BRAND['email']}" method="post" enctype="text/plain">
        <h3>Request a conversation</h3>
        <label>Name<input name="Name" required></label>
        <label>Organization<input name="Organization"></label>
        <label>Email<input type="email" name="Email" required></label>
        <label>Primary interest<select name="Interest">
          <option>Product demonstration</option><option>Workflow assessment</option>
          <option>Pilot deployment</option><option>Partnership</option></select></label>
        <label>How do you manage field work today?<textarea name="Message"></textarea></label>
        <button class="btn" type="submit">Submit request</button>
        <p class="small">This draft uses your email app. Connect a secure form service before public launch.</p>
        </form></div></section>""")


PAGES = [
    ("index.html", "index", f"Connect Enterprise Systems to ArcGIS Field Operations | {BRAND['name']}",
     "ORCSERVE queries work from enterprise systems, powers ArcGIS field workflows, and synchronizes updates back to the system of record.", home),
    ("platform.html", "platform", f"Platform | {BRAND['name']}",
     "The ORCSERVE connector framework, configuration engine, canonical model, sync engine, monitoring, and deployment.", platform),
    ("how-it-works.html", "how", f"How It Works | {BRAND['name']}",
     "See how ORCSERVE queries source data, publishes work to ArcGIS, powers field workflows, and synchronizes updates back.", how_it_works),
    ("solutions.html", "solutions", f"Solutions | {BRAND['name']}",
     "ORCSERVE supports public works, utilities, transportation, airports, campuses, telecom, and other distributed operations.", solutions),
    ("where-we-fit.html", "where", f"Where OrcServe Fits | {BRAND['name']}",
     "How OrcServe complements enterprise waste platforms, route optimization, FME, public-works asset systems, and 311/CRM.", where_we_fit),
    ("workflow-assessment.html", "assessment", f"Workflow Assessment | {BRAND['name']}",
     "Document current field workflows, identify gaps, and build a future-state roadmap with the ORCSERVE Workflow Assessment.", workflow_assessment),
    ("resources.html", "resources", f"Resources | {BRAND['name']}",
     "ORCSERVE resources for field workflow modernization, ArcGIS architecture, deployment, and enterprise integration.", resources),
    ("about.html", "about", f"About | {BRAND['name']}",
     "ORCSERVE is an independently developed integration platform connecting enterprise systems with ArcGIS field operations.", about),
    ("contact.html", "contact", f"Contact | {BRAND['name']}",
     "Request an ORCSERVE demonstration, workflow assessment, or pilot discussion.", contact),
]


def main():
    OUT.mkdir(exist_ok=True)
    # copy static assets
    assets_src = ROOT / "assets"
    assets_out = OUT / "assets"
    if assets_out.exists():
        shutil.rmtree(assets_out)
    shutil.copytree(assets_src, assets_out)
    # render pages
    for filename, slug, title, desc, fn in PAGES:
        (OUT / filename).write_text(page(slug, title, desc, fn()), encoding="utf-8")
        print(f"  wrote site/{filename}")
    print(f"\nBuilt {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
