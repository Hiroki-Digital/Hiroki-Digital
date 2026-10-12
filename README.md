# Hiroki Digital website + local SEO client tracker

```
website/                         ← upload this folder to your host
  index.html                     Homepage (SEO & Website Design Agency in Australia & New Zealand)
  web-design.html                Ad landing page + core service: website design
  digital-marketing.html         Ad landing page + core service: marketing
  google-seo.html                Ad landing page + core service: Google SEO
  services.html                  Services hub (category page)
  services/*.html                15 specialist service pages (1,000+ words each)
  areas.html                     "Areas we serve" hub (in the main menu)
  areas/*.html                   12 city pages: 8 Australian, 4 New Zealand (1,200+ words each)
  privacy.html, terms.html, accessibility.html   Legal pages (APPs, NZ Privacy Act, ACL, WCAG 2.2 AA)
  thank-you.html, 404.html
  assets/js/config.js            ← Google Sheet URL, Tag Manager ID, email
  robots.txt, sitemap.xml (36 URLs), site.webmanifest, favicons
  _headers, vercel.json          Security headers (HTTPS-only, Content Security Policy, no framing)
google-sheets/Code.gs            Apps Script that saves every form into a formatted Google Sheet
source/                          Templates and content, if you want to change NAP or copy and rebuild
Local-SEO-Client-Tracker.xlsx    One copy per client: the whole local SEO workflow as a spreadsheet
```

Lighthouse (mobile) scores in testing: 98–99 performance, 100 accessibility, 100 best practices, 100 SEO.

---

## 1. How the site follows the local SEO workflow

Hiroki Digital is treated as its own local SEO client. Service area: Australia and New Zealand.

| Workflow step | Where it's done on the site |
|---|---|
| Title tag: BEST + primary category + city + business name + services + near me (~200 chars) | Every page. e.g. "BEST SEO & Website Design Agency Sydney – looking for Google SEO, Website Design or Digital Marketing near me in Sydney? Hiroki Digital…" |
| H1 = primary category + city | "SEO & Website Design Agency in Australia & New Zealand", "… in Sydney", "Local SEO Services in Australia & New Zealand" |
| H2s = secondary categories + main services | Section headings name the services (Website Design, Google SEO & Digital Marketing Services, etc.) |
| NAP in footer on every page | Footer and every contact section. Address and phone appear automatically once you add them (step 3) |
| GBP map embedded on the homepage | Ready: shows as soon as you add the embed URL (step 3) |
| LocalBusiness schema (Advanced) | ProfessionalService + Service + BreadcrumbList + FAQPage on every page, with areaServed for AU, NZ and all 12 cities |
| At least 30 indexed pages (Advanced) | 36 indexable pages, all in sitemap.xml |
| Page hierarchy (Advanced) | Rank 1 homepage → Rank 2 services hub + 3 core service pages → Rank 3 specialist service pages |
| Areas we serve in navigation (Advanced) | "Areas we serve" in the main menu → hub → 12 city pages |
| Interlinking (Advanced) | Service pages link to 2–4 area pages in the text plus a "We also serve these areas" list. Area pages link to 3 services in the text plus a "Services we offer in [city]" section with 5 services. Homepage links to every area and the main services. Max ~8 unique destinations per page, varied anchor text, nothing footer-only |

## 2. Connect the forms to Google Sheets (about 5 minutes)

