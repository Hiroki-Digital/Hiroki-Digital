#!/usr/bin/env python3
"""Builds the Hiroki Digital static site into ../dist/site."""
import json, re, shutil, datetime, pathlib
from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "dist" / "site"
# Business details (NAP). Keep these IDENTICAL to the Google Business Profile once it exists.
# Leave address/phone empty until they're on the profile: the footer, contact blocks and schema update automatically.
SITE = {
    "url": "https://hirokidigital.com",
    "name": "Hiroki Digital",
    "email": "info@hirokidigital.com",
    "phone": "",                       # e.g. "0400 000 000" — exactly as written on the GBP
    "address": {"street": "", "locality": "", "region": "", "postcode": "", "country": "AU"},
    "area_label": "Australia & New Zealand",
    "gbp_url": "",                     # e.g. "https://maps.app.goo.gl/..." (added to schema sameAs)
    "map_embed": "",                   # GBP "Share → Embed a map" src URL; shows a map on the homepage
    "same_as": [],                     # social profile URLs
    # Legal details. Fill these in once registered; they appear in the footer and legal pages when set.
    "legal_name": "",                  # e.g. your own name (sole trader) or "Hiroki Digital Pty Ltd"
    "abn": "",                         # e.g. "12 345 678 901"
    "governing_law": "the Australian Capital Territory",   # state/territory where the business is based
    "privacy_updated": "11 October 2026",
}
VERSION = "1"
TODAY = datetime.date(2026, 10, 11)

ICONS = {
    "search": '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
    "layout": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/>',
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18h2"/>',
    "gauge": '<path d="M4 17a8 8 0 1 1 16 0"/><path d="M12 17l4.5-5"/><circle cx="12" cy="17" r="1.2"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "pen": '<path d="M4 20l4.5-1 10-10a2.1 2.1 0 0 0-3-3l-10 10L4 20z"/><path d="M13.5 7.5l3 3"/>',
    "chart": '<path d="M4 20h16"/><rect x="5.5" y="12" width="3" height="6" rx=".6"/><rect x="10.5" y="8" width="3" height="10" rx=".6"/><rect x="15.5" y="4" width="3" height="14" rx=".6"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "megaphone": '<path d="M3 10v4h3l7 5V5L6 10H3z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a7.5 7.5 0 0 1 0 11"/>',
    "shield": '<path d="M12 3l7.5 3v5.5c0 4.8-3.3 8.3-7.5 9.5-4.2-1.2-7.5-4.7-7.5-9.5V6L12 3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "doc": '<path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8l-5-5z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M21.5 20a6.5 6.5 0 0 0-3.8-5.9"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
    "cursor": '<path d="M5 3l14 7-6 2-2 6L5 3z"/><path d="M13 12l6 6"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "inbox": '<path d="M3 13l2.5-7.5A2 2 0 0 1 7.4 4h9.2a2 2 0 0 1 1.9 1.5L21 13v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5z"/><path d="M3 13h5l1.5 2.5h5L16 13h5"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3.5 17.5a2 2 0 0 0 3 3l5.8-5.8a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.5-.5-2.4 2.5-2.7z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "refresh": '<path d="M20 11a8 8 0 0 0-14.6-4.5M4 13a8 8 0 0 0 14.6 4.5"/><path d="M4 4v4h4M20 20v-4h-4"/>',
}

# ---------------------------------------------------------------- charts (drawn to one scale each)
def fmt_int(n): return f"{n:,.0f}"

def marketing_data():
    leads = [9, 11, 10, 13, 15, 14, 18, 21, 20, 24, 27, 31]
    cpl = [74, 70, 71, 64, 60, 61, 54, 49, 50, 45, 42, 39]
    clicks = [290, 330, 300, 360, 380, 350, 410, 440, 400, 450, 470, 500]
    spend = [l * c for l, c in zip(leads, cpl)]
    cur, prev = slice(8, 12), slice(4, 8)
    L, Lp = sum(leads[cur]), sum(leads[prev])
    S, Sp = sum(spend[cur]), sum(spend[prev])
    C, Cp = sum(clicks[cur]), sum(clicks[prev])
    cpl_now, cpl_prev = S / L, Sp / Lp
    cr, crp = L / C * 100, Lp / Cp * 100
    kpis = [
        {"label": "Leads", "value": fmt_int(L), "delta": f"▲ {round((L / Lp - 1) * 100)}%"},
        {"label": "Cost per lead", "value": f"${cpl_now:,.0f}", "delta": f"▼ {round((1 - cpl_now / cpl_prev) * 100)}%"},
        {"label": "Conversion rate", "value": f"{cr:.1f}%", "delta": f"▲ {cr - crp:.1f} pts"},
        {"label": "Ad spend", "value": f"${S:,.0f}", "delta": f"▲ {round((S / Sp - 1) * 100)}%"},
    ]
    # chart: bars on left axis 0–40 leads, line on right axis $0–$80 (both 5 aligned ticks)
    W, H, ml, mr, mt, mb = 560, 230, 34, 42, 12, 26
    pw, ph = W - ml - mr, H - mt - mb
    n = len(leads)
    band = pw / n
    bw = band * 0.56
    y_l = lambda v: mt + ph - v / 40 * ph
    y_r = lambda v: mt + ph - v / 80 * ph
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Sample chart: weekly leads rise from {leads[0]} to {leads[-1]} over 12 weeks while cost per lead falls from ${cpl[0]} to ${cpl[-1]}.">']
    parts.append('<g class="grid">')
    for i in range(5):
        y = y_l(i * 10)
        parts.append(f'<line x1="{ml}" x2="{W - mr}" y1="{y:.1f}" y2="{y:.1f}"/>')
    parts.append('</g><g class="axis">')
    for i in range(5):
        y = y_l(i * 10)
        parts.append(f'<text x="{ml - 8}" y="{y + 3.5:.1f}" text-anchor="end">{i * 10}</text>')
        parts.append(f'<text x="{W - mr + 8}" y="{y + 3.5:.1f}">${i * 20}</text>')
    for i in range(n):
        cx = ml + band * i + band / 2
        parts.append(f'<text x="{cx:.1f}" y="{H - 6}" text-anchor="middle">W{i + 1}</text>')
    parts.append('</g>')
    for i, v in enumerate(leads):
        x = ml + band * i + (band - bw) / 2
        y = y_l(v)
        cls = "bar bar--hot" if i >= 8 else "bar"
        parts.append(f'<rect class="{cls} anim-grow" style="--i:{i}" x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{mt + ph - y:.1f}" rx="3"/>')
    pts = [(ml + band * i + band / 2, y_r(v)) for i, v in enumerate(cpl)]
    length = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** .5 for i in range(n - 1))
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    parts.append(f'<polyline class="line anim-draw" style="--len:{length:.0f}" points="{d}"/>')
    ex, ey = pts[-1]
    parts.append(f'<circle class="dot anim-fade" cx="{ex:.1f}" cy="{ey:.1f}" r="4.5"/>')
    parts.append('</svg>')
    channels = [{"name": "Google Search", "pct": 44}, {"name": "Meta ads", "pct": 29}, {"name": "Email", "pct": 17}, {"name": "Retargeting", "pct": 10}]
    assert sum(c["pct"] for c in channels) == 100
    return {"kpis": kpis, "chart": "".join(parts), "channels": channels}

