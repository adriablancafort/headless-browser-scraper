from playwright.sync_api import sync_playwright


def launch_browser():
    """Launch the Playwright browser and return the context and browser."""

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(java_script_enabled=False)
    return playwright, browser, context


def close_browser(playwright, browser):
    """Close the Playwright browser and stop the Playwright context."""

    browser.close()
    playwright.stop()


def scrape_amazon_com(page, ASIN: int):
    """Scrape the Amazon product page for the given ASIN."""

    URL = f"https://www.amazon.com/dp/{ASIN}"
    page.goto(URL)

    title_element = page.query_selector('span#productTitle')
    price_symbol_element = page.query_selector('span.a-price-symbol')
    price_whole_element = page.query_selector('span.a-price-whole')
    price_fraction_element = page.query_selector('span.a-price-fraction')

    PRODUCT_TITLE = title_element.inner_text().strip() if title_element else "Title not found"
    PRICE_SYMBOL = price_symbol_element.inner_text() if price_symbol_element else "Symbol not found"
    PRICE_WHOLE = price_whole_element.inner_text().replace('.', '').strip() if price_whole_element else "Whole part not found"
    PRICE_FRACTION = price_fraction_element.inner_text() if price_fraction_element else "Fraction not found"

    print(f"Product Title: {PRODUCT_TITLE}")
    print(f"Price Symbol: {PRICE_SYMBOL}")
    print(f"Price Whole: {PRICE_WHOLE}")
    print(f"Price Fraction: {PRICE_FRACTION}")


def main():
    ASINs = ["B09LNW3CY2", "B009KYJAJY", "B0B2D77YB8", "B0D3KPGFHL"]
    playwright, browser, context = launch_browser()
    page = context.new_page()
    try:
        for ASIN in ASINs:
            scrape_amazon_com(page, ASIN)
    finally:
        close_browser(playwright, browser)


if __name__ == "__main__":
    main()