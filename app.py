import asyncio
import os
from browser_use_sdk.v3 import AsyncBrowserUse
from playwright.async_api import async_playwright

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Jbd6H_zrIUrqic91x0B1z9ZiVilvxm5ixMJWirBiWz4")

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("=" * 50)
    
    client = AsyncBrowserUse(api_key=API_KEY)
    
    try:
        print("🔌 Creating cloud browser...")
        browser = await client.browsers.create()
        
        async with async_playwright() as p:
            pw_browser = await p.chromium.connect_over_cdp(browser.cdp_url)
            
            if pw_browser.contexts and pw_browser.contexts[0].pages:
                page = pw_browser.contexts[0].pages[0]
            else:
                context = await pw_browser.new_context()
                page = await context.new_page()
            
            # Vai al login
            print("🌐 Opening login page...")
            await page.goto("https://www.easyhits4u.com/logon/")
            await page.wait_for_timeout(5000)
            
            # === USA SELECTORI PIÙ PRECISI ===
            print("📝 Filling form...")
            
            # Usa ID invece di name (più preciso)
            await page.fill('#username', "sandrominori50+ulugarecexisa@gmail.com")
            await page.fill('#password', "DDnmVV45!!")
            
            # Aspetta che il bottone sia realmente cliccabile
            print("🔑 Waiting for button...")
            await page.wait_for_selector('button.btn_green:not([disabled])', timeout=10000)
            
            # Click con JavaScript (bypassa overlay)
            print("🔑 Clicking login...")
            await page.evaluate('document.querySelector("button.btn_green").click()')
            
            # Attesa redirect
            print("⏳ Waiting for redirect...")
            await page.wait_for_timeout(20000)
            
            # Prendi cookie
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
            
            current_url = page.url
            print(f"📍 URL: {current_url}")
            
            await pw_browser.close()
        
        await client.browsers.stop(browser.id)
        
        print("\n" + "=" * 50)
        if sesids and user_id:
            print(f"🎉 SUCCESSO!")
            print(f"   sesids = {sesids}")
            print(f"   user_id = {user_id}")
        else:
            print("❌ Cookie non trovati")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    asyncio.run(main())
