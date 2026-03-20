#!/usr/bin/env python3
"""Mobile screenshot capture for Robocraze lead audit."""

import sys
import json
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = "/Users/growisto/Documents/Claude_Code/_audit_reports/robocraze-lead/screenshots"

def capture(url, filename, wait_ms=3000, scroll_y=0, click_selector=None, full_page=False):
    """Capture a mobile screenshot."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(wait_ms)

        # Dismiss any popups
        try:
            page.evaluate("document.querySelectorAll('[class*=popup] [class*=close], [class*=modal] [class*=close]').forEach(el => el.click())")
        except:
            pass

        if click_selector:
            try:
                page.click(click_selector, timeout=5000)
                page.wait_for_timeout(1500)
            except:
                pass

        if scroll_y > 0:
            page.evaluate(f"window.scrollTo(0, {scroll_y})")
            page.wait_for_timeout(1000)

        filepath = f"{SCREENSHOTS_DIR}/{filename}"
        page.screenshot(path=filepath, type="jpeg", quality=85, full_page=full_page)
        browser.close()
        print(f"Saved: {filepath}")
        return filepath

if __name__ == "__main__":
    # Parse command line args as JSON
    args = json.loads(sys.argv[1])
    capture(**args)
