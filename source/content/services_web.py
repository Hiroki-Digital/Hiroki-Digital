"""Rank 3 service pages under Website design (parent: web-design.html).
Link syntax inside text: [[a:slug|anchor]] area page, [[s:slug|anchor]] service page, [[c:web|anchor]] core page."""

SERVICES_WEB = [
dict(
    slug="website-redesign", name="Website Redesign", parent="web", icon="refresh",
    h1="Website Redesign Services in Australia & New Zealand",
    title="BEST Website Redesign Agency Australia & New Zealand – looking for a Website Redesign, SEO-safe Migration or Modern Responsive Website near me? Hiroki Digital",
    description="Website redesign for Australian and NZ businesses. Keep your rankings, fix slow and dated pages, and turn more visitors into enquiries. Free homepage concept.",
    tagline="A modern website that keeps the Google rankings you've already earned.",
    timeline="3–6 weeks for most small-business sites",
    intro=[
        "Hiroki Digital redesigns websites for small and growing businesses across Australia and New Zealand. We replace slow, dated or hard-to-edit sites with fast, mobile-first designs that make it obvious what you do, where you do it and how to get in touch.",
        "A redesign is also the moment most businesses lose search traffic. Pages get renamed, content gets cut and nobody sets up redirects. We plan the move around your existing rankings first, so the new site starts with the visibility the old one built up.",
    ],
    sections=[
        dict(h2="Signs your website needs a redesign", paras=[
            "Most owners know their site feels old. The clearer signal is what visitors do on it. If people arrive from Google or ads and leave without calling or filling in a form, the site is costing you money every week it stays live.",
        ], bullets=[
            ("It's hard to use on a phone", "Text is tiny, buttons are cramped and the phone number isn't one tap away."),
            ("It loads slowly", "Large images and old plugins push load times past three seconds, and visitors give up."),
            ("You can't update it yourself", "Simple changes need a developer, so the site falls further out of date."),
            ("It doesn't say where you work", "No suburbs, no service areas and no address details for Google to match to local searches."),
            ("Enquiries have dropped", "Traffic looks steady, but calls and form submissions don't."),
        ]),
        dict(h2="How we protect your SEO during a redesign", paras=[
            "Before we change anything, we record what Google has indexed. We run a site: search, export every URL from your current site and note which pages bring in traffic and enquiries. Those pages keep their content, or move to a new address with a permanent 301 redirect.",
            "We also carry over the on-page basics that already work, such as title tags, headings and internal links, then improve them. Every new page gets a title tag with your main service and location, one clear H1, structured data and a place in the XML sitemap. After launch we submit the sitemap in Search Console and watch for crawl errors for 30 days.",
        ]),
        dict(h2="What's included in a website redesign", paras=[], bullets=[
            ("Content and URL audit", "A map of every existing page, what to keep, what to merge and where each one redirects."),
            ("Custom design", "A design system built for your brand: type, colours, buttons and page layouts."),
            ("Mobile-first build", "Layouts designed for phones first, then scaled up for tablets and desktops."),
            ("Local SEO foundations", "Name, address and phone in the footer, service-area pages and LocalBusiness schema."),
            ("Speed work", "Compressed images, lean code and good hosting so pages pass Core Web Vitals."),
            ("Tracking", "GA4, form tracking and call tracking, so you can compare enquiries before and after."),
        ]),
    ],
    steps=[
        ("Audit the current site", "We list every URL, its traffic and rankings, and what each page needs to keep.", "week 1"),
        ("Homepage concept", "A free homepage design so you can see the new direction before committing.", "week 1–2"),
        ("Design and build", "Remaining pages, redirects and content updates on a private preview link.", "weeks 2–5"),
        ("Launch and monitor", "Go live, submit the sitemap and watch rankings and crawl errors for 30 days.", "launch + 30 days"),
    ],
    local="We redesign websites for businesses anywhere from [[a:sydney|Sydney's suburbs]] to [[a:christchurch|Christchurch]], and every redesign includes the local signals that help you rank in your own area. If your site has slipped down the map results, pair the redesign with [[s:local-seo|local SEO work]] so the new pages and your Google Business Profile tell the same story.",
    faqs=[
        ("Will I lose my Google rankings if I redesign my website?", "Not if the move is planned. We keep pages that rank, redirect any URL that changes and carry over the on-page elements that work. Small ranking movements in the first few weeks are normal and usually settle once Google recrawls the site."),
        ("How long does a website redesign take?", "Most small-business redesigns take 3 to 6 weeks from the discovery call to launch. Sites with online stores, booking systems or a lot of content take longer, and your quote includes a timeline."),
        ("Can you keep my existing content?", "Yes. We review every page and keep what works, rewrite what's thin or out of date, and add the service and area pages that help you rank locally."),
        ("Do I need a new domain name?", "No. We rebuild the site on your existing domain, which keeps the history and authority it has built up with Google."),
        ("Can you redesign a site built on Wix or Squarespace?", "Yes. We'll recommend whether to stay on your current platform or move to WordPress, Webflow or Shopify, based on how you'll edit and grow the site."),
    ],
    related=["c:web", "wordpress-website-design", "website-speed-optimisation"],
    areas=["sydney", "melbourne", "christchurch", "perth"],
),
dict(
    slug="wordpress-website-design", name="WordPress Website Design", parent="web", icon="layout",
    h1="WordPress Website Design in Australia & New Zealand",
    title="BEST WordPress Website Design Agency Australia & New Zealand – looking for WordPress Web Design, Custom Themes or WordPress SEO near me? Hiroki Digital builds fast WordPress sites",
    description="Custom WordPress websites for Australian and NZ businesses. Fast, secure, easy to edit and built for local SEO. Get a free homepage concept first.",
    tagline="Custom WordPress sites that load fast and are easy for your team to update.",
    timeline="3–6 weeks",
    intro=[
        "WordPress runs a large share of the web because it's flexible and easy to edit. It also has a reputation for slow, plugin-heavy sites that break after updates. Hiroki Digital builds WordPress websites that keep the easy editing and drop the bloat.",
        "Every site is designed for your business, built on a lightweight theme with only the plugins it needs, and set up for local SEO from day one. You get a site your team can update in minutes, and one that Google can crawl and understand.",
    ],
    sections=[
        dict(h2="Why choose WordPress for your business website", paras=[
            "WordPress suits businesses that publish often, need lots of service and location pages, or want full control of their site and hosting. You own the files, you can move hosts whenever you like, and almost any feature you need has a reliable, well-supported option.",
        ], bullets=[
            ("Easy editing", "Change text, images and pages in a visual editor, without touching code."),
            ("Built for content", "Service pages, area pages and blog posts are simple to add as you grow."),
            ("SEO control", "Full control over title tags, headings, URLs, schema and redirects."),
            ("No platform lock-in", "Your site, your hosting and your data, all in your name."),
        ]),
        dict(h2="How we keep WordPress sites fast and secure", paras=[
            "Speed problems on WordPress usually come from heavy page builders, oversized images and plugins that load scripts on every page. We use a lean theme and the block editor, compress and lazy-load images, and only load scripts where they're used.",
            "For security, we set up managed hosting with daily backups, automatic minor updates, a firewall and limited admin accounts. Your team gets an editor login with the access it needs, and we keep the administrator keys safe.",
        ]),
        dict(h2="What's included in a WordPress website", paras=[], bullets=[
            ("Custom design", "A unique design built around your brand and customers, not a bought theme."),
            ("Reusable blocks", "Pre-styled blocks for services, FAQs, testimonials and calls to action, so new pages stay on brand."),
            ("Local SEO setup", "Title tags, H1s, NAP in the footer, LocalBusiness schema and an XML sitemap."),
            ("Contact forms", "Forms that send to your inbox and a Google Sheet, with spam protection."),
            ("Training", "A recorded walkthrough showing your team how to edit pages and publish posts."),
        ]),
    ],
    steps=[
        ("Discovery call", "Your goals, pages, features and who will edit the site.", "day 1"),
        ("Homepage concept", "A free design of your homepage, plus a fixed quote and timeline.", "within 5 business days"),
        ("Design and build", "All pages built in WordPress on a private staging site for review.", "2–4 weeks"),
        ("Launch and training", "Go live, connect analytics and Search Console, and train your team.", "launch day"),
    ],
    local="We build WordPress sites for businesses in [[a:melbourne|Melbourne]], [[a:auckland|Auckland]] and everywhere in between. Each one is ready for [[s:seo-content-writing|SEO content]], so adding a new service or suburb page is a ten-minute job rather than a developer request.",
    faqs=[
        ("Is WordPress good for SEO?", "Yes, when it's set up properly. WordPress gives you full control over titles, headings, URLs, schema and redirects. Most WordPress SEO problems come from slow themes and duplicate pages, which we avoid in the build."),
        ("Will I be able to edit the site myself?", "Yes. You'll edit pages in the WordPress block editor using blocks we've styled for your brand, and you'll get a recorded walkthrough to refer back to."),
        ("Do you use page builders like Elementor or Divi?", "We avoid heavy page builders because they slow sites down. We use the native block editor with custom blocks, which keeps editing simple and pages fast."),
        ("Who hosts the website?", "We recommend managed WordPress hosting in your name, with backups and security included. We can set it up for you or work with your current host."),
        ("Can you move my existing site to WordPress?", "Yes. We migrate your content, keep URLs where possible and set up 301 redirects for anything that changes, so you keep your search rankings."),
    ],
    related=["c:web", "website-redesign", "seo-content-writing"],
    areas=["melbourne", "auckland", "brisbane", "adelaide"],
),
dict(
    slug="shopify-ecommerce-websites", name="Shopify & Ecommerce Websites", parent="web", icon="spark",
    h1="Shopify & Ecommerce Website Design in Australia & New Zealand",
    title="BEST Shopify & Ecommerce Website Design Agency Australia & New Zealand – looking for a Shopify Store, Ecommerce Web Design or Online Shop SEO near me? Hiroki Digital",
    description="Shopify and ecommerce website design for Australian and NZ brands. Fast stores, clear product pages and SEO-ready collections that turn browsers into buyers.",
    tagline="Online stores that are quick to browse, easy to buy from and simple to run.",
    timeline="4–8 weeks depending on catalogue size",
    intro=[
        "Hiroki Digital designs and builds Shopify stores and ecommerce websites for retailers and product brands across Australia and New Zealand. We focus on the parts that change revenue: fast pages, clear product information, simple checkout and product pages that can rank on Google.",
        "Whether you're launching your first store or moving from an older platform, we set up the catalogue, payments, shipping and tracking so you can see exactly where sales come from from your first order.",
    ],
    sections=[
        dict(h2="Why we usually recommend Shopify", paras=[
            "Shopify handles hosting, security, payments and checkout, so your team can focus on products and customers. It supports Australian and New Zealand payment methods, buy-now-pay-later options, GST settings and local shipping carriers through its app ecosystem. For most small and mid-sized retailers it's the fastest way to a reliable store.",
            "If your business has unusual requirements, such as complex B2B pricing or bookings mixed with products, we'll talk through WooCommerce or a custom setup before you commit.",
        ]),
        dict(h2="Ecommerce SEO built into the store", paras=[
            "Product and collection pages are your best chance to rank for buying searches. We write unique collection descriptions, set clean URLs, add Product and Breadcrumb schema, and make sure filters don't create thousands of duplicate pages for Google to crawl.",
        ], bullets=[
            ("Collection pages", "Category pages that target searches like 'linen dresses NZ' or 'work boots Brisbane'."),
            ("Product schema", "Price, availability and reviews marked up so search results can show rich details."),
            ("Image optimisation", "Compressed images with descriptive file names and alt text."),
            ("Internal links", "Related products and collections linked so customers and Google can find more."),
        ]),
        dict(h2="What's included in an ecommerce website", paras=[], bullets=[
            ("Store design", "Homepage, collection, product, cart and content pages designed for your brand."),
            ("Catalogue setup", "Products, variants, collections and inventory imported and organised."),
            ("Payments and shipping", "Payment gateways, GST, shipping zones and rates configured."),
            ("Tracking", "GA4 ecommerce events, Meta pixel and Google Ads conversion tags."),
            ("Email capture", "Pop-up or footer sign-up connected to your email platform for abandoned-cart and welcome flows."),
        ]),
    ],
    steps=[
        ("Plan the store", "Products, collections, payments, shipping and the apps you'll need.", "week 1"),
        ("Design", "Homepage, collection and product page designs for your review.", "weeks 1–3"),
        ("Build and import", "Theme build, catalogue import, payments and tracking set up.", "weeks 3–6"),
        ("Test and launch", "Test orders, speed checks, redirects from any old store, then go live.", "weeks 6–8"),
    ],
    local="Your store can sell nationwide whether you're based on [[a:gold-coast|the Gold Coast]] or in [[a:wellington|Wellington]]. Once your store is live, [[s:email-marketing-automation|email automation]] and [[s:facebook-instagram-ads|social ads]] are usually the quickest ways to grow repeat sales.",
    faqs=[
        ("How much does a Shopify store cost to build?", "It depends on the number of products, custom features and integrations. You'll get a fixed quote after the discovery call, and Shopify's own monthly plan is billed directly to you."),
        ("Can you move my store from WooCommerce or another platform?", "Yes. We migrate products, customers and order history where the platforms allow, and redirect old product URLs so you keep your search rankings."),
        ("Do you set up GST and shipping?", "Yes. We configure tax settings and shipping zones for Australia, New Zealand or international orders, and connect carrier apps if you need live rates."),
        ("Will my store rank on Google?", "Your store will be built with ecommerce SEO foundations. Ranking for competitive product searches usually also needs ongoing content and link building, which we can add as an SEO plan."),
        ("Can I manage products myself after launch?", "Yes. Shopify's admin is easy to learn, and we include a walkthrough on adding products, running discounts and managing orders."),
    ],
    related=["c:web", "conversion-rate-optimisation", "email-marketing-automation"],
    areas=["gold-coast", "wellington", "sydney", "auckland"],
),
dict(
    slug="landing-page-design", name="Landing Page Design", parent="web", icon="cursor",
    h1="Landing Page Design in Australia & New Zealand",
    title="BEST Landing Page Design Agency Australia & New Zealand – looking for High-Converting Landing Pages, Google Ads Landing Pages or Lead Generation Pages near me? Hiroki Digital",
    description="High-converting landing pages for Google Ads, Meta ads and lead magnets. Fast, focused pages designed and tested for Australian and NZ businesses.",
    tagline="One page, one offer, one action. Built to turn ad clicks into enquiries.",
    timeline="1–2 weeks per page",
    intro=[
        "When you pay for every click, the page people land on decides whether that money turns into enquiries. Hiroki Digital designs landing pages for Google Ads, Meta ads and lead magnets that match the ad, make one clear offer and remove everything that distracts from it.",
        "Each page is fast on mobile, tracked properly and built so we can test headlines, offers and forms. The goal is a lower cost per lead, measured in your ad account and your lead sheet.",
    ],
    sections=[
        dict(h2="What makes a landing page convert", paras=[
            "A landing page has one job. It should feel like the next step after the ad, explain the offer in seconds and make the form or phone number impossible to miss. Most underperforming pages fail on one of these basics.",
        ], bullets=[
            ("Message match", "The headline repeats the promise from the ad, so visitors know they're in the right place."),
            ("A clear offer", "A free audit, quote, consultation or guide that's worth the visitor's details."),
            ("A short form", "Only the fields you need, placed where people can see it without scrolling far."),
            ("Proof and detail", "What's included, how it works, FAQs and your real business details."),
            ("Speed", "Pages that load in under two and a half seconds on a mid-range phone."),
        ]),
        dict(h2="Landing pages and lead magnets", paras=[
            "Lead magnets work best when each one has its own page. A free homepage concept, a 90-day growth plan or a downloadable checklist each attracts a different visitor, so each gets its own headline, form and follow-up. We connect every page to your lead sheet with the ad source attached, so you can see which offer and which ad brought in each lead.",
            "We also set up the thank-you page as a conversion event in Google Ads and GA4. That gives the ad platforms clean data to optimise against, which usually lowers cost per lead over the following weeks.",
        ]),
        dict(h2="What's included", paras=[], bullets=[
            ("Page design and copy", "Headline options, offer, sections and form, written for your audience."),
            ("Form connected to your systems", "Leads sent to a Google Sheet or CRM with UTM and click ID data."),
            ("Conversion tracking", "Google Ads, GA4 and Meta conversion events on the thank-you page."),
            ("A/B test plan", "The first two or three tests to run, ranked by likely impact."),
        ]),
    ],
    steps=[
        ("Ad and offer review", "We look at your ads, audience and offer before writing a word.", "day 1–2"),
        ("Copy and design", "Headline, sections and form designed for mobile first.", "days 3–7"),
        ("Build and tracking", "Page built, form connected and conversions tested end to end.", "week 2"),
        ("Launch and test", "Page goes live with your ads, then we test and improve.", "ongoing"),
    ],
    local="Landing pages for local ads perform better when they mention the area. A page for a [[a:brisbane|Brisbane]] campaign should name Brisbane suburbs, and an ad for [[a:canberra|Canberra]] should say Canberra. We pair page design with [[s:google-ads-management|Google Ads management]] so the targeting and the page match.",
    faqs=[
        ("Why not send ad traffic to my homepage?", "Your homepage talks to everyone. A landing page talks to the person who clicked one specific ad, with one offer and one action, which usually converts at a much higher rate."),
        ("How many landing pages do I need?", "One per offer or service you advertise. If you run ads for three services, three focused pages will usually outperform one general page."),
        ("Can you build landing pages on my existing website?", "Yes. We can build them on your current platform, or as standalone pages on a subdomain if your site is slow or hard to edit."),
        ("Do you write the copy?", "Yes. We write the headline, offer and page copy, and you approve everything before it goes live."),
        ("How do you measure success?", "Conversion rate and cost per lead from your ad platform, checked against the leads that actually arrive in your sheet or CRM."),
    ],
    related=["c:web", "conversion-rate-optimisation", "google-ads-management"],
    areas=["brisbane", "canberra", "perth", "hamilton"],
),
dict(
    slug="website-speed-optimisation", name="Website Speed Optimisation", parent="web", icon="gauge",
    h1="Website Speed Optimisation in Australia & New Zealand",
    title="BEST Website Speed Optimisation Agency Australia & New Zealand – looking for Core Web Vitals Fixes, Page Speed Optimisation or a Faster WordPress Site near me? Hiroki Digital",
    description="Website speed optimisation and Core Web Vitals fixes for Australian and NZ businesses. Faster pages on mobile, better rankings and more enquiries.",
    tagline="Faster pages on mobile, passing all three Core Web Vitals.",
    timeline="1–3 weeks",
    intro=[
        "Slow websites lose visitors before they've read a word, and Google uses page experience signals as part of how it ranks pages. Hiroki Digital finds what's slowing your site down and fixes it, with a focus on the mobile experience where most of your customers arrive.",
        "We measure before and after with the same tools Google uses, so you can see exactly what changed.",
    ],
    sections=[
        dict(h2="The three Core Web Vitals we fix", paras=[
            "Core Web Vitals are Google's measures of real-world page experience. We aim for the 'good' threshold on all three, measured on mobile.",
        ], bullets=[
            ("Largest Contentful Paint (LCP)", "How quickly the main content appears. Good is 2.5 seconds or less."),
            ("Interaction to Next Paint (INP)", "How quickly the page responds when someone taps or clicks. Good is 200 milliseconds or less."),
            ("Cumulative Layout Shift (CLS)", "How much the page jumps around while loading. Good is 0.1 or less."),
        ]),
        dict(h2="Common causes of a slow website", paras=[
            "Most slow small-business sites have the same handful of problems. Oversized images, heavy page builders, too many plugins, third-party chat and tracking scripts, and cheap shared hosting are the usual causes.",
            "We fix the causes in order of impact: compress and resize images, serve modern formats, defer scripts that aren't needed straight away, remove unused plugins and CSS, preload key fonts, add caching and a CDN, and move to better hosting when it's the bottleneck.",
        ]),
        dict(h2="What's included", paras=[], bullets=[
            ("Speed audit", "Lighthouse, PageSpeed Insights and Search Console field data for your key pages."),
            ("Fix list", "Every issue ranked by impact, with the effort each one takes."),
            ("Implementation", "We make the fixes on your site and test that nothing breaks."),
            ("Before and after report", "Scores and load times for each key page, measured the same way."),
        ]),
    ],
    steps=[
        ("Measure", "Lab and field data for your homepage and top service pages.", "days 1–2"),
        ("Diagnose", "A ranked list of what's slowing each page down.", "days 2–4"),
        ("Fix", "Image, script, font, caching and hosting fixes, tested on staging.", "week 1–2"),
        ("Verify", "Re-test, then track field data in Search Console over the next month.", "weeks 2–6"),
    ],
    local="Speed matters most for people searching on the go, like someone looking for an emergency plumber in [[a:adelaide|Adelaide]] or a cafe in [[a:hobart|Hobart]] on their phone. Faster pages support every other part of [[s:technical-seo-audit|technical SEO]].",
    faqs=[
        ("Does website speed affect Google rankings?", "Page experience, including Core Web Vitals, is one of the signals Google uses. It rarely outweighs relevance, but between similar pages a faster one has an edge, and it converts more visitors either way."),
        ("Why is my site slow on mobile but fine on my computer?", "Phones have slower processors and often slower connections. Large images and heavy scripts that a desktop handles easily can take several seconds on a mid-range phone."),
        ("Can you speed up a WordPress site without rebuilding it?", "Usually, yes. Image optimisation, caching, plugin clean-up and better hosting often make a big difference. If the theme or page builder is the root cause, we'll explain the options."),
        ("Will speed fixes break anything?", "We test every change on a staging copy of your site first and check forms, tracking and key pages before anything goes live."),
        ("How do you measure the results?", "We use Lighthouse and PageSpeed Insights for lab results and Search Console's Core Web Vitals report for real visitor data over the following weeks."),
    ],
    related=["c:web", "technical-seo-audit", "wordpress-website-design"],
    areas=["adelaide", "hobart", "sydney", "wellington"],
),
]
