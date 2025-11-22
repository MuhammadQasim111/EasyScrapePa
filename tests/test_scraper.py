import pytest
from scraper.downloader import Downloader
from scraper.parser import Parser

def test_downloader_static():
    d = Downloader()
    result = d.fetch_static("https://example.com")
    assert result["status"] == 200
    assert "Example Domain" in result["content"]

def test_parser_extraction():
    html = """
    <html>
        <body>
            <h1>Test Title</h1>
            <a href="/link1">Link 1</a>
            <div class="content">Some text</div>
        </body>
    </html>
    """
    p = Parser(html, "https://example.com")
    links = p.extract_links()
    assert len(links) == 1
    assert links[0]["url"] == "https://example.com/link1"
    assert "Some text" in p.extract_text()

def test_structure_detection():
    html = """
    <html><body>
        <table><tr><td>Data</td></tr></table>
        <ul><li>Item</li></ul>
    </body></html>
    """
    p = Parser(html, "https://example.com")
    struct = p.detect_structure()
    assert struct["tables"] == 1
    assert struct["lists"] == 1
