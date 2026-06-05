import asyncio
from browser_use_sdk.v3 import AsyncBrowserUse
from playwright.async_api import async_playwright
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Fk49iTm7o4hfnTYAM_Qh_7ovxObscyZe1Y10s3VluxA")

async def wait_for_turnstile_token(page, timeout=60):
    """Aspetta che Turnstile generi il token cf-turnstile-response"""
    print("⏳ Waiting for Turnstile token...")
    
    for i in range(timeout):
        # Legge il token dall'input hidden
        token = await page.evaluate('''
            () => {
                const input = document.querySelector('input[name="cf-turnstile-response"]');
                return input ? input.value : null;
            }
        ''')
        
        if token and len(token) > 10:
            print(f"✅ Turnstile token obtained after {i+1} seconds!")
            print(f"   Token preview: {token[:50]}...")
            return token
        
        # Mostra progresso ogni 10 secondi
        if i > 0 and i % 10 == 0:
            print(f"   Still waiting... {i}s")
        
        await asyncio.sleep(1)
    
    print("⚠️ Turnstile token not obtained within timeout")
    return None

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("Wait for Turnstile Token, then Enter")
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
            
            # Compila il form PRIMA di Turnstile?
            print("📝 Filling form...")
            await page.fill('#username', "sandrominori50+ulugarecexisa@gmail.com")
            await page.fill('#password', "DDnmVV45!!")
            
            # ASPETTA IL TOKEN TURNSTILE
            token = await wait_for_turnstile_token(page)
            
            if token:
                # Opzionale: possiamo anche usare il token per verificare
                print(f"🔐 Turnstile resolved with token: {token[:30]}...")
            
            # PICCOLA ATTESA EXTRA PER SICUREZZA
            await page.wait_for_timeout(2000)
            
            # Ora premi Enter (Turnstile è risolto)
            print("🔑 Pressing Enter...")
            
            # Prova diversi metodi
            try:
                # Metodo 1: Enter
                await page.keyboard.press('Enter')
                print("   Used Enter key")
            except Exception as e:
                print(f"   Enter failed: {e}")
                try:
                    # Metodo 2: Click sul bottone
                    await page.click('button.btn_green', force=True)
                    print("   Used forced click")
                except:
                    # Metodo 3: JavaScript
                    await page.evaluate('document.querySelector("button.btn_green").click()')
                    print("   Used JavaScript click")
            
            print("⏳ Waiting for redirect...")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(10000)
            
            # Leggi cookie
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