def seo_data():
    clicks = [310, 330, 360, 420, 480, 560, 690, 820, 960, 1110, 1290, 1480]
    W, H, ml, mr, mt, mb = 300, 210, 38, 10, 16, 24
    pw, ph = W - ml - mr, H - mt - mb
    n = len(clicks)
    x = lambda i: ml + pw * i / (n - 1)
    y = lambda v: mt + ph - v / 1500 * ph
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Illustration: organic clicks per month grow from {clicks[0]} to {fmt_int(clicks[-1])} over 12 months.">',
             '<defs><linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2D3BD1" stop-opacity=".28"/><stop offset="1" stop-color="#2D3BD1" stop-opacity="0"/></linearGradient></defs>',
             '<g class="grid">']
    for v in (0, 500, 1000, 1500):
        parts.append(f'<line x1="{ml}" x2="{W - mr}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
    parts.append('</g><g class="axis">')
    for v in (0, 500, 1000, 1500):
        parts.append(f'<text x="{ml - 8}" y="{y(v) + 3.5:.1f}" text-anchor="end">{fmt_int(v)}</text>')
    for i in (0, 3, 6, 9, 11):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        parts.append(f'<text x="{x(i):.1f}" y="{H - 6}" text-anchor="{anchor}">{"Month 1" if i == 0 else i + 1}</text>')
    parts.append('</g>')
    pts = [(x(i), y(v)) for i, v in enumerate(clicks)]
    line = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    area = f"M{pts[0][0]:.1f},{y(0):.1f} L" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f" L{pts[-1][0]:.1f},{y(0):.1f}Z"
    length = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** .5 for i in range(n - 1))
    parts.append(f'<path class="area anim-fade" d="{area}"/>')
    parts.append(f'<polyline class="line anim-draw" style="--len:{length:.0f};stroke:var(--indigo)" points="{line}"/>')
    ex, ey = pts[-1]
    parts.append(f'<circle class="dot anim-fade" style="stroke:var(--indigo)" cx="{ex:.1f}" cy="{ey:.1f}" r="4.5"/>')
    parts.append('</svg>')
    return {"chart": "".join(parts), "last": fmt_int(clicks[-1])}

VITALS = [
    {"name": "LCP", "what": "Largest Contentful Paint · loading", "target": "≤ 2.5 s", "good": 2.5 / 6 * 100, "poor": 4 / 6 * 100, "at": 1.8 / 6 * 100, "scale": "6 s"},
    {"name": "INP", "what": "Interaction to Next Paint · responsiveness", "target": "≤ 200 ms", "good": 200 / 800 * 100, "poor": 500 / 800 * 100, "at": 120 / 800 * 100, "scale": "800 ms"},
    {"name": "CLS", "what": "Cumulative Layout Shift · visual stability", "target": "≤ 0.1", "good": 0.1 / 0.4 * 100, "poor": 0.25 / 0.4 * 100, "at": 0.04 / 0.4 * 100, "scale": "0.4"},
]

# ---------------------------------------------------------------- page content
HOME_FAQ = [
    {"q": "Do I need all three services?", "a": ["No. Many businesses start with one, usually a new website or SEO, and add the others later. The free audit tells you which one will make the biggest difference first."]},
    {"q": "How much does it cost?", "a": ["Websites are quoted at a fixed price after the free audit, based on the pages and features you need. SEO and marketing are monthly retainers with no lock-in contract. You'll always see the price before any work starts."]},
    {"q": "How long until I see results?", "a": ["Most websites launch in 3 to 6 weeks. Search ads can bring enquiries within the first week or two. SEO is slower to build, usually 3 to 6 months for meaningful traffic growth, but it keeps working without a cost per click."]},
    {"q": "Will I own my website and accounts?", "a": ["Yes. Your domain, website, Google Ads, Analytics and Business Profile accounts are set up in your name. If you ever move on, everything goes with you."]},
    {"q": "Who will I be working with?", "a": ["A small team, with one main contact from your first call to your monthly reports. No account managers passing messages along."]},
    {"q": "Which areas do you work in?", "a": ["We work with businesses across Australia and New Zealand. Everything runs over video calls, email and shared reports, so location is never a problem."]},
]

