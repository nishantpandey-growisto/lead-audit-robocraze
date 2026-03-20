#!/usr/bin/env python3
"""Capture all mobile screenshots for Robocraze lead audit."""

from playwright.sync_api import sync_playwright

DIR = "/Users/growisto/Documents/Claude_Code/_audit_reports/robocraze-lead/screenshots"

def save(page, name):
    path = f"{DIR}/{name}"
    page.screenshot(path=path, type="jpeg", quality=85)
    print(f"  -> {name}")

def dismiss_popups(page):
    """Aggressively dismiss popups."""
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    page.evaluate("""
        // Remove all overlay/popup/modal elements
        document.querySelectorAll('[class*="popup"], [class*="modal"], [class*="overlay"], [class*="bitespeed"], [id*="popup"], [id*="modal"]').forEach(el => {
            if (el.style) el.style.display = 'none';
        });
        // Also remove any fixed/sticky overlays covering content
        document.querySelectorAll('*').forEach(el => {
            const style = getComputedStyle(el);
            if ((style.position === 'fixed' || style.position === 'sticky') && style.zIndex > 999 && el.offsetHeight > 400) {
                el.style.display = 'none';
            }
        });
    """)
    page.wait_for_timeout(500)

def new_mobile_page(browser):
    context = browser.new_context(
        viewport={"width": 375, "height": 812},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
    )
    return context, context.new_page()

def capture_homepage(browser):
    print("\n=== HOMEPAGE ===")
    ctx, page = new_mobile_page(browser)
    page.goto("https://robocraze.com", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)

    # Capture popup first
    save(page, "hp_f2_client.jpeg")  # popup screenshot

    dismiss_popups(page)
    page.wait_for_timeout(500)

    # Homepage first fold (after popup dismiss)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    save(page, "hp_f1_client.jpeg")

    # Scroll through homepage
    for i, y in enumerate([600, 1200, 2000, 3000, 4500, 6000], start=3):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(800)
        save(page, f"hp_f{i}_client.jpeg")

    height = page.evaluate("document.body.scrollHeight")
    print(f"  Page height: {height}")
    ctx.close()

