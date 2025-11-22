# Antigravity Web Scraper

A production-ready, full-stack web scraper built with Streamlit, Playwright, and optional Gemini AI integration.

## Features

- **Dual-Mode Scraping**: 
  - **Static**: Fast, lightweight using `requests`.
  - **Dynamic**: Full browser rendering using `playwright` for JS-heavy sites.
- **AI Integration**: Optional Gemini 2.0 Flash integration for summarization and entity extraction.
- **Visual Inspector**: Inspect HTML structure directly in the UI.
- **Compliance**: Built-in `robots.txt` checking and PII redaction.
- **Export**: CSV and JSON export with PII masking.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Install Playwright Browsers**:
    ```bash
    playwright install
    ```

3.  **Environment Variables** (Optional):
    Create a `.env` file or set variables:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

## Running the App

```bash
streamlit run app.py
```

## Testing

Run unit tests with pytest:
```bash
pytest tests/
```

## Why this is better than ChatGPT Browsing?

1.  **Control**: You choose the rendering engine (Static vs Dynamic).
2.  **Persistence**: History and data are saved locally.
3.  **Scale**: Can handle pagination and infinite scroll (configurable).
4.  **Structured Data**: Extracts specific entities and JSON-LD, not just text summaries.
5.  **Privacy**: Runs locally, PII redaction included.

## Legal Disclaimer

This tool is for educational and testing purposes. Always respect `robots.txt` and Terms of Service of target websites.