WEB = {
    "crumb": "website-design",
    "h1_kw": "Website Design Agency in Australia & New Zealand",
    "more_title": "More website design services",
    "areas_title": "Website design across Australia & New Zealand",
    "h1": 'Websites that look sharp and <span class="hl">bring in enquiries</span>.',
    "lede": "We design and build custom, mobile-first websites for small businesses. Fast to load, easy to update and built around one job: turning visitors into customers.",
    "offer": {"label": "free offer for new clients", "title": "See your new homepage before you pay a cent",
              "items": ["<strong>A custom homepage concept</strong> designed around your brand and customers",
                        "<strong>A 10-point review</strong> of your current site's speed, mobile layout and SEO",
                        "<strong>A fixed-price quote</strong> with a clear timeline. Keep the concept either way."]},
    "ticks": ["Reply within one business day", "Fixed-price quotes", "You own everything"],
    "demo": {"crumb": "responsive design", "h2": "Responsive Website Design for Every Screen",
             "p": "Most visitors arrive on a phone. We design mobile-first, then scale up to tablet and desktop, so every layout feels made for the device it's on.",
             "points": [{"icon": "phone", "t": "Mobile-first layouts", "d": "Thumb-friendly buttons, readable text and tap-to-call on every page."},
                        {"icon": "gauge", "t": "Fast on 4G", "d": "We aim for the main content to load in under 2.5 seconds on a mid-range phone."},
                        {"icon": "users", "t": "Accessible to everyone", "d": "Built to WCAG 2.2 AA: good contrast, keyboard friendly, screen-reader ready."}]},
    "incl_h2": "Website Design Services Included in Every Project",
    "incl_p": "No add-on surprises. Every website project includes the strategy, design, build and setup below.",
    "incl": [
        {"icon": "doc", "t": "Strategy and sitemap", "d": "We map your pages around what customers search for and what you want them to do."},
        {"icon": "spark", "t": "Custom design", "d": "No off-the-shelf templates. A look built for your brand, from type to buttons."},
        {"icon": "phone", "t": "Responsive build", "d": "Hand-tuned for phones, tablets and desktops, and tested on real devices."},
        {"icon": "gauge", "t": "Speed optimisation", "d": "Compressed images, lean code and quality hosting to pass Core Web Vitals."},
        {"icon": "search", "t": "On-page SEO", "d": "Titles, meta descriptions, headings, schema markup and an XML sitemap."},
        {"icon": "target", "t": "Conversion tracking", "d": "GA4 plus form and call tracking, so you know where every enquiry came from."},
        {"icon": "pen", "t": "Copywriting help", "d": "We shape your words so every page is clear, specific and persuasive."},
        {"icon": "layout", "t": "Easy editing", "d": "Update text, images and blog posts yourself, without touching code."},
        {"icon": "shield", "t": "Launch support", "d": "30 days of fixes and tweaks after launch, plus a recorded walkthrough."},
    ],
    "steps_h2": "Our Website Design Process",
    "steps": [
        {"t": "Discovery call", "d": "20 minutes on your business, customers and goals, and what your current site gets right or wrong.", "when": "day 1"},
        {"t": "Free homepage concept", "d": "A custom design for your homepage plus a fixed quote and timeline for the full site.", "when": "within 5 business days"},
        {"t": "Design and build", "d": "We design the remaining pages, build the site and share a private preview for your feedback.", "when": "2–4 weeks"},
        {"t": "Launch and handover", "d": "We go live, submit your sitemap to Google, set up tracking and show you how to edit.", "when": "launch day"},
    ],
    "promise": {"icon": "key", "t": "You own it. All of it.", "d": "Your domain, hosting, website files and Google accounts are set up in your name. If you ever leave, everything leaves with you."},
    "faq_h2": "Website Design FAQs",
    "cta": {"h2": "Ready to see your new homepage?", "p": "Send your details and we'll have a custom concept back to you within 5 business days. Free, and yours to keep.", "btn": "Get my free concept"},
}
WEB_FAQ = [
    {"q": "How much does a website cost?", "a": ["You get a fixed quote after the discovery call, based on the number of pages and features such as online booking, payments or a blog. The price we quote is the price you pay."]},
    {"q": "How long does it take?", "a": ["Most small-business websites launch in 3 to 6 weeks. Larger sites with online stores or custom features take longer, and your quote includes a timeline."]},
    {"q": "Can you redesign my existing website?", "a": ["Yes. We keep what's working, such as pages that already rank on Google, and set up redirects so you don't lose search traffic when the new site goes live."]},
    {"q": "Will I be able to update it myself?", "a": ["Yes. You'll be able to change text, swap images and publish posts from a simple editor. We include a recorded walkthrough so you can refer back to it."]},
    {"q": "Which platform do you build on?", "a": ["It depends on how you'll use the site. We usually recommend WordPress or Webflow for sites you'll edit often, and Shopify for online stores. We'll explain the trade-offs before you decide."]},
    {"q": "Do you write the content?", "a": ["We can. Usually you give us the facts about your business and we turn them into clear, search-friendly page copy. You review and approve everything before launch."]},
]

MKT = {
    "crumb": "digital-marketing",
    "h1_kw": "Digital Marketing Agency in Australia & New Zealand",
    "more_title": "More marketing services",
    "areas_title": "Digital marketing across Australia & New Zealand",
    "h1": 'Marketing that brings in <span class="hl">customers</span>, not just clicks.',
    "lede": "We plan, launch and manage campaigns across Google, Meta and email, then report on what matters: leads, sales and what each one cost you.",
    "offer": {"label": "free offer for new clients", "title": "Get a free 90-day growth plan",
              "items": ["<strong>A review of your current marketing</strong>: ad accounts, website and tracking",
                        "<strong>A channel and budget plan</strong> showing where your next dollar should go",
                        "<strong>Three campaign ideas</strong> ready to launch, with audiences and messaging"]},
    "ticks": ["Month-to-month, no lock-in", "Reports in plain English", "Reply within one business day"],
    "demo": {"crumb": "campaign management", "h2": "Campaign Management: Every Dollar Tracked",
             "p": "You get a live dashboard showing leads, cost per lead and which channels are working, so budget moves to what performs.",
             "points": [{"icon": "chart", "t": "Live dashboard", "d": "Leads, spend and cost per lead across every channel, updated daily."},
                        {"icon": "refresh", "t": "Weekly optimisation", "d": "We test audiences, offers and creative, then shift budget to the winners."},
                        {"icon": "clock", "t": "Monthly review call", "d": "Thirty minutes on results, learnings and next month's plan."}]},
    "incl_h2": "Digital Marketing Strategy, Campaign Management & Brand Growth",
    "incl_p": "From positioning to the final click, we handle the strategy and the day-to-day work of running your campaigns.",
    "incl": [
        {"icon": "target", "t": "Marketing strategy", "d": "Positioning, audience and offer work so your campaigns say the right thing to the right people."},
        {"icon": "search", "t": "Google Ads", "d": "Search, Performance Max and local campaigns built around high-intent keywords."},
        {"icon": "megaphone", "t": "Meta ads", "d": "Facebook and Instagram campaigns with creative tested against real results."},
        {"icon": "mail", "t": "Email and automation", "d": "Welcome series, nurture flows and newsletters that keep leads warm."},
        {"icon": "cursor", "t": "Landing pages and CRO", "d": "A dedicated page for each campaign, tested to lift conversion rates."},
        {"icon": "spark", "t": "Creative and copy", "d": "Ad copy, graphics and short video edits that match your brand."},
        {"icon": "link", "t": "Tracking and attribution", "d": "GA4, conversion tags and call tracking, so each lead traces back to its source."},
        {"icon": "trend", "t": "Brand growth", "d": "Consistent messaging and visuals that build recognition across every channel."},
        {"icon": "chart", "t": "Monthly reporting", "d": "One page in plain English: results, learnings and next month's plan."},
    ],
    "steps_h2": "Our Campaign Management Process",
    "steps": [
        {"t": "Audit and plan", "d": "We review your accounts, website and tracking, then agree goals, channels and budget.", "when": "week 1"},
        {"t": "Build campaigns", "d": "Audiences, ads, landing pages and conversion tracking, all checked before a dollar is spent.", "when": "week 2"},
        {"t": "Launch and learn", "d": "Campaigns go live. We test offers, audiences and creative, and cut what doesn't work.", "when": "weeks 3–6"},
        {"t": "Scale what works", "d": "Budget moves to the best performers, and we add new channels once the core is profitable.", "when": "ongoing"},
    ],
    "promise": {"icon": "key", "t": "Month-to-month, always.", "d": "No lock-in contracts. We keep your business by getting results, and your ad accounts, audiences and data stay in your name."},
    "faq_h2": "Digital Marketing FAQs",
    "cta": {"h2": "Find out where your next customers will come from", "p": "Get a free 90-day growth plan with the channels, budget and campaigns we'd use for your business.", "btn": "Get my free growth plan"},
}
MKT_FAQ = [
    {"q": "What budget do I need?", "a": ["Your growth plan includes a recommended starting budget based on your market, competition and goals. Many local businesses start with a modest test budget and scale up once cost per lead is proven."]},
    {"q": "Which platforms do you manage?", "a": ["Google Ads, Meta (Facebook and Instagram), LinkedIn for B2B, and email platforms such as Mailchimp and Klaviyo."]},
    {"q": "How quickly will I see results?", "a": ["Search ads can bring enquiries in the first week or two. Expect 4 to 8 weeks of testing before campaigns are fully optimised and cost per lead settles."]},
    {"q": "Do you lock me into a contract?", "a": ["No. All marketing plans are month-to-month. You can pause or cancel with 30 days' notice."]},
    {"q": "Do you create the ads?", "a": ["Yes. We write the copy, design the graphics and edit short videos. If you have brand assets or photos, we'll use them."]},
    {"q": "How do you report on results?", "a": ["You get a live dashboard, a one-page monthly report and a 30-minute review call. Every report leads with leads, cost per lead and revenue where we can track it."]},
]

