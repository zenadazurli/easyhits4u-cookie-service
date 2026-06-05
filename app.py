import asyncio
import os
from browser_use_sdk.v3 import AsyncBrowserUse
from playwright.async_api import async_playwright

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Jbd6H_zrIUrqic91x0B1z9ZiVilvxm5ixMJWirBiWz4")

async def wait_for_turnstile_complete(page, timeout=60):
    """Aspetta che Turnstile sia completato (quadratino verde/spuntato)"""
    print("⏳ Attesa completamento Turnstile...")
    
    for i in range(timeout):
        # Controlla se il token cf-turnstile-response è presente
        token = await page.evaluate('''
            () => {
                const input = document.querySelector('[name="cf-turnstile-response"]');
                return input ? input.value : null;
            }
        ''')
        
        if token and len(token) > 10:
            print(f"✅ Turnstile completato dopo {i+1} secondi!")
            return True
        
        # Controlla anche se il widget è scomparso
        widget = await page.locator('.cf-turnstile').count()
        if widget == 0:
            print(f"✅ Widget Turnstile scomparso dopo {i+1} secondi!")
            return True
        
        await asyncio.sleep(1)
    
    print("⚠️ Timeout Turnstile, procedo comunque...")
    return False

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("=" * 50)
    
    client = AsyncBrowserUse(api_key=API_KEY)
    
    try:
        # Crea browser cloud
        print("🔌 Creating cloud browser...")
        browser = await client.browsers.create()
        print(f"✅ Browser created: {browser.id}")
        
        # Connetti Playwright
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
            
            # === ATTESA CHE TURNSTILE SIA COMPLETATO ===
            await wait_for_turnstile_complete(page)
            
            # Attesa extra per sicurezza
            await page.wait_for_timeout(3000)
            
            # Compila form
            print("📝 Filling form...")
            await page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
            await page.fill('input[name="password"]', "DDnmVV45!!")
            
            # Premi Enter (non click sul bottone)
            print("🔑 Pressing Enter...")
            await page.keyboard.press('Enter')
            
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
            
            await pw_browser.close()
        
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
    finally:
        if 'browser' in locals():
            await client.browsers.stop(browser.id)

if __name__ == "__main__":
    asyncio.run(main())
