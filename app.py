import asyncio
import os
import json
from playwright.async_api import async_playwright, Browser as PlaywrightBrowser, Page
from browser_use import BrowserSession, Agent, Tools, ActionResult

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_kGrN4LoTG5wF85mSno8d_xFCbMOO2jM7bRWtu2RP_Ks")

# Variabili globali per Playwright
playwright_browser: PlaywrightBrowser | None = None
playwright_page: Page | None = None
playwright_instance = None

async def connect_playwright_to_cdp(cdp_url: str):
    """Connetti Playwright alla stessa istanza Chrome di Browser Use"""
    global playwright_browser, playwright_page, playwright_instance
    
    playwright_instance = await async_playwright().start()
    playwright_browser = await playwright_instance.chromium.connect_over_cdp(cdp_url)
    
    if playwright_browser and playwright_browser.contexts and playwright_browser.contexts[0].pages:
        playwright_page = playwright_browser.contexts[0].pages[0]
    elif playwright_browser:
        context = await playwright_browser.new_context()
        playwright_page = await context.new_page()

# Crea i tools personalizzati
tools = Tools()

@tools.registry.action(
    "Get session cookies including HTTP-only cookies like sesids and user_id"
)
async def get_session_cookies(browser_session: BrowserSession) -> ActionResult:
    """Prende i cookie dalla sessione Playwright (inclusi HTTP-only)"""
    global playwright_page
    
    if not playwright_page:
        return ActionResult(error="Playwright not connected")
    
    try:
        all_cookies = await playwright_page.context.cookies()
        
        sesids = None
        user_id = None
        
        for cookie in all_cookies:
            if cookie['name'] == 'sesids':
                sesids = cookie['value']
            if cookie['name'] == 'user_id':
                user_id = cookie['value']
        
        if sesids and user_id:
            return ActionResult(
                extracted_content=f"sesids={sesids}, user_id={user_id}",
                long_term_memory=f"Cookie ottenuti: sesids={sesids}, user_id={user_id}"
            )
        else:
            return ActionResult(error=f"Cookie non trovati. Cookie disponibili: {[c['name'] for c in all_cookies]}")
            
    except Exception as e:
        return ActionResult(error=f"Errore: {e}")

@tools.registry.action(
    "Login to EasyHits4U using Playwright form filling"
)
async def playwright_login(browser_session: BrowserSession) -> ActionResult:
    """Login a EasyHits4U usando Playwright"""
    global playwright_page
    
    if not playwright_page:
        return ActionResult(error="Playwright not connected")
    
    try:
        await playwright_page.goto("https://www.easyhits4u.com/logon/")
        await playwright_page.wait_for_timeout(3000)
        
        await playwright_page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
        await playwright_page.fill('input[name="password"]', "DDnmVV45!!")
        await playwright_page.click('button.btn_green')
        
        await playwright_page.wait_for_timeout(15000)
        
        return ActionResult(
            extracted_content="Login completato",
            long_term_memory="Login eseguito con successo"
        )
        
    except Exception as e:
        return ActionResult(error=f"Login fallito: {e}")

async def main():
    print("=" * 50)
    print("EasyHits4U Cookie Service")
    print("Browser Use + Playwright Integration")
    print("=" * 50)
    
    os.environ["BROWSER_USE_API_KEY"] = API_KEY
    
    # Avvia Browser Use con CDP
    browser_session = BrowserSession(use_cloud=True)
    
    try:
        # Ottieni il CDP URL dalla sessione
        await browser_session.start()
        cdp_url = await browser_session.get_cdp_url()
        
        print(f"🔌 CDP URL: {cdp_url}")
        
        # Connetti Playwright alla stessa istanza
        await connect_playwright_to_cdp(cdp_url)
        
        # Crea l'agente con i tools
        agent = Agent(
            task="""
            1. Use playwright_login tool to login to EasyHits4U
            2. Wait for the page to load
            3. Use get_session_cookies tool to extract cookies
            """,
            browser_session=browser_session,
            tools=tools,
        )
        
        result = await agent.run()
        print(f"\n📊 Risultato: {result}")
        
    except Exception as e:
        print(f"❌ Errore: {e}")
    finally:
        if playwright_browser:
            await playwright_browser.close()
        if playwright_instance:
            await playwright_instance.stop()
        await browser_session.stop()

if __name__ == "__main__":
    asyncio.run(main())
