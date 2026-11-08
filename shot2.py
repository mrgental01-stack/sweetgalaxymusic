import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp('http://localhost:29229')
        for name,vp,mob in [('desktop',{'width':1440,'height':900},False),('mobile',{'width':390,'height':844},True)]:
            ctx=await b.new_context(viewport=vp,is_mobile=mob); pg=await ctx.new_page()
            await pg.goto('http://localhost:8090/',wait_until='networkidle')
            for sec in ['social']:
                await pg.evaluate(f"document.getElementById('{sec}').scrollIntoView()"); await pg.wait_for_timeout(1000)
                await pg.screenshot(path=f'shots/{name}-{sec}.png')
            await ctx.close()
asyncio.run(main())