def capture_collection(browser):
    print("\n=== COLLECTION ===")
    ctx, page = new_mobile_page(browser)
    page.goto("https://robocraze.com/collections/raspberry-pi", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    dismiss_popups(page)

    save(page, "col_f1_client.jpeg")

    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(800)
    save(page, "col_f2_client.jpeg")

    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(800)
    save(page, "col_f3_client.jpeg")

    # Also check a larger collection with filters
    page.goto("https://robocraze.com/collections/all", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)
    save(page, "col_f4_client.jpeg")

    ctx.close()

def capture_pdp(browser):
    print("\n=== PDP ===")
    ctx, page = new_mobile_page(browser)
    # Navigate to a product - let's find one from homepage
    page.goto("https://robocraze.com/collections/raspberry-pi", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)

    # Click first product
    try:
        products = page.query_selector_all('.product-item a, .grid-product a, .product-card a, [class*="product"] a[href*="/products/"]')
        if products:
            href = products[0].get_attribute("href")
            print(f"  Found product link: {href}")
            if href and not href.startswith("http"):
                href = f"https://robocraze.com{href}"
            page.goto(href, wait_until="domcontentloaded", timeout=30000)
        else:
            # Fallback to a known product
            page.goto("https://robocraze.com/products/raspberry-pi-5-8gb", wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print(f"  Error finding product: {e}")
        page.goto("https://robocraze.com/products/raspberry-pi-5-8gb", wait_until="domcontentloaded", timeout=30000)

    page.wait_for_timeout(3000)
    dismiss_popups(page)

    # PDP first fold
    save(page, "pdp_f1_client.jpeg")

    # Scroll through PDP
    for i, y in enumerate([500, 1000, 1500, 2000, 3000, 4000], start=2):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(800)
        save(page, f"pdp_f{i}_client.jpeg")

    # Check for sticky ATC by scrolling past fold
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(1000)
    save(page, "pdp_sticky_check.jpeg")

    # Get current URL for reference
    print(f"  PDP URL: {page.url}")

    ctx.close()

def capture_cart(browser):
    print("\n=== CART ===")
    ctx, page = new_mobile_page(browser)

    # Go to a product and add to cart first
    page.goto("https://robocraze.com/products/raspberry-pi-5-8gb", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)

    # Click Add to Cart
    try:
        atc_btn = page.query_selector('button[type="submit"][name="add"], .product-form__submit, [class*="add-to-cart"], button:has-text("Add to Cart"), button:has-text("ADD TO CART"), .addToCart')
        if atc_btn:
            atc_btn.click()
            page.wait_for_timeout(3000)
            print("  Clicked ATC")
            save(page, "cart_f1_client.jpeg")  # Cart drawer/popup after ATC
        else:
            print("  ATC button not found")
    except Exception as e:
        print(f"  ATC error: {e}")

    # Navigate to /cart page
    page.goto("https://robocraze.com/cart", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)
    save(page, "cart_f2_client.jpeg")

    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(800)
    save(page, "cart_f3_client.jpeg")

    ctx.close()

def capture_competitors(browser):
    print("\n=== COMPETITORS ===")

    # ThinkRobotics
    print("  ThinkRobotics...")
    ctx, page = new_mobile_page(browser)
    page.goto("https://thinkrobotics.com", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    dismiss_popups(page)
    save(page, "bench_hp_thinkrobotics.jpeg")

    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(800)
    save(page, "bench_hp_thinkrobotics_scroll.jpeg")

    # ThinkRobotics collection
    page.goto("https://thinkrobotics.com/collections", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)
    save(page, "bench_col_thinkrobotics.jpeg")

    # ThinkRobotics product (find one)
    try:
        links = page.query_selector_all('a[href*="/products/"]')
        if links:
            href = links[0].get_attribute("href")
            if href and not href.startswith("http"):
                href = f"https://thinkrobotics.com{href}"
            page.goto(href, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            dismiss_popups(page)
            save(page, "bench_pdp_thinkrobotics.jpeg")
            page.evaluate("window.scrollTo(0, 600)")
            page.wait_for_timeout(800)
            save(page, "bench_pdp_thinkrobotics_scroll.jpeg")
    except Exception as e:
        print(f"    Error: {e}")
    ctx.close()

    # The Pi Hut
    print("  The Pi Hut...")
    ctx, page = new_mobile_page(browser)
    page.goto("https://thepihut.com", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    dismiss_popups(page)
    save(page, "bench_hp_pihut.jpeg")

    # Pi Hut collection
    page.goto("https://thepihut.com/collections/raspberry-pi", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)
    save(page, "bench_col_pihut.jpeg")

    # Pi Hut PDP
    try:
        links = page.query_selector_all('a[href*="/products/"]')
        if links:
            href = links[0].get_attribute("href")
            if href and not href.startswith("http"):
                href = f"https://thepihut.com{href}"
            page.goto(href, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            dismiss_popups(page)
            save(page, "bench_pdp_pihut.jpeg")
            page.evaluate("window.scrollTo(0, 600)")
            page.wait_for_timeout(800)
            save(page, "bench_pdp_pihut_scroll.jpeg")
    except Exception as e:
        print(f"    Error: {e}")
    ctx.close()

    # Pimoroni
    print("  Pimoroni...")
    ctx, page = new_mobile_page(browser)
    page.goto("https://shop.pimoroni.com", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    dismiss_popups(page)
    save(page, "bench_hp_pimoroni.jpeg")

    # Pimoroni PDP
    try:
        links = page.query_selector_all('a[href*="/products/"]')
        if links:
            href = links[0].get_attribute("href")
            if href and not href.startswith("http"):
                href = f"https://shop.pimoroni.com{href}"
            page.goto(href, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            dismiss_popups(page)
            save(page, "bench_pdp_pimoroni.jpeg")
    except Exception as e:
        print(f"    Error: {e}")
    ctx.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        capture_homepage(browser)
        capture_collection(browser)
        capture_pdp(browser)
        capture_cart(browser)
        capture_competitors(browser)
        browser.close()
    print("\n=== DONE ===")
