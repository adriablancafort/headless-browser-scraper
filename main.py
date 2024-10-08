from playwright.sync_api import sync_playwright, Playwright, Browser, Page, Route
from dotenv import load_dotenv
import os


load_dotenv()

PROXY_SERVER = os.getenv("PROXY_SERVER")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

def launch_browser() -> tuple[Playwright, Browser]:
    """Launch the Playwright browser and return the context and browser."""

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        proxy = {
            "server": PROXY_SERVER,
            "username": PROXY_USERNAME,
            "password": PROXY_PASSWORD
        },
        headless=True
    )
    return playwright, browser


def close_browser(playwright: Playwright, browser: Browser) -> None:
    """Close the Playwright browser and stop the Playwright context."""

    browser.close()
    playwright.stop()


def block_all_resources(route: Route) -> None:
    """Block all the resources except HTML documents."""

    if route.request.resource_type != "document":
        route.abort()
    elif "ads" in route.request.url or "analytics" in route.request.url:
        route.abort()
    else:
        route.continue_()


def scrape_amazon_com(page: Page, ASIN: str) -> None:
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


def main() -> None:
    playwright, browser = launch_browser()
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()

    page.route("**/*", block_all_resources) # Block everything except HTML documents

    ASINs = ["B09LNW3CY2", "B009KYJAJY", "B0B2D77YB8", "B0D3KPGFHL"]

    try:
        for ASIN in ASINs:
            scrape_amazon_com(page, ASIN)
    finally:
        close_browser(playwright, browser)


if __name__ == "__main__":
    main()