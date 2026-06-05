import asyncio
import subprocess
import time
import re
import os
from playwright.async_api import async_playwright

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Fk49iTm7o4hfnTYAM_Qh_7ovxObscyZe1Y10s3VluxA")

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("CLI + Playwright Context")
    print("=" * 50)
    
    # 1. Configura CLI
    print("\n1. Configuring CLI...")
    subprocess.run(f"browser-use config set api_key {API_KEY}", shell=True)
    subprocess.run("browser-use close --all", shell=True)
    time.sleep(2)
    
    # 2. Connetti al cloud e cattura CDP URL
    print("\n2. Connecting to cloud...")
    result = subprocess.run("browser-use cloud connect", shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    # Estrai CDP URL
    cdp_match = re.search(r'cdp_url:\s*(wss://[^\s]+)', result.stdout)
    if not cdp_match:
        print("❌ CDP URL not found")
        return
    
    cdp_url = cdp_match.group(1)
    print(f"✅ CDP URL: {cdp_url}")
    
    # 3. Connetti Playwright
    print("\n3. Connecting Playwright...")
    async with async_playwright() as p:
        pw_browser = await p.chromium.connect_over_cdp(cdp_url)
        
        if pw_browser.contexts and pw_browser.contexts[0].pages:
            page = pw_browser.contexts[0].pages[0]
        else:
            context = await pw_browser.new_context()
            page = await context.new_page()
        
        # 4. Login usando CLI
        print("\n4. Logging in...")
        
        # Compila form via CLI
        subprocess.run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"', shell=True)
        time.sleep(1)
        subprocess.run('browser-use keys "Tab"', shell=True)
        time.sleep(1)
        subprocess.run('browser-use type "DDnmVV45!!"', shell=True)
        time.sleep(1)
        subprocess.run('browser-use keys "Enter"', shell=True)
        
        print("⏳ Waiting for login...")
        time.sleep(20)
        
        # 5. Prendi cookie dal context Playwright
        print("\n5. Extracting cookies...")
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