SEO = {
    "crumb": "google-seo",
    "h1_kw": "Google SEO Agency in Australia & New Zealand",
    "more_title": "More Google SEO services",
    "areas_title": "Google SEO across Australia & New Zealand",
    "h1": 'Climb Google and get found by customers <span class="hl">already searching</span>.',
    "lede": "We fix what's holding your site back, target the keywords your customers actually use and build the authority that moves you up the rankings, month after month.",
    "offer": {"label": "free offer for new clients", "title": "Free SEO audit, ranking heatmap and keyword gap report",
              "items": ["<strong>A ranking heatmap</strong> showing where you appear in Google Maps across your service area",
                        "<strong>A keyword gap report</strong> showing searches your competitors win and you don't",
                        "<strong>A prioritised fix list</strong> you can hand to any developer, or to us"]},
    "ticks": ["No lock-in contracts", "Monthly ranking reports", "White-hat methods only"],
    "demo": {"crumb": "rankings", "h2": "Google Ranking Improvements: From Page Two to the Top Three",
             "p": "Most clicks go to the first few results. We focus on the keywords that bring buyers, then work to move you up the page and into the map pack.",
             "points": [{"icon": "trend", "t": "Ranking improvements", "d": "Weekly position tracking for the keywords that drive enquiries."},
                        {"icon": "pin", "t": "Local map pack", "d": "Google Business Profile optimisation to show up in local results."},
                        {"icon": "chart", "t": "Organic traffic growth", "d": "More visitors from Google that you don't pay per click for."}]},
    "incl_h2": "Google SEO Techniques We Use, All White-Hat",
    "incl_p": "Our local SEO program works through your Google Business Profile, your website and your citations, in that order, because that's where the easiest wins are.",
    "incl": [
        {"icon": "tool", "t": "Ranking heatmap benchmark", "d": "A grid of ranking checks across your service area for your main keyword, plus a review of the top 10 competitors."},
        {"icon": "pin", "t": "Google Business Profile", "d": "One sharp primary category, up to three secondary ones and a fully completed profile."},
        {"icon": "doc", "t": "Services and descriptions", "d": "A full services list on your profile, with descriptions of up to 300 characters for your top 20."},
        {"icon": "search", "t": "On-page SEO", "d": "Title tags with your main service and city, one H1 per page, service-led H2s and your NAP in the footer."},
        {"icon": "code", "t": "Schema and map", "d": "LocalBusiness structured data and your Google map embedded on the homepage."},
        {"icon": "pen", "t": "Service and area pages", "d": "A page for each core service and each area you serve, linked so Google understands what you do and where."},
        {"icon": "link", "t": "Citations", "d": "Bing Places, Apple Business Connect, Foursquare, Yelp and the directories that rank for your keyword."},
        {"icon": "refresh", "t": "Weekly posts and photos", "d": "A Google Business Profile post and fresh photos every week, plus a simple review process."},
        {"icon": "chart", "t": "Rankings reports", "d": "A new heatmap and a plain-English report, so you can see exactly what moved."},
    ],
    "steps_h2": "Our 12-Week Local SEO Program",
    "steps": [
        {"t": "Benchmark and profile", "d": "Ranking heatmap and competitor review, then categories, services, bookings link and FAQs on your Google Business Profile.", "when": "weeks 1–4"},
        {"t": "On-page SEO", "d": "Title tags, H1s, H2s, NAP, schema and map, then service and area pages linked together.", "when": "weeks 5–8"},
        {"t": "Citations", "d": "Core citations, then the directories that rank for your keyword.", "when": "weeks 9–10"},
        {"t": "Rankings review", "d": "A new heatmap compared with week one, and the plan for what comes next.", "when": "weeks 11–12"},
    ],
    "promise": {"icon": "shield", "t": "We'll never promise you the #1 spot.", "d": "Nobody controls Google's rankings, and agencies that guarantee #1 often use tactics that get sites penalised. We promise clear work, honest reporting and steady progress on the keywords that bring in business."},
    "faq_h2": "Google SEO FAQs",
    "cta": {"h2": "Find out what's stopping you from ranking", "p": "Get a free ranking heatmap and keyword gap report, with a prioritised list of fixes.", "btn": "Get my free SEO audit"},
}
SEO_FAQ = [
    {"q": "How long does SEO take to work?", "a": ["Most sites see early ranking movement within 6 to 12 weeks and meaningful traffic growth in 4 to 6 months. Competitive industries and brand-new websites can take longer."]},
    {"q": "Can you guarantee a #1 ranking?", "a": ["No, and be careful with anyone who does. Google's own guidance warns against SEO providers that guarantee rankings. We commit to the work, the reporting and the keywords that matter to your business."]},
    {"q": "What is local SEO?", "a": ["Local SEO helps you appear when people search for a service near them, including the map results. It covers your Google Business Profile, reviews, local citations and location pages."]},
    {"q": "Do I need a new website for SEO?", "a": ["Not usually. Most sites can be improved where they are. If your current site has deeper problems, the audit will show what they cost you and whether a rebuild is worth it."]},
    {"q": "What's in the monthly report?", "a": ["Keyword rankings, organic traffic and enquiries from Search Console and GA4, the work completed that month and what we're doing next, all on one page."]},
    {"q": "Is SEO better than Google Ads?", "a": ["They do different jobs. Ads bring enquiries quickly, and you pay for every click. SEO takes longer but builds traffic you don't pay per click for. We can run both from one plan."]},
]

