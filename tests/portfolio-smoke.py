"""Cross-device smoke checks for the AdventureX portfolio."""

from __future__ import annotations

import json
import sys

from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8765/"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def inspect_page(page, name: str) -> dict:
    errors: list[str] = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    response = page.goto(BASE_URL, wait_until="domcontentloaded")
    require(response is not None and response.status == 200, f"{name}: homepage did not return 200")

    initial_video_src = page.locator("[data-media-dialog] video").get_attribute("src")
    require(initial_video_src is None, f"{name}: scrna video loaded before user action")
    require(page.locator("h1").count() == 1, f"{name}: expected one H1")
    require(page.get_by_text("独立构建者。", exact=True).count() == 1, f"{name}: identity line missing")
    require(page.locator('img[src*="portrait"]').count() == 0, f"{name}: portrait is still used on the website")
    require(page.get_by_text("时机成熟了。我想参与其中。", exact=True).count() == 0, f"{name}: rejected hero copy remains")
    require(page.locator(".research-list > a").count() == 8, f"{name}: expected eight small projects")
    require(page.locator('img[src*="timebox-ai-v2"]').count() == 1, f"{name}: TimeBox v2 evidence is missing")
    require(page.locator('img[src*="gogowork-marketplace"]').count() == 1, f"{name}: GoGoWork marketplace evidence is missing")

    page.wait_for_load_state("networkidle")
    page.locator('[data-project-trigger="mirror"]').click()
    require(
        page.locator('[data-project-trigger="mirror"]').get_attribute("aria-expanded") == "true",
        f"{name}: Mirror did not expand",
    )
    require(not page.locator("#project-mirror").get_attribute("hidden"), f"{name}: Mirror panel is hidden")

    state = page.evaluate(
        """() => ({
          bodyWidth: document.body.scrollWidth,
          viewportWidth: innerWidth,
          heroReady: document.querySelector('[data-hero]')?.classList.contains('is-ready'),
          scrnaMetric: document.querySelector('#scrna-omics')?.textContent.includes('13'),
          resumeHref: document.querySelector('a[href*="AdventureX"]')?.getAttribute('href')
        })"""
    )
    require(state["bodyWidth"] == state["viewportWidth"], f"{name}: horizontal overflow")
    require(state["heroReady"], f"{name}: hero reveal did not initialize")
    require(state["scrnaMetric"], f"{name}: scrna evidence is missing")
    require(state["resumeHref"], f"{name}: resume link is missing")
    require(not errors, f"{name}: browser errors: {errors}")
    return state


def main() -> int:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        desktop = browser.new_page(viewport={"width": 1440, "height": 1000})
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        reduced = browser.new_page(viewport={"width": 1440, "height": 1000})
        reduced.emulate_media(reduced_motion="reduce")

        results = {
            "desktop": inspect_page(desktop, "desktop"),
            "mobile": inspect_page(mobile, "mobile"),
        }

        reduced.goto(BASE_URL, wait_until="networkidle")
        reduced.wait_for_timeout(2100)
        results["reduced_motion"] = reduced.evaluate(
            """() => ({
              loaded: document.querySelector('[data-hero-video]')?.dataset.loaded || null,
              overflow: document.body.scrollWidth === innerWidth
            })"""
        )
        require(results["reduced_motion"]["loaded"] is None, "reduced motion loaded the hero video")
        require(results["reduced_motion"]["overflow"], "reduced-motion layout overflowed")
        browser.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