1. Go to [sheets.new](https://sheets.new) and name it **Hiroki Digital — Website Leads**.
2. **Extensions → Apps Script**, delete the sample code, paste in `google-sheets/Code.gs`, click **Save**.
3. Choose **setup** in the function dropdown, click **Run**, approve the permissions (*Advanced → Go to project* on the "unverified app" screen; it's your own script).
   This builds a formatted **Leads** tab (status dropdown, colour-coded statuses, overdue follow-ups in red, filters) and a **Dashboard** tab (leads by service, status, ad source and campaign, plus a weekly chart).
4. **Deploy → New deployment → Web app**, *Execute as: Me*, *Who has access: Anyone*. Copy the URL ending in `/exec`.
5. Paste it into `website/assets/js/config.js` → `sheetEndpoint`, then re-upload the site and send a test enquiry.

Every form on the site posts to the same sheet, with the page, UTM tags and Google/Meta/Microsoft click IDs attached. Until `sheetEndpoint` is set, forms run in preview mode (nothing is saved).

## 3. When Hiroki Digital's Google Business Profile is live

NAP must match the profile exactly, so fill these in once the profile exists. Open `source/build.py` and edit the `SITE` block:

```python
"phone": "0400 000 000",                     # exactly as on the GBP
"address": {"street": "", "locality": "", "region": "", "postcode": "", "country": "AU"},  # leave blank for a service-area business
"gbp_url": "https://maps.app.goo.gl/…",      # added to schema sameAs
"map_embed": "https://www.google.com/maps/embed?pb=…",  # GBP → Share → Embed a map → the src="" URL
```

Then rebuild: `pip install jinja2` once, then `python3 build.py` inside `source/`. The new site appears in `dist/site`; upload that instead of `website/`. The footer, contact blocks, schema and homepage map all update together.

## 4. Put the site online (GitHub Pages + GoDaddy)

The site is hosted from the `main` branch of github.com/Hiroki-Digital/Hiroki-Digital, at the repository root, on **hirokidigital.com**.

**GoDaddy DNS** (My Products → hirokidigital.com → DNS → DNS Records):

| Type | Name | Value | Notes |
|---|---|---|---|
| A | @ | 185.199.108.153 | GitHub Pages |
| A | @ | 185.199.109.153 | GitHub Pages |
| A | @ | 185.199.110.153 | GitHub Pages |
| A | @ | 185.199.111.153 | GitHub Pages |
| AAAA | @ | 2606:50c0:8000::153 | optional, IPv6 |
| AAAA | @ | 2606:50c0:8001::153 | optional, IPv6 |
| AAAA | @ | 2606:50c0:8002::153 | optional, IPv6 |
| AAAA | @ | 2606:50c0:8003::153 | optional, IPv6 |
| CNAME | www | hiroki-digital.github.io | |

**No other A records for @.** GoDaddy's "Parked" / forwarding addresses (76.223.105.230 and 13.248.243.5) must be deleted, and Domain Forwarding must be off. If they stay, a share of visitors get GoDaddy's blank parked page and GitHub can't issue the HTTPS certificate.

**GitHub** (repo → Settings → Pages): Source = Deploy from a branch, `main`, `/ (root)`, custom domain `hirokidigital.com`. Once the certificate is issued, tick **Enforce HTTPS**.

**Email records:** keep the MX record and the `autodiscover`, `email` and `lyncdiscover` CNAMEs. They run the Microsoft 365 mailbox for info@hirokidigital.com and don't affect the website.

**After a DNS change** (the first hour is normal):

1. DNS answers are cached for up to 1 hour (TTL 3600), so GitHub may still show *DNS check unsuccessful / NotServedByPagesError*, and https:// may show a certificate warning (`ERR_CERT_COMMON_NAME_INVALID`). Use `http://hirokidigital.com` meanwhile.
2. After an hour, click **Check again** on the Pages settings page.
3. Still failing, or the HTTPS box is still greyed out after the check passes? **Remove** the custom domain, wait a minute, type `hirokidigital.com` again and **Save**. That forces a fresh check and a new certificate request (normally issued within 15 minutes to a few hours, up to 24 hours).
4. When the box unlocks, tick **Enforce HTTPS**.

**Updating the site:** upload the *contents* of the `website` folder to the repo root (Add file → Upload files, or GitHub Desktop). Keep the `CNAME` file (it holds the custom domain) and `.nojekyll` (tells GitHub to serve the files as-is). GitHub Pages publishes within a minute or two.

**Security headers on GitHub Pages:** GitHub doesn't read `_headers` or `vercel.json`, so every page also carries its Content Security Policy as a `<meta>` tag. GitHub provides HTTPS once Enforce HTTPS is on. The `_headers` and `vercel.json` files only matter if you move to Netlify, Cloudflare Pages or Vercel.

After launch, add the site to Google Search Console and submit `https://hirokidigital.com/sitemap.xml`.

## 5. Ads and conversion tracking

| Ad group | Final URL | Offer |
|---|---|---|
| Website design | `/web-design.html` | Free homepage concept |
| Marketing | `/digital-marketing.html` | Free 90-day growth plan |
| Google SEO | `/google-seo.html` | Free SEO audit, ranking heatmap and keyword gap report |

Google Ads final URL suffix: `utm_source=google&utm_medium=cpc&utm_campaign={_campaign}&utm_term={keyword}&utm_content={creative}`. Count conversions on page views of `/thank-you.html`, or set `gtmId` in `config.js` and trigger tags from the `generate_lead` dataLayer event.

## 6. The client tracker spreadsheet

`Local-SEO-Client-Tracker.xlsx` turns the workflow into a per-client checklist. Make one copy per client (it imports cleanly into Google Sheets: File → Import).

- **Start Here**: client details, progress for each of the 8 milestones from the workflow checklist, Basic vs Advanced progress and a quick health check.
- **Checklist**: all 58 tasks with week, stage (Basic/Advanced), how-to, tool link and status.
- **Benchmark**: heatmap runs (week 1 vs week 11–12) and the top 10 with reviews, photos, categories and services, plus a gap analysis.
- **Website Audit**: NAP, title, H1, indexed pages, schema and map, with automatic pass/fail.
- **GBP**: categories (1 + 0–3), profile features (min 3 of 5), completeness.
- **Services**: up to 99 services with a 300-character counter for descriptions.
- **Content Plan** and **Interlinking**: page hierarchy, word counts and the 2–4 / 3–6 link rules checked automatically.
- **Citations**: the 80/20 platforms, AU and NZ directories and the additional sources list.
- **Weekly**, **Emails** (all 12 weekly emails plus the services check and client habits emails), **Rank Log**, **Blackhat** and **Prompts**.

Yellow cells are for input; grey italic rows are examples to overwrite.

## 7. Check before launch

- Turnaround and terms used in the copy: reply within one business day, homepage concept in 5 business days, 3–6 week builds, month-to-month SEO/marketing with 30 days' notice, 30 days' launch support.
- Budget ranges in each form.
- City pages describe how you work with each city and contain no invented clients or testimonials. Add real reviews and case studies as you get them.

## 8. Privacy and legal compliance (Australia & New Zealand)

The site was reviewed against the laws below on 11 October 2026. This is a practical checklist, not legal advice. Have a lawyer review the privacy policy and terms before you rely on them.

### What the site does

| Law or standard | How the site meets it |
|---|---|
| **Privacy Act 1988 (Cth) and Australian Privacy Principles** | Full privacy policy covering everything APP 1.4 requires. A collection notice under every form (APP 5) says who collects the details, why, that they're stored with Google overseas, and links to the policy. Name field accepts a pseudonym or first name (APP 2). Only name and email are required, and the browser user agent is no longer collected (APP 3). Google storage is disclosed as an overseas disclosure (APP 8). Access, correction and complaint steps include OAIC contact details (APPs 12–13). |
| **APP 11 security and retention** | HTTPS-only and Content Security Policy headers. The form endpoint checks email format, caps field lengths, rate-limits submissions (20 a minute), blocks spreadsheet formula injection and drops honeypot bots. A daily clean-up deletes enquiries after 24 months, spam after 30 days and client rows after 7 years, matching the policy. The visitor's name is never put in a URL. |
| **OAIC tracking pixel guidance (2024)** | No cookies or third-party tags by default. If you set `gtmId`, nothing loads until the visitor clicks Accept. "No thanks" is remembered and "Cookie settings" in the footer lets them change their mind. Form contents are never sent to ad platforms. |
| **Privacy Act 2020 (NZ)** | Applies because the site targets NZ businesses, and NZ has no small-business exemption. The policy covers the NZ Information Privacy Principles, breach notification and the NZ Privacy Commissioner. The forms collect information directly from the person. The policy also explains the public business information reviewed for free audits, which is relevant to the new IPP 3A indirect-collection rule (in force since 1 May 2026). |
| **Spam Act 2003 (Cth) / Unsolicited Electronic Messages Act 2007 (NZ)** | No marketing emails without consent. The policy commits to sender identification, an unsubscribe link and processing opt-outs within 5 business days. |
| **Australian Consumer Law and NZ Fair Trading Act** | Wording that implied an existing client base was rewritten as recommendations. Sample dashboards, charts and share images are labelled "sample data" or "illustration". Free offers have plain terms with no hidden conditions. No ranking guarantees. Terms of use don't exclude consumer guarantees. A trade mark notice says you're not affiliated with Google, Meta and others. |
| **Disability Discrimination Act 1992 (Cth) / WCAG 2.2 AA** | Zero violations in an automated axe-core scan of 14 key pages. Pages reflow at 320px (400% zoom), with keyboard focus and reduced-motion support. There's an accessibility statement with a feedback route. |
| **Copyright** | All graphics and copy are original. The three fonts are SIL Open Font Licence, and the licence files ship with them. |

### What you need to do

1. **Register "Hiroki Digital" as a business name with ASIC** unless you trade under your own name. It's an offence to trade under an unregistered business name. Get an ABN, then add `legal_name` and `abn` to `SITE` in `source/build.py` and rebuild. They then appear in the footer, privacy policy and terms.
2. **Check `governing_law`** in `SITE` (set to the Australian Capital Territory) matches the state or territory you're based in.
3. **Secure the Google side.** Turn on 2-step verification, keep the leads sheet private, and run `setup` once so the retention clean-up trigger is installed.
4. **Small business exemption.** If your annual turnover is $3 million or less, the Privacy Act's small business exemption probably applies to you. It was still in force as of 29 September 2026; the government has agreed in principle to remove it, but no Bill has been introduced. The site follows the APPs anyway, so you're ready either way, but you must actually do what the policy says (respond within 30 days, delete on schedule, and so on).
5. **Before turning on Google Tag Manager or a Meta pixel,** keep tags to the minimum, don't send form fields to them, and add any new tag domains to the Content Security Policy in `_headers` / `vercel.json`.
6. **Client work.** Use a written client agreement that covers how you handle their customers' data, confidentiality and offboarding (removing your access). If you use standard-form contracts with small businesses, check them against the unfair contract terms rules, which now carry penalties.
7. **Data breach plan.** If the leads sheet or a client account is compromised: contain it, assess the harm, and notify affected people and the OAIC (or NZ Privacy Commissioner) where the breach is likely to cause serious harm.
8. **Keep promises true.** Every timeframe and term on the site is a representation under the ACL: reply within one business day, concept within 5 business days, month-to-month with 30 days' notice, and 30 days' launch support. Change the copy if any of these stop being true.
9. **"BEST" in title tags** follows your workflow. Courts and the ACCC generally treat a vague superlative like this as puffery rather than a factual claim, but avoid pairing it with specific, unprovable comparisons.
10. **Make sure info@hirokidigital.com receives email** before launch. The privacy policy, forms and footer all use it, so it must work for access requests and complaints. Use GoDaddy email forwarding or a mailbox (Microsoft 365 or Google Workspace), or change `email` in `SITE` and `config.js`.
