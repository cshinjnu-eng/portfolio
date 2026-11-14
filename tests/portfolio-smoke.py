"""Check generated portfolio routes, interactions, media, and private-path boundaries."""

import os
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

BASE = os.environ.get("PORTFOLIO_URL", "http://127.0.0.1:8768/")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        for width in (1440, 390):
            context = browser.new_context(
                viewport={"width": width, "height": 900}, reduced_motion="reduce"
            )
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            assert page.goto(BASE, wait_until="networkidle").status == 200
            assert page.locator("h1").count() == 1
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            for img in page.locator("img").all():
                img.scroll_into_view_if_needed()
                assert img.evaluate("el => el.complete && el.naturalWidth > 0")
            page.goto(urljoin(BASE, "projects/"))
            assert page.locator(".archive-item").count() == 17
            page.locator("#search").fill("TimeBox")
            assert page.locator(".archive-item:visible").count() == 1
            page.locator("#search").fill("")
            page.get_by_role("button", name="医学与科研").click()
            assert 0 < page.locator(".archive-item:visible").count() < 17
            page.get_by_role("button", name="全部", exact=True).click()
            assert page.locator(".archive-item:visible").count() == 17
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        request = browser.new_page().request
        html = request.get(urljoin(BASE, "projects/")).text()
        import re

        routes = set(re.findall(r'href="(/projects/[^"#]+/)"', html))
        assert len(routes) == 17, len(routes)
        for route in routes:
            response = request.get(urljoin(BASE, route))
            assert response.status == 200, route
            assert "状态与边界" in response.text(), route
            for asset in re.findall(
                r'(?:src|poster|data-src)="(/assets/[^"]+)"', response.text()
            ):
                assert request.get(urljoin(BASE, asset)).status == 200, asset
        for route in (
            "/CHECKPOINT.md",
            "/.git/config",
            "/docs/",
            "/%2e%2e/site/server.js",
        ):
            assert request.get(urljoin(BASE, route)).status == 404, route
        browser.close()
    print("Portfolio routes, assets, filters, mobile overflow and private paths passed")


if __name__ == "__main__":
    main()
