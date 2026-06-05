import asyncio
from browser_use_sdk.v3 import AsyncBrowserUse
from playwright.async_api import async_playwright
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Fk49iTm7o4hfnTYAM_Qh_7ovxObscyZe1Y10s3VluxA")

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("Browser Use SDK v3 + Playwright")
    print("=" * 50)
    
    # Crea client con API key
    client = AsyncBrowserUse(api_key=API_KEY)
    
    try:
        # Crea browser cloud
        print("\n🔌 Creating cloud browser...")
        browser = await client.browsers.create()
        print(f"✅ Browser ID: {browser.id}")
        print(f"🔗 CDP URL: {browser.cdp_url}")
        
        # Connetti Playwright al browser cloud
        print("\n🔗 Connecting Playwright...")
        async with async_playwright() as p:
            pw_browser = await p.chromium.connect_over_cdp(browser.cdp_url)
            
            # Ottieni context e page
            context = pw_browser.contexts[0]
            page = context.pages[0]
            
            # Login su EasyHits4U
            print("\n🌐 Logging in to EasyHits4U...")
            await page.goto("https://www.easyhits4u.com/logon/")
            await page.wait_for_timeout(3000)
            
            print("📝 Filling form...")
            await page.fill('#username', "sandrominori50+ulugarecexisa@gmail.com")
            await page.fill('#password', "DDnmVV45!!")
            
            print("🔑 Submitting...")
            await page.click('button.btn_green')
            
            print("⏳ Waiting for redirect...")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000)
            
            # Leggi TUTTI i cookie (inclusi HTTP-only!)
            print("\n🍪 Extracting ALL cookies...")
            all_cookies = await context.cookies()
            
            print(f"\n📊 Total cookies found: {len(all_cookies)}")
            
            sesids = None
            user_id = None
            
            for cookie in all_cookies:
                print(f"   {cookie['name']} = {cookie['value'][:30]}...")
                if cookie['name'] == 'sesids':
                    sesids = cookie['value']
                if cookie['name'] == 'user_id':
                    user_id = cookie['value']
            
            print(f"\n📍 Final URL: {page.url}")
            
            await pw_browser.close()
        
        print("\n" + "=" * 50)
        if sesids and user_id:
            print("🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {sesids}")
            print(f"   user_id = {user_id}")
        else:
            print("❌ Cookie non trovati")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'browser' in locals():
            await client.browsers.stop(browser.id)

if __name__ == "__main__":
    asyncio.run(main())
