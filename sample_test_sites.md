# Sample Test Sites

Use these sites to test different capabilities of the scraper.

1.  **Static Content**: `https://example.com`
    - Simple HTML, no JS required.
2.  **E-commerce (Pagination)**: `https://webscraper.io/test-sites/e-commerce/static`
    - Good for testing list extraction and pagination detection.
3.  **Dynamic Content (JS)**: `https://webscraper.io/test-sites/e-commerce/allinone`
    - Requires Playwright to render items.
4.  **Infinite Scroll**: `https://webscraper.io/test-sites/e-commerce/scroll`
    - Test the auto-scroll feature.
5.  **Table Data**: `https://www.w3schools.com/html/html_tables.asp`
    - Test table detection and extraction.
6.  **JSON-LD**: `https://schema.org/Product`
    - Test structured data extraction.
7.  **Login Required**: `https://the-internet.herokuapp.com/login`
    - Test form detection (Note: Auth implementation requires custom script extension).
8.  **Broken/404**: `https://httpbin.org/status/404`
    - Test error handling.
9.  **Delayed Loading**: `https://httpbin.org/delay/3`
    - Test timeout handling.
10. **Robots.txt**: `https://www.google.com`
    - Test compliance check.
