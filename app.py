import asyncio
import os
from browser_use_sdk.v3 import AsyncBrowserUse
from playwright.async_api import async_playwright

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_kGrN4LoTG5wF85mSno8d_xFCbMOO2jM7bRWtu2RP_Ks")

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("Browser Use Cloud SDK v3 + Playwright")
    print("=" * 50)
    
    # Crea client con API key
    client = AsyncBrowserUse(api_key=API_KEY)
    
    # Crea browser cloud
    print("🔌 Creating cloud browser...")
    browser = await client.browsers.create()
    print(f"✅ Browser created: {browser.id}")
    print(f"🔗 CDP URL: {browser.cdp_url}")
    
    # Connetti Playwright al browser cloud
    print("🔗 Connecting Playwright...")
    async with async_playwright() as p:
        pw_browser = await p.chromium.connect_over_cdp(browser.cdp_url)
        
        # Ottieni la pagina
        if pw_browser.contexts and pw_browser.contexts[0].pages:
            page = pw_browser.contexts[0].pages[0]
        else:
            context = await pw_browser.new_context()
            page = await context.new_page()
        
        # Login
        print("🌐 Login to EasyHits4U...")
        await page.goto("https://www.easyhits4u.com/logon/")
        await page.wait_for_timeout(3000)
        
        await page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
        await page.fill('input[name="password"]', "DDnmVV45!!")
        await page.click('button.btn_green')
        
        print("⏳ Waiting for redirect...")
        await page.wait_for_timeout(15000)
        
        # Prendi i cookie (HTTP-only inclusi!)
        print("\n🍪 Extracting cookies...")
        all_cookies = await page.context.cookies()
        
        sesids = None
        user_id = None
        
        for cookie in all_cookies:
            if cookie['name'] == 'sesids':
                sesids = cookie['value']
                print(f"✅ sesids = {sesids}")
            if cookie['name'] == 'user_id':
                user_id = cookie['value']
                print(f"✅ user_id = {user_id}")
        
        await pw_browser.close()
    
    # Ferma il browser cloud
    await client.browsers.stop(browser.id)
    
    print("\n" + "=" * 50)
    if sesids and user_id:
        print(f"🎉 SUCCESSO!")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ Cookie non trovati")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
