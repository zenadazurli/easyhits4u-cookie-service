import asyncio
import json
import os
from browser_use import Browser

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_kGrN4LoTG5wF85mSno8d_xFCbMOO2jM7bRWtu2RP_Ks")

async def get_session_cookies():
    print("🚀 EasyHits4U Cookie Service")
    
    browser = Browser(use_cloud=True, api_key=API_KEY, headless=True)
    
    try:
        page = await browser.get_page()
        
        print("🌐 Opening login page...")
        await page.goto("https://www.easyhits4u.com/logon/")
        await page.wait_for_timeout(3000)
        
        print("📝 Filling form...")
        await page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
        await page.fill('input[name="password"]', "DDnmVV45!!")
        
        print("🔑 Submitting login...")
        await page.click('button.btn_green')
        
        print("⏳ Waiting for redirect...")
        await page.wait_for_timeout(15000)
        
        print("\n🍪 Extracting cookies...")
        context = page.context
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
        
        with open("/tmp/cookies.json", "w") as f:
            json.dump(all_cookies, f, indent=2)
        
        return sesids, user_id
        
    finally:
        await browser.close()

async def main():
    print("=" * 50)
    sesids, user_id = await get_session_cookies()
    print("=" * 50)
    if sesids and user_id:
        print(f"🎉 SUCCESS!")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ FAILED")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())