BUDGETS = {
    "home": ("Budget", ["Under $2,000", "$2,000–$5,000", "$5,000–$10,000", "$10,000+", "Not sure yet"]),
    "web": ("Project budget", ["Under $3,000", "$3,000–$6,000", "$6,000–$12,000", "$12,000+", "Not sure yet"]),
    "marketing": ("Monthly marketing budget", ["Under $1,500 / month", "$1,500–$3,000 / month", "$3,000–$7,500 / month", "$7,500+ / month", "Not sure yet"]),
    "seo": ("Monthly SEO budget", ["Under $1,000 / month", "$1,000–$2,000 / month", "$2,000–$4,000 / month", "$4,000+ / month", "Not sure yet"]),
}

OFFER_NAME = {"home": "growth plan", "web": "homepage concept", "marketing": "90-day growth plan", "seo": "SEO audit"}
def form_cfg(key, **kw):
    label, opts = BUDGETS[key]
    kw.setdefault("offer", OFFER_NAME[key])
    return dict(budget_label=label, budget=opts, **kw)

# ---------------------------------------------------------------- site structure
from markupsafe import Markup, escape
from content.services_web import SERVICES_WEB
from content.services_mkt import SERVICES_MKT
from content.services_seo import SERVICES_SEO
from content.areas_au import AREAS_AU
from content.areas_nz import AREAS_NZ

SERVICES = SERVICES_WEB + SERVICES_MKT + SERVICES_SEO
AREAS = AREAS_AU + AREAS_NZ
from content.extra_services import SVC_EXTRA
from content.extra_services import SVC_EXTRA_FAQS
from content.extra_areas import AREA_EXTRA, AREA_MORE
for _sv in SERVICES:
    _sv.update(SVC_EXTRA[_sv["slug"]])
    _sv["faqs"] = list(_sv["faqs"]) + SVC_EXTRA_FAQS[_sv["slug"]]
for _ar in AREAS:
    _x = AREA_EXTRA[_ar["slug"]]
    _ar["checklist"], _ar["start"] = _x["checklist"], _x["start"]
    _m = AREA_MORE[_ar["slug"]]
    _ar["searches"], _ar["edge"] = _m["searches"], _m["edge"]
    _ar["faqs"] = list(_ar["faqs"]) + _x["faqs"] + [_m["faq"]]
SVC = {x["slug"]: x for x in SERVICES}
AREA = {x["slug"]: x for x in AREAS}
REGION = "Australia & New Zealand"

CORE = {
    "web": dict(href="web-design.html", label="Website design", icon="layout", offer="homepage concept",
                cta="Get a free homepage concept", cta_h2="See your new homepage before you commit",
                cta_p="Tell us about your business and we'll design a custom homepage concept for you, free. Keep it whether or not you go ahead.",
                note="Custom, mobile-first websites built to rank and convert.",
                summary="Modern, responsive websites that load fast, look sharp on every screen and turn visitors into enquiries.",
                form=dict(budget="web", service="Website design", message_label="What should your new website do better?",
                          message_ph="Look more professional, get more bookings, work on phones…", button="Send me my free concept", title="Get your free homepage concept")),
    "marketing": dict(href="digital-marketing.html", label="Marketing services", icon="megaphone", offer="90-day growth plan",
                cta="Get a free growth plan", cta_h2="Get a free 90-day growth plan",
                cta_p="Tell us about your goals and current marketing. We'll map the channels, budget and campaigns we'd use for your business.",
                note="Google Ads, Meta ads and email, managed around cost per lead.",
                summary="Strategy, campaign management and creative across Google Ads, Meta and email, measured on leads and cost per lead.",
                form=dict(budget="marketing", service="Marketing services", message_label="What are your growth goals for the next 3 months?",
                          message_ph="More leads, lower cost per lead, launch a new service…", button="Get my free growth plan", title="Get your free 90-day growth plan")),
    "seo": dict(href="google-seo.html", label="Google SEO", icon="search", offer="SEO audit and ranking heatmap",
                cta="Get a free SEO audit", cta_h2="Get a free SEO audit and ranking heatmap",
                cta_p="Tell us your main service and area. We'll show you where you rank across your area today and the quickest wins to move up.",
                note="Local SEO, Google Business Profile, on-page SEO and citations.",
                summary="White-hat local SEO that gets you into the Google map pack and grows organic traffic, month after month.",
                form=dict(budget="seo", service="Google SEO", message_label="Which services or keywords do you want to rank for?",
                          message_ph="e.g. accountant near me, tax returns, BAS agent…", button="Get my free SEO audit", title="Get your free SEO audit", website_label="Website to audit")),
}
LP_SLUG_TO_CORE = {"web": "web", "marketing": "marketing", "seo": "seo"}

def ref_href(ref, b):
    kind, slug = ref.split(":", 1) if ":" in ref else ("s", ref)
    if kind == "c":
        return b + CORE[slug]["href"]
    if kind == "s":
        assert slug in SVC, f"unknown service {slug}"
        return f"{b}services/{slug}.html"
    if kind == "a":
        assert slug in AREA, f"unknown area {slug}"
        return f"{b}areas/{slug}.html"
    raise ValueError(ref)

def ref_link(ref, b, note=True):
    kind, slug = ref.split(":", 1) if ":" in ref else ("s", ref)
    if kind == "c":
        c = CORE[slug]
        return dict(href=ref_href(ref, b), label=c["label"], note=c["note"] if note else "", icon=c["icon"])
    if kind == "a":
        a = AREA[slug]
        return dict(href=ref_href(ref, b), label=a["name"], note=f"{a['region']}, {a['country']}" if note else "", icon="pin")
    sv = SVC[slug]
    return dict(href=ref_href(ref, b), label=sv["name"], note=sv["tagline"] if note else "", icon=sv["icon"])

