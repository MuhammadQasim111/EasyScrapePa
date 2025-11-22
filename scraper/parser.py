from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin

class Parser:
    def __init__(self, html_content, base_url):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.base_url = base_url

    def extract_text(self):
        """Extracts all visible text."""
        return self.soup.get_text(separator='\n', strip=True)

    def extract_links(self):
        """Extracts all links."""
        links = []
        for a in self.soup.find_all('a', href=True):
            full_url = urljoin(self.base_url, a['href'])
            links.append({"text": a.get_text(strip=True), "url": full_url})
        return links

    def extract_images(self):
        """Extracts all images."""
        images = []
        for img in self.soup.find_all('img', src=True):
            full_url = urljoin(self.base_url, img['src'])
            images.append({"alt": img.get('alt', ''), "src": full_url})
        return images

    def detect_structure(self):
        """Detects potential structured data (tables, lists, JSON-LD)."""
        structure = {
            "tables": len(self.soup.find_all('table')),
            "lists": len(self.soup.find_all(['ul', 'ol'])),
            "json_ld": len(self.soup.find_all('script', type='application/ld+json')),
            "articles": len(self.soup.find_all('article')),
            "products": len(self.soup.select('.product, .item, [itemtype*="Product"]'))
        }
        return structure

    def extract_json_ld(self):
        """Extracts JSON-LD data."""
        data = []
        for script in self.soup.find_all('script', type='application/ld+json'):
            try:
                data.append(json.loads(script.string))
            except:
                pass
        return data

    def extract_by_selector(self, selector):
        """Extracts data using a CSS selector."""
        results = []
        for item in self.soup.select(selector):
            results.append(item.get_text(strip=True))
        return results
    
    def get_preview(self):
        """Returns a simplified HTML preview."""
        # Remove scripts and styles for cleaner preview
        for script in self.soup(["script", "style"]):
            script.decompose()
        return str(self.soup)
