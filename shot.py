import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp('http://localhost:29229')
        for name,vp,mob in [('desktop',{'width':1440,'height':900},False),('mobile',{'width':390,'height':844},True)]:
            ctx=await b.new_context(viewport=vp,is_mobile=mob,device_scale_factor=1)
            pg=await ctx.new_page(); errs=[]
            pg.on('console',lambda m: m.type=='error' and errs.append(m.text)); pg.on('pageerror',lambda e: errs.append(str(e)))
            await pg.goto('http://localhost:8090/',wait_until='networkidle')
            await pg.screenshot(path=f'shots/{name}-top.png')
            h=await pg.evaluate('document.body.scrollHeight')
            for y in range(0,h,600):
                await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(120)
            await pg.wait_for_timeout(900)
            await pg.screenshot(path=f'shots/{name}-full.png',full_page=True)
            print(name,'height',h,'errors',errs)
            await ctx.close()
asyncio.run(main())
