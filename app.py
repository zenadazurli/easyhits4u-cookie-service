import asyncio
from browser_use_sdk.v3 import AsyncBrowserUse
from playwright.async_api import async_playwright
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Fk49iTm7o4hfnTYAM_Qh_7ovxObscyZe1Y10s3VluxA")

async def wait_for_turnstile_complete(page, timeout=60):
    """Aspetta che Turnstile sia completamente risolto"""
    print("⏳ Waiting for Turnstile to complete...")
    
    for i in range(timeout):
        # Controlla se il token cf-turnstile-response è presente e non vuoto
        token = await page.evaluate('''
            () => {
                const input = document.querySelector('[name="cf-turnstile-response"]');
                return input ? input.value : null;
            }
        ''')
        
        if token and len(token) > 10:
            print(f"✅ Turnstile completed after {i+1} seconds!")
            return True
        
        # Controlla anche se il widget è scomparso
        widget = await page.locator('.cf-turnstile').count()
        if widget == 0:
            print(f"✅ Turnstile widget disappeared after {i+1} seconds!")
            return True
        
        await asyncio.sleep(1)
    
    print("⚠️ Turnstile timeout, proceeding anyway...")
    return False

async def close_modals(page):
    """Chiude modali React"""
    await page.evaluate('''
        () => {
            const overlays = document.querySelectorAll('.ReactModal__Overlay');
            overlays.forEach(overlay => overlay.style.display = 'none');
            const portals = document.querySelectorAll('.ReactModalPortal');
            portals.forEach(portal => portal.style.display = 'none');
        }
    ''')
    await page.wait_for_timeout(500)

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("Wait for Turnstile before Enter")
    print("=" * 50)
    
    client = AsyncBrowserUse(api_key=API_KEY)
    
    try:
        print("\n🔌 Creating cloud browser...")
        browser = await client.browsers.create()
        
        async with async_playwright() as p:
            pw_browser = await p.chromium.connect_over_cdp(browser.cdp_url)
            context = pw_browser.contexts[0]
            page = context.pages[0]
            
            print("\n🌐 Opening login page...")
            await page.goto("https://www.easyhits4u.com/logon/")
            
            # 1. ASPETTA CHE TURNSTILE SIA COMPLETATO
            await wait_for_turnstile_complete(page)
            
            # 2. Chiudi modali
            await close_modals(page)
            
            # 3. Compila form
            print("📝 Filling form...")
            await page.fill('#username', "sandrominori50+ulugarecexisa@gmail.com")
            await page.fill('#password', "DDnmVV45!!")
            
            # 4. Piccola attesa prima di Enter
            await page.wait_for_timeout(1000)
            
            # 5. Premi Enter (ora Turnstile è risolto)
            print("🔑 Pressing Enter...")
            await page.keyboard.press('Enter')
            
            # 6. Attesa redirect
            print("⏳ Waiting for redirect...")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(10000)
            
            # 7. Leggi cookie
            print("\n🍪 Extracting cookies...")
            all_cookies = await context.cookies()
            
            sesids = None
            user_id = None
            
            for cookie in all_cookies:
                if cookie['name'] == 'sesids':
                    sesids = cookie['value']
                    print(f"✅ sesids = {sesids}")
                if cookie['name'] == 'user_id':
                    user_id = cookie['value']
                    print(f"✅ user_id = {user_id}")
            
            print(f"📍 Final URL: {page.url}")
            await pw_browser.close()
        
        print("\n" + "=" * 50)
        if sesids and user_id:
            print("🎉 SUCCESSO!")
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
