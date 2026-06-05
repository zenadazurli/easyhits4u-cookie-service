import asyncio
import subprocess
import time
import re
import os
from playwright.async_api import async_playwright

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Jbd6H_zrIUrqic91x0B1z9ZiVilvxm5ixMJWirBiWz4")

async def get_cookies_from_cli_session():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("CLI + Playwright Context")
    print("=" * 50)
    
    # 1. Configura CLI
    subprocess.run(f"browser-use config set api_key {API_KEY}", shell=True)
    subprocess.run("browser-use close --all", shell=True)
    time.sleep(2)
    
    # 2. Connetti al cloud e ottieni il CDP URL
    print("🔌 Connecting to cloud...")
    result = subprocess.run("browser-use cloud connect", shell=True, capture_output=True, text=True)
    print(result.stdout)
    time.sleep(5)
    
    # Estrai CDP URL dall'output
    cdp_match = re.search(r'cdp_url:\s*(wss://[^\s]+)', result.stdout)
    if not cdp_match:
        print("❌ CDP URL not found")
        return None, None
    
    cdp_url = cdp_match.group(1)
    print(f"🔗 CDP URL: {cdp_url}")
    
    # 3. Connetti Playwright alla stessa sessione
    print("🔗 Connecting Playwright...")
    async with async_playwright() as p:
        pw_browser = await p.chromium.connect_over_cdp(cdp_url)
        
        if pw_browser.contexts and pw_browser.contexts[0].pages:
            page = pw_browser.contexts[0].pages[0]
        else:
            context = await pw_browser.new_context()
            page = await context.new_page()
        
        # 4. Login tramite CLI (già fatto, ma verifichiamo)
        print("🌐 Checking page...")
        await page.wait_for_timeout(5000)
        
        # Se non siamo sulla pagina giusta, naviga
        if "logon" in page.url:
            print("📝 Filling form via CLI...")
            subprocess.run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"', shell=True)
            time.sleep(1)
            subprocess.run('browser-use keys "Tab"', shell=True)
            time.sleep(1)
            subprocess.run('browser-use type "DDnmVV45!!"', shell=True)
            time.sleep(1)
            subprocess.run('browser-use keys "Enter"', shell=True)
            time.sleep(20)
        
        # 5. Prendi i cookie dal context Playwright
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
        
        print(f"📍 URL: {page.url}")
        await pw_browser.close()
    
    # 6. Cleanup
    subprocess.run("browser-use close --all", shell=True)
    
    return sesids, user_id

if __name__ == "__main__":
    sesids, user_id = asyncio.run(get_cookies_from_cli_session())
    print("\n" + "=" * 50)
    if sesids and user_id:
        print(f"🎉 SUCCESSO!")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ Cookie non trovati")
    print("=" * 50)