LINK_RE = re.compile(r"\[\[([sca]):([\w-]+)\|([^\]]+)\]\]")
def xl(text, b=""):
    out, last = [], 0
    for m in LINK_RE.finditer(text):
        out.append(escape(text[last:m.start()]))
        out.append(Markup('<a href="%s">%s</a>') % (ref_href(m[1] + ":" + m[2], b), m[3]))
        last = m.end()
    out.append(escape(text[last:]))
    return Markup("").join(out)

def slugify(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def area_links(b, note=True):
    groups = []
    for country, lst in (("Australia", AREAS_AU), ("New Zealand", AREAS_NZ)):
        groups.append(dict(name=country, areas=[dict(href=f"{b}areas/{a['slug']}.html", label=a["name"], region=a["region"] if a["region"] != a["name"] else country,
                                                    note=", ".join(a["suburbs"][:4])) for a in lst]))
    return groups

# ---------------------------------------------------------------- schema
ORG_ID = SITE["url"] + "/#org"
def org():
    o = {
        "@type": "ProfessionalService", "@id": ORG_ID, "name": SITE["name"], "url": SITE["url"] + "/",
        "logo": SITE["url"] + "/assets/img/logo-512.png", "image": SITE["url"] + "/assets/og/og-home.png",
        "email": SITE["email"],
        "description": "SEO, website design and digital marketing agency for small businesses across Australia and New Zealand.",
        "areaServed": [{"@type": "Country", "name": "Australia"}, {"@type": "Country", "name": "New Zealand"}] +
                      [{"@type": "City", "name": a["name"]} for a in AREAS],
        "knowsAbout": ["Website design", "Search engine optimisation", "Local SEO", "Google Business Profile", "Google Ads", "Digital marketing"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": sv["name"], "url": f"{SITE['url']}/services/{sv['slug']}.html"}} for sv in SERVICES]},
    }
    if SITE["phone"]: o["telephone"] = SITE["phone"]
    if SITE["address"]["street"]:
        a = SITE["address"]
        o["address"] = {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["locality"], "addressRegion": a["region"], "postalCode": a["postcode"], "addressCountry": a["country"]}
    same = [u for u in [SITE["gbp_url"]] + SITE["same_as"] if u]
    if same: o["sameAs"] = same
    return o

def faq_schema(items, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": " ".join(q["a"])}} for q in items]}

def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + u} for i, (n, u) in enumerate(trail)]}

def service_schema(url, name, desc, area_served, offer=None):
    d = {"@type": "Service", "@id": url + "#service", "name": name, "serviceType": name, "description": desc, "url": url,
         "provider": {"@id": ORG_ID}, "areaServed": area_served}
    if offer: d["offers"] = {"@type": "Offer", "name": offer, "price": "0", "priceCurrency": "AUD"}
    return d

COUNTRIES_SERVED = [{"@type": "Country", "name": "Australia"}, {"@type": "Country", "name": "New Zealand"}]
def dumps(o): return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
def qa(items): return [{"q": q, "a": [a]} for q, a in items]

