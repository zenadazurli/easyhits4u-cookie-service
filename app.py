import asyncio
import os
from browser_use import Browser, BrowserSession

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_kGrN4LoTG5wF85mSno8d_xFCbMOO2jM7bRWtu2RP_Ks")

async def get_cookies():
    os.environ["BROWSER_USE_API_KEY"] = API_KEY
    
    browser = Browser(use_cloud=True, headless=True)
    
    try:
        # Avvia il browser e ottieni la sessione
        await browser.start()
        
        # Ottieni la pagina tramite la sessione
        session = await browser.get_browser_session()
        page = await session.must_get_current_page()
        
        # Login
        await page.goto("https://www.easyhits4u.com/logon/")
        await page.wait_for_timeout(3000)
        await page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
        await page.fill('input[name="password"]', "DDnmVV45!!")
        await page.click('button.btn_green')
        await page.wait_for_timeout(15000)
        
        # Prendi cookie
        context = page.context
        all_cookies = await context.cookies()
        
        for cookie in all_cookies:
            if cookie['name'] in ['sesids', 'user_id']:
                print(f"{cookie['name']} = {cookie['value']}")
        
        return all_cookies
        
    finally:
        await browser.stop()

if __name__ == "__main__":
    asyncio.run(get_cookies())
