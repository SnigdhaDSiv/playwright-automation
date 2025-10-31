import os
import pytest
from playwright.sync_api import sync_playwright
#from playwright.async_api import async_playwright
from src.utils.Logger import get_logger
from datetime import datetime
from dotenv import load_dotenv
from src.EnvDataStore import EnvDataStore
from pathlib import Path

SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

@pytest.fixture(scope="session", autouse=True)
def logger():
    return get_logger(__name__)

# Environment Fixture
@pytest.fixture(scope="session")
def urls():
    env = os.getenv("ENV_NAME", "qa").lower()  # default to QA
    dotenv_path = f".env.{env}"
    load_dotenv(dotenv_path)
    
    out= {
        "WEB_BASE_URL": os.getenv("WEB_BASE_URL"),
        "API_GATEWAY_URL": os.getenv("API_GATEWAY_URL"),
        "USER_SERVICE_URL": os.getenv("USER_SERVICE_URL"),
        "TRANSACTION_SERVICE_URL": os.getenv("TRANSACTION_SERVICE_URL"),
        "HEADLESS": os.getenv("HEADLESS")
    }
    return out

@pytest.fixture(scope="session")  
def datastore():
    env = os.getenv("ENV_NAME", "qa").lower()
    return EnvDataStore(env)

def make_clickable_link(path: str) -> str:
    abs_path = os.path.abspath(path)
    return f"\033]8;;file://{abs_path}\033\\{abs_path}\033]8;;\033\\"

'''@pytest.fixture
async def page(urls, logger, request):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        #await page.goto(urls["WEB_BASE_URL"])

        yield page

        # Check if test failed
        rep_call = getattr(request.node, "rep_call", None)
        if rep_call and rep_call.failed:
            screenshot_dir = SCREENSHOT_DIR
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            file_name = f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = screenshot_dir / file_name
            await page.screenshot(path=str(path))
            logger.error(f"[SCREENSHOT CAPTURED] {make_clickable_link(str(path))}")

        await context.close()
        await browser.close()'''
@pytest.fixture
def page(urls, logger, request):
    with sync_playwright() as p:
        browser =  p.chromium.launch(headless=bool(urls["HEADLESS"]))
        context =  browser.new_context()
        page =  context.new_page()
        #await page.goto(urls["WEB_BASE_URL"])

        yield page

        # Check if test failed
        rep_call = getattr(request.node, "rep_call", None)
        if rep_call and rep_call.failed:
            screenshot_dir = SCREENSHOT_DIR
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            file_name = f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = screenshot_dir / file_name
            page.screenshot(path=str(path))
            logger.error(f"[SCREENSHOT CAPTURED] {make_clickable_link(str(path))}")

        context.close()
        browser.close()


# Pytest hook to access test outcome in fixture
def pytest_runtest_makereport(item, call):
    print(f"item.fixturenames => {item.fixturenames}  {item}")
    if "page" in item.fixturenames:
        setattr(item, "rep_" + call.when, call)