# ---------------------------------------------------------------- pages
HOME_TITLE = "BEST SEO & Website Design Agency Australia & New Zealand – looking for Google SEO, Website Design or Digital Marketing near me? Hiroki Digital is the place to be"
PAGES = [
    dict(tpl="index.html", out="index.html", slug="home", path="/", depth=0,
         title=HOME_TITLE,
         description="SEO, website design and digital marketing agency for businesses across Australia and New Zealand. Rank in Google Maps and get more enquiries.",
         og="og-home", og_alt="Hiroki Digital: SEO and website design agency in Australia and New Zealand",
         og_title="Hiroki Digital: SEO & Website Design Agency in Australia & New Zealand",
         faqs=HOME_FAQ,
         form=form_cfg("home", title="Tell us about your business", sub="Takes about a minute. We reply within one business day.", choose_service=True,
                       message_label="What would you like more of?", message_ph="More calls from Google, a site that converts, better ads…", button="Send my free plan request")),
    dict(tpl="web-design.html", out="web-design.html", slug="web", path="/web-design.html", depth=0, lp=WEB, faqs=WEB_FAQ,
         title="BEST Website Design Agency Australia & New Zealand – looking for Custom Website Design, WordPress or Shopify Web Design near me? Hiroki Digital builds sites that bring in enquiries",
         description="Website design agency for Australian and NZ businesses. Custom, mobile-first websites that load fast and rank. Get a free homepage concept first.",
         og="og-web-design", og_alt="Hiroki Digital website design: a responsive site on desktop and phone",
         og_title="Website Design Agency in Australia & New Zealand | Hiroki Digital",
         cta_href="#get-started", cta_label="Free homepage concept", mcta="Get my free homepage concept", body_class="has-mcta",
         form=form_cfg("web", title="Get your free homepage concept", sub="Takes about a minute. No obligation.", service="Website design",
                       message_label="What should your new website do better?", message_ph="Look more professional, get more bookings, work on phones…", button="Send me my free concept")),
    dict(tpl="digital-marketing.html", out="digital-marketing.html", slug="marketing", path="/digital-marketing.html", depth=0, lp=MKT, faqs=MKT_FAQ,
         title="BEST Digital Marketing Agency Australia & New Zealand – looking for Google Ads Management, Facebook & Instagram Ads or Email Marketing near me? Hiroki Digital",
         description="Digital marketing agency for Australian and NZ businesses. Google Ads, Meta ads and email managed around cost per lead. Free 90-day growth plan.",
         og="og-marketing", og_alt="Hiroki Digital marketing services: a campaign dashboard with leads rising",
         og_title="Digital Marketing Agency in Australia & New Zealand | Hiroki Digital",
         cta_href="#get-started", cta_label="Free growth plan", mcta="Get my free growth plan", body_class="has-mcta",
         form=form_cfg("marketing", title="Get your free 90-day growth plan", sub="Takes about a minute. No obligation.", service="Marketing services",
                       message_label="What are your growth goals for the next 3 months?", message_ph="More leads, lower cost per lead, launch a new service…", button="Get my free growth plan")),
    dict(tpl="google-seo.html", out="google-seo.html", slug="seo", path="/google-seo.html", depth=0, lp=SEO, faqs=SEO_FAQ,
         title="BEST Google SEO Agency Australia & New Zealand – looking for Local SEO, Google Business Profile Optimisation or Google Maps Ranking near me? Hiroki Digital",
         description="Google SEO agency for Australian and NZ businesses. Heatmap benchmarking, Google Business Profile, on-page SEO and citations. Free SEO audit.",
         og="og-seo", og_alt="Hiroki Digital Google SEO: a search result climbing to position one",
         og_title="Google SEO Agency in Australia & New Zealand | Hiroki Digital",
         cta_href="#get-started", cta_label="Free SEO audit", mcta="Get my free SEO audit", body_class="has-mcta",
         form=form_cfg("seo", title="Get your free SEO audit", sub="Takes about a minute. No obligation.", service="Google SEO", website_label="Website to audit",
                       message_label="Which services or keywords do you want to rank for?", message_ph="e.g. accountant near me, tax returns, BAS agent…", button="Get my free SEO audit")),
    dict(tpl="services-hub.html", out="services.html", slug="services", path="/services.html", depth=0,
         title="BEST Digital Marketing Services Australia & New Zealand – Website Design, Google SEO, Local SEO, Google Ads & Email Marketing near me | Hiroki Digital",
         description="All Hiroki Digital services: website design, Google SEO, local SEO, Google Business Profile, Google Ads, Meta ads and email marketing in Australia and NZ.",
         og="og-home", og_alt="Hiroki Digital services", og_title="Website Design, SEO & Digital Marketing Services | Hiroki Digital",
         crumbs=[("services", None)]),
    dict(tpl="areas-hub.html", out="areas.html", slug="areas", path="/areas.html", depth=0,
         title="Areas We Serve – SEO, Website Design & Digital Marketing in Sydney, Melbourne, Brisbane, Perth, Adelaide, Canberra, Auckland, Wellington & more | Hiroki Digital",
         description="Hiroki Digital serves businesses across Australia and New Zealand, with local SEO pages for Sydney, Melbourne, Brisbane, Perth, Auckland and more.",
         og="og-home", og_alt="Hiroki Digital areas we serve", og_title="Areas We Serve Across Australia & New Zealand | Hiroki Digital",
         crumbs=[("areas", None)]),
    dict(tpl="thank-you.html", out="thank-you.html", slug="ty", path="/thank-you.html", depth=0, noindex=True,
         title="Thanks, we've got your details | Hiroki Digital", description="Thanks for getting in touch with Hiroki Digital. We'll reply within one business day.",
         og="og-home", og_alt="Hiroki Digital"),
    dict(tpl="privacy.html", out="privacy.html", slug="privacy", path="/privacy.html", depth=0,
         title="Privacy Policy | Hiroki Digital", description="How Hiroki Digital collects, uses, stores and protects personal information under the Australian Privacy Principles and NZ Privacy Act 2020.",
         og="og-home", og_alt="Hiroki Digital"),
    dict(tpl="terms.html", out="terms.html", slug="terms", path="/terms.html", depth=0,
         title="Website Terms of Use | Hiroki Digital", description="The terms that apply when you use the Hiroki Digital website and request a free audit, homepage concept or growth plan.",
         og="og-home", og_alt="Hiroki Digital"),
    dict(tpl="accessibility.html", out="accessibility.html", slug="a11y", path="/accessibility.html", depth=0,
         title="Accessibility Statement | Hiroki Digital", description="How the Hiroki Digital website meets WCAG 2.2 AA, and how to tell us about an accessibility problem or request another format.",
         og="og-home", og_alt="Hiroki Digital"),
    dict(tpl="404.html", out="404.html", slug="404", path="/404.html", noindex=True, abs=True, depth=0,
         title="Page not found | Hiroki Digital", description="This page doesn't exist. Find Hiroki Digital's website design, marketing and Google SEO services here.",
         og="og-home", og_alt="Hiroki Digital"),
]
OG_BY_CORE = {"web": "og-web-design", "marketing": "og-marketing", "seo": "og-seo"}

for sv in SERVICES:
    PAGES.append(dict(tpl="service.html", out=f"services/{sv['slug']}.html", slug="svc", key=sv["slug"], path=f"/services/{sv['slug']}.html", depth=1,
                      title=sv["title"], description=sv["description"], og=OG_BY_CORE[sv["parent"]], og_alt=sv["h1"],
                      og_title=f"{sv['h1']} | Hiroki Digital", faqs=qa(sv["faqs"]), parent_key=sv["parent"],
                      crumbs=[("services", "../services.html"), (sv["slug"], None)]))
for ar in AREAS:
    PAGES.append(dict(tpl="area.html", out=f"areas/{ar['slug']}.html", slug="area", key=ar["slug"], path=f"/areas/{ar['slug']}.html", depth=1,
                      title=ar["title"], description=ar["description"], og="og-home", og_alt=ar["h1"],
                      og_title=f"{ar['h1']} | Hiroki Digital", faqs=qa(ar["faqs"]),
                      form=form_cfg("home", title="Tell us about your business", sub="Takes about a minute. We reply within one business day.", choose_service=True,
                                    message_label=f"Which parts of {ar['name']} do you serve?", message_ph="Suburbs, towns or regions, and what you'd like more of…", button="Send my free plan request"),
                      crumbs=[("areas", "../areas.html"), (ar["slug"], None)]))

MAIN_SERVICES = ["local-seo", "google-business-profile-optimisation", "google-ads-management", "website-redesign", "seo-content-writing", "facebook-instagram-ads"]

