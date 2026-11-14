"""Smoke-test the built public portfolio served at PORTFOLIO_URL."""

from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("PORTFOLIO_URL", "http://127.0.0.1:8768/")
OUTPUT = Path(os.environ.get("PORTFOLIO_SCREENSHOTS", "/tmp/portfolio-smoke"))


def inspect(page, name: str) -> None:
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    response = page.goto(BASE_URL, wait_until="networkidle")
    assert response and response.status == 200
    assert page.get_by_role("heading", level=1).count() == 1
    assert "口腔医学在读" in page.locator(".hero-aside").inner_text()
    assert page.locator(".project-row").count() == 12
    assert page.get_by_role("link", name="作品索引").count() == 1
    assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
    assert page.locator("#featured img").evaluate(
        "image => image.complete && image.naturalWidth > 0"
    )

    page.get_by_role("button", name="医学与科研").click()
    assert "显示 4 个项目" in page.locator("#result-count").inner_text()
    page.get_by_role("link", name="儿童牙外伤科普").click()
    dialog = page.get_by_role("dialog")
    dialog.wait_for(state="visible")
    assert "口腔健康教育" in dialog.inner_text()
    page.get_by_role("button", name="关闭项目详情").press("Escape")
    assert not dialog.is_visible()
    page.get_by_role("button", name="全部", exact=True).click()
    page.get_by_role("link", name="GoGoWork").click()
    dialog.wait_for(state="visible")
    assert "团队项目" in dialog.inner_text()
    assert dialog.locator("img").count() == 0
    page.get_by_role("button", name="关闭项目详情").click()
    page.get_by_role("link", name="TimeBox").click()
    dialog.wait_for(state="visible")
    page.wait_for_function("document.querySelector('dialog img')?.naturalWidth > 0")
    page.get_by_role("button", name="关闭项目详情").click()
    assert not errors, errors
    page.goto(BASE_URL, wait_until="networkidle")
    page.screenshot(path=str(OUTPUT / f"{name}.png"), full_page=True)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        for name, size in [
            ("desktop", {"width": 1440, "height": 900}),
            ("mobile", {"width": 390, "height": 844}),
        ]:
            context = browser.new_context(viewport=size, reduced_motion="reduce")
            inspect(context.new_page(), name)
            context.close()
        request = browser.new_page().request
        for route in (
            "/CHECKPOINT.md",
            "/.git/config",
            "/docs/",
            "/%2e%2e/site/server.js",
        ):
            assert request.get(BASE_URL.rstrip("/") + route).status == 404, route
        browser.close()
    print("Desktop, mobile, interactions, images and private-path checks passed")


if __name__ == "__main__":
    main()
