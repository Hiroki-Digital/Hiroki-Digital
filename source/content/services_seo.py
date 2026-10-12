"""Rank 3 service pages under Google SEO (parent: google-seo.html)."""

SERVICES_SEO = [
dict(
    slug="local-seo", name="Local SEO", parent="seo", icon="pin",
    h1="Local SEO Services in Australia & New Zealand",
    title="BEST Local SEO Agency Australia & New Zealand – looking for Local SEO, Google Maps Ranking or Google Business Profile Optimisation near me? Hiroki Digital gets you into the map pack",
    description="Local SEO for Australian and NZ businesses. Heatmap benchmarking, Google Business Profile optimisation, on-page SEO and citations to rank in the map pack.",
    tagline="Get into the Google map pack for the searches that bring in customers.",
    timeline="a 12-week program, then monthly",
    intro=[
        "When someone searches 'plumber near me' or 'accountant in Brisbane', Google shows a map with three businesses before any normal results. Those three get most of the calls. Local SEO is the work that gets your business into that map pack, across the whole area you serve.",
        "Hiroki Digital runs a structured 12-week local SEO program for businesses in Australia and New Zealand. It covers your Google Business Profile, your website and your citations, in that order, because that's where the easiest wins usually are. It's all white-hat work that follows Google's guidelines, so your profile is never put at risk.",
    ],
    sections=[
        dict(h2="Step one: benchmark where you rank today", paras=[
            "Every client starts with a ranking heatmap. We place a grid of points over your service area and check where you rank for your main keyword from each point. It's common for a business to rank well near its office and disappear a few kilometres away.",
            "The heatmap gives us a starting point to measure against. We also compare the top 10 businesses in your area on review count, photos, categories and services, and look for fake or keyword-stuffed listings that are taking spots they shouldn't.",
        ]),
        dict(h2="What the 12-week local SEO program includes", paras=[
            "We work through the program in two passes. The basic pass covers the changes that move rankings for most businesses. If you're not in the top three after a few weeks, the advanced pass builds out your website's content and citations.",
        ], bullets=[
            ("Google Business Profile", "One main category and up to three supporting ones, a complete profile, a full services list with descriptions, a bookings link and FAQs."),
            ("On-page SEO", "Title tags with your main service and city, one H1 per page, service-led H2s, your name, address and phone in the footer, and an embedded Google map."),
            ("Schema markup", "LocalBusiness structured data so Google can read your details reliably."),
            ("Service and area pages", "A page for each core service and each area you serve, linked together so Google understands what you do and where."),
            ("Citations", "Consistent listings on Bing Places, Apple Business Connect, Foursquare, Yelp and the directories that rank for your keyword."),
            ("Weekly activity", "A Google Business Profile post and geotagged photos every week, and a simple process for collecting reviews."),
        ]),
        dict(h2="What we need from you", paras=[
            "Local SEO works best as a partnership. We handle the technical work and the content, and ask for two habits from you.",
        ], bullets=[
            ("Ask every happy customer for a review", "A steady stream of Google reviews matters more than a burst every few months. We'll give you a link and a message to send."),
            ("Send us photos of your work", "Real photos of jobs, your team and your premises, every week. We upload them to your profile with location data."),
        ]),
    ],
    steps=[
        ("Benchmark", "Ranking heatmap, competitor review and a check for easy wins.", "week 1"),
        ("Google Business Profile", "Categories, services, descriptions, bookings link, FAQs and photos.", "weeks 2–4"),
        ("On-page SEO and content", "Titles, H1s, NAP, schema, map, then service and area pages.", "weeks 5–8"),
        ("Citations and review", "Core citations and directories, then a new heatmap to compare.", "weeks 9–12"),
    ],
    local="Your service area decides your keyword targets. A business in [[a:brisbane|Brisbane]] might target the CBD and several surrounding suburbs, while one in [[a:auckland|Auckland]] might focus on the North Shore. The program leans heavily on [[s:google-business-profile-optimisation|Google Business Profile optimisation]], since the profile is what appears in the map.",
    faqs=[
        ("How long does local SEO take to work?", "Many businesses see movement in the map pack within the first four to eight weeks, once the Google Business Profile changes are in. Competitive areas and categories take longer, which is when the advanced content and citation work comes in."),
        ("Do I need a physical address to rank locally?", "You need a real, verified Google Business Profile. Service-area businesses can hide their address and list the areas they serve instead."),
        ("What is a ranking heatmap?", "A grid of ranking checks across your area, showing where you appear in the map results from each point. It's how we measure progress beyond a single ranking position."),
        ("Can you get rid of fake listings competing with me?", "If a listing is clearly fake, such as a keyword-stuffed name at an address where the business doesn't exist, we report it to Google with evidence. We only report listings we're sure about."),
        ("Is this white-hat SEO?", "Yes. Everything we do follows Google's guidelines. Shortcuts like fake reviews or fake addresses can get a profile suspended, and we don't use them."),
    ],
    related=["c:seo", "google-business-profile-optimisation", "link-building"],
    areas=["brisbane", "auckland", "sydney", "canberra"],
),
dict(
    slug="google-business-profile-optimisation", name="Google Business Profile Optimisation", parent="seo", icon="pin",
    h1="Google Business Profile Optimisation in Australia & New Zealand",
    title="BEST Google Business Profile Optimisation Agency Australia & New Zealand – looking for GBP Optimisation, Google Maps Listing Setup or Google My Business Help near me? Hiroki Digital",
    description="Google Business Profile optimisation for Australian and NZ businesses. Categories, services, descriptions, photos and posts that lift your map rankings.",
    tagline="A complete, accurate profile that Google wants to show in the map.",
    timeline="2–3 weeks, then weekly posts",
    intro=[
        "Your Google Business Profile, once called Google My Business, is often the first thing customers see. It's the listing in the map results, with your reviews, photos, hours and phone number. It's also the biggest single lever in local SEO.",
        "Hiroki Digital optimises Google Business Profiles for businesses across Australia and New Zealand. We compare your profile with the businesses ranking above you, then fix the gaps one by one.",
    ],
    sections=[
        dict(h2="Categories: fewer and sharper", paras=[
            "Your primary category is one of the most important ranking factors in the map. Many businesses dilute it by adding every category that seems related. We usually limit profiles to one primary category and up to three secondary ones, chosen by checking what the top-ranking businesses in your area use.",
            "Categories that overlap too much, or that drift away from what you want to rank for, both weaken the signal. A surveyor listed as 'Surveyor', 'Property surveyor' and 'Valuer' is usually better off with one or two.",
        ]),
        dict(h2="Services, descriptions and profile features", paras=[
            "Most profiles list a handful of services. The businesses that rank often list dozens. Google allows a large services list, and each service is another chance to match a specific search.",
        ], bullets=[
            ("A full services list", "We compile services from your business and from top competitors, remove duplicates and confirm the list with you."),
            ("Service descriptions", "A clear description of up to 300 characters for your 20 most important services."),
            ("Profile features", "Address or service area, website, phone, hours and a bookings link pointing to your contact page."),
            ("FAQs and description", "A business description and common questions answered in your own words."),
            ("Photos with location data", "Real photos of your work, team and premises, uploaded weekly."),
            ("Weekly posts", "Short updates, offers and project spotlights that keep the profile active."),
        ]),
        dict(h2="Dealing with fake competitor listings", paras=[
            "Some map results are fake: a keyword-stuffed name, an address in a shopping centre where the business doesn't exist and a website with no address. These listings are often built to be rented out to other businesses. When we're certain a listing breaks Google's guidelines, we report it through 'Suggest an edit' with evidence. We never report real businesses, because false reports harm everyone's credibility with Google.",
        ]),
    ],
    steps=[
        ("Audit", "Your profile compared with the top 20 in your area for your main keyword.", "week 1"),
        ("Categories and features", "Categories trimmed, profile features completed and bookings link added.", "week 1–2"),
        ("Services and FAQs", "Full services list, top 20 descriptions and FAQs added.", "weeks 2–3"),
        ("Weekly activity", "Posts and geotagged photos every week, plus review requests.", "ongoing"),
    ],
    local="Profiles behave differently in dense cities and spread-out regions. In [[a:melbourne|Melbourne]] you may compete with dozens of businesses within a few kilometres, while in [[a:hamilton|Hamilton]] your service area might cover surrounding towns as well. Profile work is the core of our [[s:local-seo|local SEO program]].",
    faqs=[
        ("Is Google My Business the same as Google Business Profile?", "Yes. Google renamed Google My Business to Google Business Profile. It's the same listing that appears in Google Search and Maps."),
        ("How many categories should my profile have?", "Usually one primary and up to three secondary categories. We check what the top-ranking businesses in your area use before deciding."),
        ("Should I add keywords to my business name?", "No. Your profile name should match your real business name. Adding keywords breaks Google's guidelines and can lead to suspension."),
        ("Do I need to give you access to my profile?", "Yes. You add us as a manager, which you can remove at any time. You stay the owner."),
        ("How often should I post on my profile?", "Once a week is a good rhythm. Posts keep the profile active and give customers a reason to choose you."),
    ],
    related=["c:seo", "local-seo", "seo-content-writing"],
    areas=["melbourne", "hamilton", "gold-coast", "christchurch"],
),
dict(
    slug="technical-seo-audit", name="Technical SEO Audit", parent="seo", icon="tool",
    h1="Technical SEO Audit Services in Australia & New Zealand",
    title="BEST Technical SEO Audit Agency Australia & New Zealand – looking for an SEO Audit, Website Health Check or Indexing & Schema Fixes near me? Hiroki Digital",
    description="Technical SEO audits for Australian and NZ websites. Indexing, crawl errors, speed, schema and on-page issues found, prioritised and fixed.",
    tagline="Find out exactly what's stopping Google from ranking your site.",
    timeline="audit in 1–2 weeks",
    intro=[
        "A technical SEO audit checks whether Google can find, crawl, understand and trust your website. Small technical problems, such as pages blocked from indexing, duplicate content or missing schema, can hold back every other piece of SEO work.",
        "Hiroki Digital audits websites for businesses across Australia and New Zealand and turns the findings into a prioritised fix list. You can hand it to your developer, or have us make the fixes.",
    ],
    sections=[
        dict(h2="What we check in a technical SEO audit", paras=[], bullets=[
            ("Indexed pages", "A site: search and Search Console data to see how many pages Google has indexed. Most local businesses need at least 30 useful, indexed pages to compete."),
            ("Crawl errors and redirects", "Broken links, redirect chains, 404 pages and blocked resources."),
            ("Title tags and headings", "Whether each page targets a clear service and location, with one H1 and logical H2s."),
            ("NAP consistency", "Your business name, address and phone shown on the site and matching your Google Business Profile."),
            ("Schema markup", "LocalBusiness, Service, FAQ and Breadcrumb structured data, checked in the Schema.org validator."),
            ("Speed and Core Web Vitals", "Mobile load times and page experience issues."),
            ("Mobile usability", "Layout, tap targets and font sizes on phones."),
            ("Duplicate and thin content", "Pages that compete with each other or don't give Google enough to rank."),
        ]),
        dict(h2="Common easy wins", paras=[
            "Small-business websites often share the same quick fixes. The homepage title doesn't mention the main service or city. The H1 is a slogan instead of a description. The footer has no address or phone number. There's no LocalBusiness schema, no embedded map and only a handful of indexed pages.",
            "Each of these takes minutes to fix and gives Google clearer signals about what you do and where. We list them first so you see progress quickly, then move on to the deeper issues.",
        ]),
        dict(h2="What you receive", paras=[], bullets=[
            ("Audit report", "Every issue, why it matters and how to fix it, in plain language."),
            ("Priority list", "Fixes ranked by impact and effort, easy wins first."),
            ("Walkthrough call", "We go through the findings and answer questions."),
            ("Optional implementation", "We make the fixes for you, then re-check."),
        ]),
    ],
    steps=[
        ("Crawl", "A full crawl of your site and a review of Search Console data.", "days 1–3"),
        ("Analyse", "Indexing, on-page, schema, speed and content checks.", "days 3–7"),
        ("Report", "Findings and a prioritised fix list.", "week 2"),
        ("Fix", "Optional implementation and a follow-up check.", "weeks 2–4"),
    ],
    local="Audits often find location signals missing entirely. A business serving [[a:perth|Perth]] or [[a:wellington|Wellington]] should say so in its titles, headings, footer and schema. Speed issues found in the audit feed straight into [[s:website-speed-optimisation|speed optimisation]].",
    faqs=[
        ("What's the difference between a technical SEO audit and the free SEO audit?", "The free audit is a quick review of your biggest opportunities. A full technical audit crawls every page and covers indexing, schema, speed and content in depth."),
        ("How many pages should my website have indexed?", "For most local businesses, at least 30 useful pages, made up of service pages, area pages and helpful content. Competitive markets often need more."),
        ("Do I need access to Google Search Console?", "It helps a lot. If you don't have it set up, we'll set it up and verify it for you."),
        ("Can my developer make the fixes?", "Yes. The report explains each fix clearly enough for any developer to follow."),
        ("How often should I audit my website?", "Once a year, and after any redesign, platform change or big drop in traffic."),
    ],
    related=["c:seo", "website-speed-optimisation", "seo-content-writing"],
    areas=["perth", "wellington", "adelaide", "sydney"],
),
dict(
    slug="link-building", name="Link Building & Citations", parent="seo", icon="link",
    h1="Link Building & Citation Services in Australia & New Zealand",
    title="BEST Link Building Agency Australia & New Zealand – looking for Local Citations, White-Hat Backlinks or Directory Listings near me? Hiroki Digital builds links that last",
    description="White-hat link building and local citations for Australian and NZ businesses. Consistent listings and relevant links that build trust with Google.",
    tagline="Consistent citations and relevant links from sites Google already trusts.",
    timeline="core citations in 2–4 weeks, links ongoing",
    intro=[
        "Google looks at which trusted websites mention and link to your business. Citations, meaning listings of your name, address and phone, confirm you're a real local business. Links from relevant sites show that others vouch for you.",
        "Hiroki Digital builds citations and links for businesses across Australia and New Zealand using white-hat methods only. No paid link networks and no spam, just listings and links a real business should have.",
    ],
    sections=[
        dict(h2="The 80/20 of citations", paras=[
            "A small number of platforms do most of the work. We set these up first, with your name, address and phone exactly matching your website and Google Business Profile.",
        ], bullets=[
            ("Bing Places for Business", "Feeds Bing search and maps, and other services that use Bing data."),
            ("Apple Business Connect", "Controls how you appear in Apple Maps and Siri on iPhones."),
            ("Foursquare", "A location data source used by many apps and platforms."),
            ("Yelp", "A widely used review and listing platform."),
            ("Major local directories", "Such as Yellow Pages, TrueLocal and Hotfrog in Australia, and Yellow and Finda in New Zealand."),
        ]),
        dict(h2="Finding the citations that matter for your keyword", paras=[
            "The best citation opportunities are the directories Google already ranks for your keyword. We search your main keyword and its variations, note every directory or list in the top 20 results and get you listed on them. If Google ranks those sites for your search, it considers them relevant.",
            "We also review the sites linking to the top competitors in your map results. Google's profile panel and backlink tools show where competitors are listed, and we fill the gaps where you're missing. Industry associations, local business groups, suppliers and community sponsorships are often the most valuable links of all.",
        ]),
        dict(h2="What's included", paras=[], bullets=[
            ("Citation audit", "Existing listings found and inconsistent details fixed."),
            ("Core citations", "The 80/20 platforms set up and verified with you."),
            ("Keyword directory research", "Directories ranking for your keywords, listed and prioritised."),
            ("Competitor link gap", "Sites linking to competitors where you could also appear."),
            ("Monthly link report", "New citations and links, with their status."),
        ]),
    ],
    steps=[
        ("Audit", "Existing citations and links, and any inconsistent details.", "week 1"),
        ("Core citations", "Bing, Apple, Foursquare, Yelp and key directories.", "weeks 1–3"),
        ("Keyword directories", "Listings on directories ranking for your keywords.", "weeks 3–6"),
        ("Ongoing links", "Competitor gaps, associations and local partnerships.", "ongoing"),
    ],
    local="Directories differ between countries and even cities. A trades business in [[a:sydney|Sydney]] has different options from one in [[a:christchurch|Christchurch]], so research always starts with your own search results. Citations are one part of our [[s:local-seo|local SEO program]].",
    faqs=[
        ("What is a citation?", "Any online mention of your business name, address and phone number, usually in a directory or listing. Consistent citations help Google trust your business details."),
        ("Do you buy links?", "No. Paid link schemes break Google's guidelines and can harm your rankings. We build citations and earn links through legitimate listings, associations and partnerships."),
        ("Why does NAP consistency matter?", "If your name, address or phone differ between listings, Google is less confident about your details. Consistent NAP across your site, profile and citations removes that doubt."),
        ("Do I need to help verify listings?", "Sometimes. Some platforms send a code by email, phone or post to the business, so we'll ask you to forward it."),
        ("How many citations do I need?", "Quality matters more than quantity. The core platforms plus the directories ranking for your keywords cover most of the value."),
    ],
    related=["c:seo", "local-seo", "technical-seo-audit"],
    areas=["sydney", "christchurch", "brisbane", "auckland"],
),
dict(
    slug="seo-content-writing", name="SEO Content Writing", parent="seo", icon="pen",
    h1="SEO Content Writing in Australia & New Zealand",
    title="BEST SEO Content Writing Agency Australia & New Zealand – looking for SEO Copywriting, Service Pages or Location Pages near me? Hiroki Digital writes content that ranks",
    description="SEO content writing for Australian and NZ businesses. Service pages, location pages and articles that build topical and local authority with Google.",
    tagline="Service and location pages that show Google what you do and where you do it.",
    timeline="4–8 pages a month",
    intro=[
        "To rank for a search, you need a page that answers it. Most small-business websites have a homepage, an about page and a contact page, which leaves Google very little to work with. SEO content writing builds out the pages that prove your expertise and your local presence.",
        "Hiroki Digital writes service pages, location pages and supporting articles for businesses across Australia and New Zealand. Every page is planned around a real search, written for people first and linked into the rest of your site.",
    ],
    sections=[
        dict(h2="Building topical authority", paras=[
            "Topical authority means covering your field thoroughly. A skincare clinic that has a page for each treatment, such as microneedling, chemical peels and acne treatment, looks more expert to Google than one with a single 'treatments' page.",
            "We structure content in a clear hierarchy: your homepage, a services page, then a page for each core service. Each service page answers what it is, who it's for, how it works, what it costs to consider and common questions, in 1,000 to 2,000 words of useful copy.",
        ]),
        dict(h2="Building local authority", paras=[
            "Local authority proves you work in the areas you say you do. We create an 'Areas we serve' page and a page for each key suburb, town or region, written with real local detail and without pretending you have an office you don't.",
        ], bullets=[
            ("Hyperlocal detail", "Suburbs, landmarks, local conditions and the questions people in that area ask."),
            ("Services offered there", "Links to the services most relevant to each area."),
            ("Directions and contact", "How to reach you, your service radius and a clear call to action."),
            ("Internal links", "Service pages link to area pages and back, with natural, varied anchor text."),
        ]),
        dict(h2="How we write", paras=[
            "We start with research: what your customers search, what the top-ranking pages cover and what questions they leave unanswered. We use AI tools to speed up drafting, but every page is planned, edited and fact-checked by a person, using details from your business. Pages include FAQs, schema recommendations and suggested images with alt text.",
        ]),
    ],
    steps=[
        ("Content map", "Your service and area pages planned, with keywords for each.", "week 1"),
        ("Research and outline", "Searches, competitor pages and an outline for each page.", "week 2"),
        ("Write and review", "Drafts sent for your approval, with your expertise added.", "weeks 2–4"),
        ("Publish and link", "Pages published, interlinked and submitted to Google.", "weeks 4–6"),
    ],
    local="Location pages need real knowledge of the area. A page for [[a:gold-coast|Gold Coast]] customers reads very differently from one for [[a:canberra|Canberra]], because the suburbs, industries and questions differ. Every new page is checked as part of our [[s:technical-seo-audit|technical SEO]] process before it goes live.",
    faqs=[
        ("How long should a service page be?", "Long enough to answer the question fully. For most service pages that's 1,000 to 2,000 words, including FAQs. Thin pages rarely rank."),
        ("Do you use AI to write content?", "We use AI to speed up research and first drafts. Every page is planned, edited and checked by a person, and includes real details from your business."),
        ("Will location pages get me penalised?", "Not when they're genuinely useful. Pages copied with only the suburb name changed can be treated as doorway pages. Ours are written for each area with local detail."),
        ("Do I need to provide information?", "A short interview and your service details are enough. You review each page before it's published."),
        ("How many pages will I need?", "Most local businesses need at least 30 indexed pages to compete, made up of service pages, area pages and helpful articles."),
    ],
    related=["c:seo", "local-seo", "wordpress-website-design"],
    areas=["gold-coast", "canberra", "melbourne", "auckland"],
),
]