def page_context(p):
    depth = p.get("depth", 0)
    b = "/" if p.get("abs") else "../" * depth
    home = "/" if p.get("abs") else (b or "./")
    url = SITE["url"] + p["path"]
    ctx = dict(page=p, faqs=p.get("faqs"), form=p.get("form"), b=b, home=home,
               home_anchor="" if p["slug"] == "home" else home)
    graph = [org()]
    if p["slug"] == "home":
        ctx["main_services"] = [ref_link(s, b) for s in MAIN_SERVICES]
        ctx["countries"] = area_links(b)
        graph += [{"@type": "WebSite", "@id": SITE["url"] + "/#website", "url": SITE["url"] + "/", "name": SITE["name"], "inLanguage": "en-AU", "publisher": {"@id": ORG_ID}},
                  faq_schema(p["faqs"], url)]
    elif p["slug"] in CORE:
        ck = p["slug"]; c = CORE[ck]
        ctx["lp"] = p["lp"]
        ctx["children"] = [ref_link(sv["slug"], b, note=False) for sv in SERVICES if sv["parent"] == ck]
        ctx["areas"] = [ref_link("a:" + a, b, note=False) for a in {"web": ["sydney", "melbourne", "brisbane", "auckland", "wellington"],
                                                                   "marketing": ["sydney", "melbourne", "perth", "auckland", "christchurch"],
                                                                   "seo": ["sydney", "brisbane", "canberra", "auckland", "hamilton"]}[ck]]
        offer = {"web": "Free homepage concept", "marketing": "Free 90-day growth plan", "seo": "Free SEO audit and ranking heatmap"}[ck]
        graph += [service_schema(url, p["lp"]["h1_kw"].replace(" in Australia & New Zealand", ""), p["description"], COUNTRIES_SERVED, offer),
                  crumbs_schema([("Home", "/"), (c["label"], p["path"])]), faq_schema(p["faqs"], url)]
    elif p["slug"] == "services":
        ctx["groups"] = [dict(href=b + CORE[k]["href"], label=CORE[k]["label"], icon=CORE[k]["icon"], summary=CORE[k]["summary"], cta=CORE[k]["cta"],
                              children=[ref_link(sv["slug"], b) for sv in SERVICES if sv["parent"] == k]) for k in ("web", "marketing", "seo")]
        graph += [crumbs_schema([("Home", "/"), ("Services", p["path"])])]
    elif p["slug"] == "areas":
        ctx["countries"] = [dict(c, blurb=("We build local pages, heatmaps and citation plans for businesses in Australia's capitals and largest regional cities."
                                            if c["name"] == "Australia" else "We work with businesses across New Zealand, from Auckland to Christchurch, with NZ directories and local pages."))
                            for c in area_links(b)]
        graph += [crumbs_schema([("Home", "/"), ("Areas we serve", p["path"])])]
    elif p["slug"] == "svc":
        sv = SVC[p["key"]]; c = CORE[sv["parent"]]
        ctx["s"] = sv
        ctx["parent"] = dict(c, href=b + c["href"])
        ctx["related"] = [ref_link(r, b, note=False) for r in sv["related"]]
        ctx["areas"] = [ref_link("a:" + a, b, note=False) for a in sv["areas"]]
        f = c["form"]
        extra = {"website_label": f["website_label"]} if "website_label" in f else {}
        ctx["form"] = form_cfg(f["budget"], title=f["title"], sub="Takes about a minute. No obligation.", service=f["service"],
                               message_label=f["message_label"], message_ph=f["message_ph"], button=f["button"], **extra)
        graph += [service_schema(url, sv["name"], sv["description"], COUNTRIES_SERVED),
                  crumbs_schema([("Home", "/"), ("Services", "/services.html"), (sv["name"], p["path"])]), faq_schema(p["faqs"], url)]
    elif p["slug"] == "area":
        ar = AREA[p["key"]]
        ctx["a"] = ar
        ctx["services"] = [ref_link(r, b) for r in ar["services"][:5]]   # workflow: 3–5 links in "Services we offer here"
        ctx["nearby"] = [ref_link("a:" + n, b, note=False) for n in ar["nearby"]]
        city = {"@type": "City", "name": ar["name"], "containedInPlace": {"@type": "Country", "name": ar["country"]}}
        graph += [service_schema(url, f"SEO and website design in {ar['name']}", ar["description"], city),
                  crumbs_schema([("Home", "/"), ("Areas we serve", "/areas.html"), (ar["name"], p["path"])]), faq_schema(p["faqs"], url)]
    p["schema"] = dumps({"@context": "https://schema.org", "@graph": graph})
    return ctx

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True, trim_blocks=True, lstrip_blocks=True)
    env.globals.update(icons=ICONS, site=SITE, v=VERSION, year=TODAY.year, updated=TODAY.strftime("%-d %B %Y"))
    env.filters["xl"] = xl
    env.filters["slug"] = slugify
    mkt, seo = marketing_data(), seo_data()
    dials = [{"v": 95, "label": "Performance"}, {"v": 100, "label": "Accessibility"}, {"v": 100, "label": "Best practices"}, {"v": 100, "label": "SEO"}]
    for p in PAGES:
        assert len(p["title"]) <= 200, (p["out"], len(p["title"]))
        assert 70 <= len(p["description"]) <= 160, (p["out"], len(p["description"]))
        ctx = page_context(p)
        ctx.update(mkt=mkt, seo=seo, dials=dials, vitals=VITALS)
        html = env.get_template(p["tpl"]).render(**ctx)
        html = re.sub(r"\n\s*\n+", "\n", html)
        out = OUT / p["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    # assets
    css = (ROOT / "site.css").read_text()
    css = css.replace('url("../img/favicon-mark.svg")', 'url("data:image/svg+xml,' + MARK_MINI + '")')
    (OUT / "assets/css").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/css/site.css").write_text(minify_css(css))
    (OUT / "assets/js").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "site.js", OUT / "assets/js/site.js")
    shutil.copy(ROOT / "config.js", OUT / "assets/js/config.js")
    shutil.copytree(ROOT / "fonts", OUT / "assets/fonts")
    if (ROOT / "static").exists():
        shutil.copytree(ROOT / "static", OUT, dirs_exist_ok=True)
    # seo files
    pri = {"home": "1.0", "web": "0.9", "marketing": "0.9", "seo": "0.9", "services": "0.8", "areas": "0.8", "svc": "0.7", "area": "0.7", "privacy": "0.2", "terms": "0.2", "a11y": "0.2"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in PAGES:
        if not p.get("noindex"):
            sm.append(f"  <url><loc>{SITE['url']}{p['path']}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{pri.get(p['slug'], '0.5')}</priority></url>")
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": "Hiroki Digital", "short_name": "Hiroki", "start_url": "/", "display": "standalone",
        "background_color": "#F4F5FA", "theme_color": "#2D3BD1",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/assets/img/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, indent=2))
    print("built", len(PAGES), "pages,", sum(1 for p in PAGES if not p.get("noindex")), "indexable →", OUT)

MARK_MINI = ("%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='8 6 32 34'%3E%3Crect x='11' y='18' width='7' height='20' rx='1.2' fill='%232D3BD1'/%3E"
             "%3Crect x='30' y='16.5' width='7' height='21.5' rx='1.2' fill='%232D3BD1'/%3E%3Crect x='30' y='9' width='7' height='5.5' rx='1.2' fill='%23F2B200'/%3E"
             "%3Cpath d='M18 30 L30 23 L30 28.5 L18 35.5Z' fill='%232D3BD1'/%3E%3C/svg%3E")

def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    css = re.sub(r"\n+", "\n", css)
    return css.strip() + "\n"

if __name__ == "__main__":
    build()
