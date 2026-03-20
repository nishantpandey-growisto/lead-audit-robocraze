#!/usr/bin/env python3
"""Capture PDP screenshots bypassing Cloudflare."""

from playwright.sync_api import sync_playwright

DIR = "/Users/growisto/Documents/Claude_Code/_audit_reports/robocraze-lead/screenshots"

def save(page, name):
    path = f"{DIR}/{name}"
    page.screenshot(path=path, type="jpeg", quality=85)
    print(f"  -> {name}")

def dismiss_popups(page):
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    page.evaluate("""
        document.querySelectorAll('[class*="popup"], [class*="modal"], [class*="overlay"], [class*="bitespeed"], [id*="popup"], [id*="modal"]').forEach(el => {
            if (el.style) el.style.display = 'none';
        });
        document.querySelectorAll('*').forEach(el => {
            const style = getComputedStyle(el);
            if ((style.position === 'fixed' || style.position === 'sticky') && parseInt(style.zIndex) > 999 && el.offsetHeight > 400) {
                el.style.display = 'none';
            }
        });
    """)
    page.wait_for_timeout(500)

with sync_playwright() as p:
    # Use non-headless to bypass Cloudflare
    browser = p.chromium.launch(headless=False, args=['--window-size=375,812'])
    context = browser.new_context(
        viewport={"width": 375, "height": 812},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    )
    page = context.new_page()

    # First visit homepage to get cookies
    print("Visiting homepage first...")
    page.goto("https://robocraze.com", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(5000)
    dismiss_popups(page)

    # Now visit PDP
    print("\n=== PDP ===")
    page.goto("https://robocraze.com/products/raspberry-pi-4-model-b-8-gb-ram", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(5000)
    dismiss_popups(page)

    # Remove floating review widget
    page.evaluate("""
        document.querySelectorAll('[class*="jdgm"], [class*="judge"]').forEach(el => {
            if (el.offsetHeight < 200) el.style.display = 'none';
        });
    """)

    save(page, "pdp_f1_client.jpeg")

    page.evaluate("window.scrollTo(0, 400)")
    page.wait_for_timeout(800)
    save(page, "pdp_f2_client.jpeg")

    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(800)
    save(page, "pdp_f3_client.jpeg")

    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(800)
    save(page, "pdp_f4_client.jpeg")

    page.evaluate("window.scrollTo(0, 1800)")
    page.wait_for_timeout(800)
    save(page, "pdp_f5_client.jpeg")

    page.evaluate("window.scrollTo(0, 2500)")
    page.wait_for_timeout(800)
    save(page, "pdp_f6_client.jpeg")

    page.evaluate("window.scrollTo(0, 3500)")
    page.wait_for_timeout(800)
    save(page, "pdp_f7_client.jpeg")

    # Check sticky ATC
    page.evaluate("window.scrollTo(0, 1500)")
    page.wait_for_timeout(1000)
    save(page, "pdp_sticky_check.jpeg")

    # Cart page
    print("\n=== CART ===")
    page.goto("https://robocraze.com/products/raspberry-pi-4-model-b-8-gb-ram", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)

    # Try adding to cart
    try:
        atc = page.query_selector('button:has-text("Add to cart"), button:has-text("ADD TO CART"), .btn-addtocart')
        if atc:
            atc.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            atc.click()
            page.wait_for_timeout(3000)
            save(page, "cart_drawer_client.jpeg")
    except Exception as e:
        print(f"  ATC click error: {e}")

    page.goto("https://robocraze.com/cart", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(3000)
    dismiss_popups(page)
    save(page, "cart_f1_client.jpeg")

    page.evaluate("window.scrollTo(0, 400)")
    page.wait_for_timeout(800)
    save(page, "cart_f2_client.jpeg")

    browser.close()
    print("\n=== DONE ===")
