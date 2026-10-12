#!/usr/bin/env python3
"""Renders OG images, favicons and logo PNGs into src/static (run build.py first, then build.py again)."""
import asyncio, pathlib, io
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright
from PIL import Image
import build

ROOT = build.ROOT
STATIC = ROOT / "static"
OGSRC = ROOT.parent / "dist" / "og-src"

OGS = [
    dict(name="og-home", kind="home", size=66, h1='Be the business people <span class="hl">find first</span>.', pill="Free growth plan", url="hirokidigital.com"),
    dict(name="og-web-design", kind="web", size=66, h1='Websites that look sharp and <span class="hl">bring in enquiries</span>.', pill="Free homepage concept", url="hirokidigital.com"),
    dict(name="og-marketing", kind="marketing", size=66, h1='Marketing that brings in <span class="hl">customers</span>, not just clicks.', pill="Free 90-day growth plan", url="hirokidigital.com"),
    dict(name="og-seo", kind="seo", size=58, h1='Climb Google. Get found by customers <span class="hl">already searching</span>.', pill="Free SEO audit", url="hirokidigital.com"),
]

def mark_svg(rx=12, scale=1.0, bg="#2D3BD1"):
    # scale shrinks the glyph around the centre (for maskable / apple icons)
    g = f'<g transform="translate(24 24) scale({scale}) translate(-24 -24)"><rect x="11" y="18" width="7" height="20" rx="1.2" fill="#fff"/><rect x="30" y="16.5" width="7" height="21.5" rx="1.2" fill="#fff"/><rect x="30" y="9" width="7" height="5.5" rx="1.2" fill="#FFC93C"/><path d="M18 30 L30 23 L30 28.5 L18 35.5Z" fill="#fff"/></g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="{rx}" fill="{bg}"/>{g}</svg>'

async def main():
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)
    env.globals.update(icons=build.ICONS)
    OGSRC.mkdir(parents=True, exist_ok=True)
    (STATIC / "assets/og").mkdir(parents=True, exist_ok=True)
    (STATIC / "assets/img").mkdir(parents=True, exist_ok=True)
    mkt, seo = build.marketing_data(), build.seo_data()
    dials = [{"v": 95, "label": "Performance"}, {"v": 100, "label": "Accessibility"}, {"v": 100, "label": "Best practices"}, {"v": 100, "label": "SEO"}]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1200, "height": 630}, reduced_motion="reduce")
        pg = await ctx.new_page()
        for og in OGS:
            html = env.get_template("og.html").render(og=og, mkt=mkt, seo=seo, dials=dials)
            f = OGSRC / f"{og['name']}.html"
            f.write_text(html)
            await pg.goto(f.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            png = await pg.screenshot(type="png")
            Image.open(io.BytesIO(png)).convert("RGB").save(STATIC / f"assets/og/{og['name']}.png", optimize=True)
        # icons
        async def render(svg, size, out):
            ip = await ctx.new_page()
            await ip.set_viewport_size({"width": size, "height": size})
            await ip.set_content(f'<html><body style="margin:0;background:transparent">{svg.replace("<svg ", f"<svg width=\"{size}\" height=\"{size}\" ", 1)}</body></html>')
            data = await ip.screenshot(type="png", omit_background=True, clip={"x": 0, "y": 0, "width": size, "height": size})
            await ip.close()
            im = Image.open(io.BytesIO(data)).convert("RGBA")
            if out:
                im.save(out, optimize=True)
            return im
        rounded = mark_svg()
        await render(rounded, 192, STATIC / "assets/img/icon-192.png")
        await render(rounded, 512, STATIC / "assets/img/icon-512.png")
        await render(rounded, 512, STATIC / "assets/img/logo-512.png")
        await render(mark_svg(rx=0, scale=0.78), 512, STATIC / "assets/img/icon-maskable-512.png")
        await render(mark_svg(rx=0, scale=0.86), 180, STATIC / "apple-touch-icon.png")
        ico = [await render(rounded, s, None) for s in (48, 32, 16)]
        ico[0].save(STATIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[1:])
        await b.close()
    (STATIC / "favicon.svg").write_text(mark_svg() + "\n")
    print("assets rendered →", STATIC)

if __name__ == "__main__":
    asyncio.run(main())
