from .downloader import Downloader
from .parser import Parser
import logging

logger = logging.getLogger(__name__)

class ScraperEngine:
    def __init__(self):
        self.downloader = Downloader()

    def run(self, url, mode="auto", wait_selector=None, scroll=False):
        """
        Main entry point for scraping.
        mode: 'static', 'dynamic', 'auto'
        """
        logger.info(f"Starting scrape for {url} in {mode} mode")
        
        # Auto-detection logic (simplified)
        if mode == "auto":
            # Heuristic: try static first, if low content or specific JS indicators, switch to dynamic
            # For now, we'll just default to static unless user specifies otherwise or we detect failure
            result = self.downloader.fetch_static(url)
            if "error" in result or len(result.get("content", "")) < 1000: # Arbitrary threshold
                logger.info("Static scrape insufficient, switching to dynamic")
                mode = "dynamic"
            else:
                mode = "static"

        if mode == "dynamic":
            result = self.downloader.fetch_dynamic(url, wait_selector, scroll)
        else:
            # If we already fetched in auto mode, don't refetch unless it failed
            if mode != "auto": 
                result = self.downloader.fetch_static(url)
            # If auto mode kept static, 'result' is already set

        if "error" in result:
            return {"success": False, "error": result["error"]}

        parser = Parser(result["content"], result["url"])
        
        data = {
            "success": True,
            "url": result["url"],
            "method": result["method"],
            "status": result["status"],
            "title": parser.soup.title.string if parser.soup.title else "",
            "text_content": parser.extract_text()[:5000], # Truncate for preview
            "links": parser.extract_links(),
            "images": parser.extract_images(),
            "structure": parser.detect_structure(),
            "json_ld": parser.extract_json_ld(),
            "html_preview": parser.get_preview()
        }
        
        return data

    def check_compliance(self, url):
        return self.downloader.check_robots_txt(url)
