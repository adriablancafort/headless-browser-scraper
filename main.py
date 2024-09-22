from playwright.sync_api import sync_playwright, Playwright, Browser, Page
import time


def launch_browser() -> tuple[Playwright, Browser]:
    """Launch the Playwright browser and return the context and browser."""

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    return playwright, browser


def close_browser(playwright: Playwright, browser: Browser) -> None:
    """Close the Playwright browser and stop the Playwright context."""

    browser.close()
    playwright.stop()


def block_all_resources(route):
    """Block all the resources except the document."""

    if route.request.resource_type == "document":
        print(f"Allowing: {route.request.url}")
        route.continue_()
    else:
        route.abort()


def scrape_amazon_com(page: Page, ASIN: int) -> None:
    """Scrape the Amazon product page for the given ASIN."""

    request_count = 0

    def on_request(request):
        nonlocal request_count
        if request.resource_type == "document":
            request_count += 1

    page.route("**/*", block_all_resources) # Block everything except HTML
    page.on("request", on_request)

    URL = f"https://www.amazon.com/dp/{ASIN}"

    start_time = time.time()

    page.goto(URL)

    end_time = time.time()
    total_time = end_time - start_time

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

    print("="*20, "Results", "="*20)
    print(f"Total requests: {request_count}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print("="*50)


def main() -> None:
    ASINs = ["B09LNW3CY2", "B009KYJAJY", "B0B2D77YB8", "B0D3KPGFHL"]
    playwright, browser = launch_browser()
    page = browser.new_page()
    try:
        for ASIN in ASINs:
            scrape_amazon_com(page, ASIN)
    finally:
        close_browser(playwright, browser)


if __name__ == "__main__":
    main()