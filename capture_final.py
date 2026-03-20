#!/usr/bin/env python3
"""Final screenshot capture for specific findings."""

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

def new_mobile_page(browser):
    context = browser.new_context(
        viewport={"width": 375, "height": 812},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
    )
    return context, context.new_page()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # 1. Robocraze PDP - with cookies to bypass Cloudflare
    print("=== Robocraze PDP via collection ===")
    ctx, page = new_mobile_page(browser)
    page.goto("https://robocraze.com/collections/raspberry-pi", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    dismiss_popups(page)

    # Click on Raspberry Pi 4
    try:
        page.click('text=Raspberry Pi 4 Model B 8 GB RAM', timeout=5000)
        page.wait_for_timeout(4000)
        dismiss_popups(page)
        save(page, "pdp_f1_client.jpeg")

        # Scroll PDP
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

        # Test sticky ATC
        page.evaluate("window.scrollTo(0, 1500)")
        page.wait_for_timeout(1000)
        save(page, "pdp_sticky_check.jpeg")

        # Try adding to cart
        try:
            page.click('text=Add to cart', timeout=5000)
            page.wait_for_timeout(3000)
            save(page, "cart_drawer_client.jpeg")
        except:
            print("  Could not click ATC")

        # Go to cart
        page.goto("https://robocraze.com/cart", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        dismiss_popups(page)
        save(page, "cart_f1_client.jpeg")

        page.evaluate("window.scrollTo(0, 400)")
        page.wait_for_timeout(800)
        save(page, "cart_f2_client.jpeg")

    except Exception as e:
        print(f"  Error: {e}")
    ctx.close()

    # 2. ThinkRobotics PDP
    print("\n=== ThinkRobotics PDP ===")
    ctx, page = new_mobile_page(browser)
    page.goto("https://thinkrobotics.com/collections/all", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    dismiss_popups(page)
    save(page, "bench_col_thinkrobotics_all.jpeg")

    # Find a product
    try:
        links = page.query_selector_all('a[href*="/products/"]')
        if links and len(links) > 2:
            href = links[2].get_attribute("href")
            if not href.startswith("http"):
                href = f"https://thinkrobotics.com{href}"
            page.goto(href, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            dismiss_popups(page)
            save(page, "bench_pdp_thinkrobotics_2.jpeg")
            page.evaluate("window.scrollTo(0, 500)")
            page.wait_for_timeout(800)
            save(page, "bench_pdp_thinkrobotics_2_scroll.jpeg")
    except Exception as e:
        print(f"  Error: {e}")
    ctx.close()

    # 3. The Pi Hut PDP
    print("\n=== The Pi Hut PDP ===")
    ctx, page = new_mobile_page(browser)
    page.goto("https://thepihut.com/products/raspberry-pi-5", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    dismiss_popups(page)
    save(page, "bench_pdp_pihut_rpi5.jpeg")
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(800)
    save(page, "bench_pdp_pihut_rpi5_scroll.jpeg")
    page.evaluate("window.scrollTo(0, 1000)")
    page.wait_for_timeout(800)
    save(page, "bench_pdp_pihut_rpi5_scroll2.jpeg")

    # Pi Hut cart
    try:
        page.click('button:has-text("Add to cart"), [name="add"]', timeout=5000)
        page.wait_for_timeout(3000)
        save(page, "bench_cart_pihut.jpeg")
    except:
        print("  Could not add to cart")
    ctx.close()

    # 4. Pimoroni PDP (retry without timeout issue)
    print("\n=== Pimoroni ===")
    ctx, page = new_mobile_page(browser)
    try:
        page.goto("https://shop.pimoroni.com/products/raspberry-pi-5", wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(4000)
        dismiss_popups(page)
        save(page, "bench_pdp_pimoroni_rpi5.jpeg")
    except Exception as e:
        print(f"  Error: {e}")
        try:
            page.goto("https://shop.pimoroni.com", wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(4000)
            dismiss_popups(page)
            save(page, "bench_hp_pimoroni.jpeg")
        except:
            print("  Pimoroni failed completely")
    ctx.close()

    browser.close()
    print("\n=== DONE ===")
