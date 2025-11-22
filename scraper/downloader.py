import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import random
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)

class Downloader:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }

    def get_headers(self):
        headers = self.headers.copy()
        headers["User-Agent"] = self.ua.random
        return headers

    def fetch_static(self, url, retries=3):
        """Fetches page using requests (Static Mode)."""
        for i in range(retries):
            try:
                response = requests.get(url, headers=self.get_headers(), timeout=15)
                response.raise_for_status()
                return {
                    "content": response.text,
                    "status": response.status_code,
                    "url": response.url,
                    "method": "static"
                }
            except requests.RequestException as e:
                logger.warning(f"Attempt {i+1} failed for {url}: {e}")
                time.sleep(random.uniform(1, 3))
        return {"error": f"Failed to fetch {url} after {retries} attempts", "method": "static"}

    def fetch_dynamic(self, url, wait_selector=None, scroll=False):
        """Fetches page using Playwright (Dynamic Mode)."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(user_agent=self.ua.random)
                page = context.new_page()
                
                page.goto(url, timeout=60000)
                
                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=10000)
                    except:
                        logger.warning(f"Timeout waiting for selector {wait_selector}")

                if scroll:
                    self._auto_scroll(page)

                content = page.content()
                final_url = page.url
                browser.close()
                
                return {
                    "content": content,
                    "status": 200,
                    "url": final_url,
                    "method": "dynamic"
                }
        except Exception as e:
            logger.error(f"Playwright error for {url}: {e}")
            return {"error": str(e), "method": "dynamic"}

    def _auto_scroll(self, page):
        """Scrolls down the page to trigger lazy loading."""
        last_height = page.evaluate("document.body.scrollHeight")
        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def check_robots_txt(self, url):
        """Checks robots.txt for the given URL."""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = f"{base_url}/robots.txt"
        
        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                return response.text
        except:
            pass
        return None
