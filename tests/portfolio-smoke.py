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
    page.on(
        "console", lambda msg: errors.append(msg.text) if msg.type == "error" else None
    )
    page.on("pageerror", lambda error: errors.append(str(error)))
    response = page.goto(BASE_URL, wait_until="domcontentloaded")
    require(
        response is not None and response.status == 200,
        f"{name}: homepage did not return 200",
    )

    initial_video_src = page.locator("[data-media-dialog] video").get_attribute("src")
    require(initial_video_src is None, f"{name}: scrna video loaded before user action")
    require(page.locator("h1").count() == 1, f"{name}: expected one H1")
    require(
        page.get_by_text("缺的工具，自己写。", exact=True).count() == 1,
        f"{name}: identity line missing",
    )
    require(
        page.locator('img[src*="portrait"]').count() == 0,
        f"{name}: portrait is still used on the website",
    )
    require(
        page.get_by_text("时机成熟了。我想参与其中。", exact=True).count() == 0,
        f"{name}: rejected hero copy remains",
    )
    require(
        page.locator(".research-list > a").count() == 8,
        f"{name}: expected eight small projects",
    )
    require(
        page.locator('img[src*="timebox-ai-v2"]').count() == 1,
        f"{name}: TimeBox v2 evidence is missing",
    )
    require(
        page.locator('img[src*="gogowork-marketplace"]').count() == 1,
        f"{name}: GoGoWork marketplace evidence is missing",
    )
    archive = page.locator(".media-archive")
    require(archive.count() == 1, f"{name}: media archive is missing")
    require(
        archive.get_attribute("open") is not None,
        f"{name}: media archive should start expanded",
    )
    require(
        page.locator("[data-public-video]").count() == 4,
        f"{name}: expected four public videos",
    )
    require(
        page.locator('a[href*="scRNA-seq-gdT-psoriasis"]').count() >= 2,
        f"{name}: public single-cell analysis evidence is missing",
    )
    require(
        page.get_by_text("67,742 个细胞", exact=False).count() >= 1
        and page.get_by_text("8 个亚群", exact=False).count() >= 1,
        f"{name}: public single-cell evidence facts are missing",
    )
    journey = page.locator("[data-builder-journey]")
    require(journey.count() == 1, f"{name}: builder journey is missing")
    require(
        page.locator("[data-builder-step]").count() == 4,
        f"{name}: expected four builder steps",
    )
    counter_values = page.locator("[data-count-value]").evaluate_all(
        "els => els.map(el => el.dataset.countValue)"
    )
    require(
        counter_values == ["44735", "12", "8.8"],
        f"{name}: builder evidence counters are incorrect",
    )
    require(
        "8.80 B Token"
        in " ".join(page.locator(".builder-evidence").inner_text().split()),
        f"{name}: long-range token evidence is missing",
    )
    require(
        page.get_by_text(
            "数据来自 CC-Switch 本地统计，共 8,798,010,310 Token。Antigravity 和绕开 CC-Switch 的 API 还没算进去。这组数字只记录我写了多少、跑了多少，不代表产品效果。",
            exact=True,
        ).count()
        == 1,
        f"{name}: workflow evidence qualifier is missing",
    )
    require(
        page.get_by_text("我们可以聊聊。", exact=True).count() == 1,
        f"{name}: revised collaboration invitation is missing",
    )
    require(
        page.get_by_text("在小红书账号内运营两个近", exact=False).count() == 1,
        f"{name}: Xiaohongshu community attribution is missing",
    )
    require(
        page.get_by_text("微信社群", exact=False).count() == 0,
        f"{name}: communities are still misattributed to WeChat",
    )
    require(
        page.get_by_text("正在寻找合作。", exact=True).count() == 0,
        f"{name}: rejected collaboration copy remains",
    )
    require(
        page.locator(".proof-strip").count() == 0,
        f"{name}: obsolete proof strip is still present",
    )
    risk = page.locator(".risk-case")
    require(risk.count() == 1, f"{name}: risk project summary is missing")
    require(
        risk.get_attribute("open") is None,
        f"{name}: risk project should start collapsed",
    )
    video_hrefs = page.locator("[data-public-video]").evaluate_all(
        "els => els.map(el => el.getAttribute('href'))"
    )
    expected_ids = {
        "6a23b6a7000000003502f93f",
        "6a0d05180000000036001c6d",
        "6a095879000000003501fbf5",
        "6a06ab44000000003502052f",
    }
    require(
        all(any(note_id in href for href in video_hrefs) for note_id in expected_ids),
        f"{name}: public video IDs do not match the audit",
    )

    magnetic = page.locator("[data-magnetic]").first
    if name == "desktop":
        page.keyboard.press("Tab")
        keyboard_focus = page.evaluate(
            """() => ({
              label: document.activeElement?.getAttribute('aria-label'),
              outline: getComputedStyle(document.activeElement).outlineStyle
            })"""
        )
        require(
            keyboard_focus["label"] == "返回首页"
            and keyboard_focus["outline"] != "none",
            "desktop: keyboard focus is not visible on the first navigation link",
        )
        hero = page.locator("[data-hero]")
        hero_bounds = hero.bounding_box()
        require(hero_bounds is not None, "desktop: hero has no bounds")
        hero.dispatch_event("pointerenter")
        hero.dispatch_event(
            "pointermove",
            {
                "clientX": hero_bounds["x"] + hero_bounds["width"] - 24,
                "clientY": hero_bounds["y"] + 40,
            },
        )
        page.wait_for_timeout(80)
        hero_state = hero.evaluate(
            """el => ({
              x: el.style.getPropertyValue('--hero-x'),
              depth: el.style.getPropertyValue('--depth-x'),
              active: el.classList.contains('is-pointer-active')
            })"""
        )
        require(hero_state["active"], "desktop: hero pointer field did not activate")
        require(
            abs(float(hero_state["x"].removesuffix("px"))) > 10
            and abs(float(hero_state["depth"].removesuffix("px"))) > 20,
            "desktop: hero pointer response is not visually meaningful",
        )
        hero.dispatch_event("pointerleave")
        page.wait_for_timeout(80)
        require(
            hero.evaluate("el => el.style.getPropertyValue('--hero-x')") == "0px",
            "desktop: hero did not reset after pointer leave",
        )
        bounds = magnetic.bounding_box()
        require(bounds is not None, "desktop: magnetic CTA has no bounds")
        magnetic.dispatch_event(
            "pointerenter",
            {
                "clientX": bounds["x"] + bounds["width"] / 2,
                "clientY": bounds["y"] + bounds["height"] / 2,
            },
        )
        magnetic.dispatch_event(
            "pointermove",
            {
                "clientX": bounds["x"] + bounds["width"] - 3,
                "clientY": bounds["y"] + 3,
            },
        )
        page.wait_for_timeout(80)
        magnetic_state = magnetic.evaluate(
            """el => ({
              x: el.style.getPropertyValue('--magnetic-x'),
              y: el.style.getPropertyValue('--magnetic-y'),
              active: el.classList.contains('is-magnetic')
            })"""
        )
        require(magnetic_state["active"], "desktop: magnetic CTA did not activate")
        x_value = float(magnetic_state["x"].removesuffix("px"))
        y_value = float(magnetic_state["y"].removesuffix("px"))
        require(
            0 < abs(x_value) <= 10 and 0 < abs(y_value) <= 10,
            "desktop: magnetic CTA movement is missing or exceeds its limit",
        )
        magnetic.dispatch_event("pointerleave")
        page.wait_for_timeout(340)
        reset_state = magnetic.evaluate(
            """el => ({
              x: el.style.getPropertyValue('--magnetic-x'),
              y: el.style.getPropertyValue('--magnetic-y'),
              active: el.classList.contains('is-magnetic')
            })"""
        )
        require(
            reset_state == {"x": "0px", "y": "0px", "active": False},
            "desktop: magnetic CTA did not reset on pointer leave",
        )
    elif name == "mobile":
        coarse_state = magnetic.evaluate(
            """el => ({
              x: el.style.getPropertyValue('--magnetic-x'),
              y: el.style.getPropertyValue('--magnetic-y'),
              active: el.classList.contains('is-magnetic')
            })"""
        )
        require(
            coarse_state == {"x": "", "y": "", "active": False},
            "mobile: coarse pointer initialized magnetic movement",
        )

    archive.locator("summary").focus()
    archive.locator("summary").press("Enter")
    require(
        archive.get_attribute("open") is None,
        f"{name}: media archive did not collapse",
    )
    archive.locator("summary").press("Enter")
    require(
        archive.get_attribute("open") is not None,
        f"{name}: media archive did not expand again",
    )

    page.locator("[data-builder-step]").first.scroll_into_view_if_needed()
    page.wait_for_function(
        "() => document.querySelectorAll('[data-builder-step].is-active').length >= 1"
    )
    require(
        page.locator("[data-builder-step].is-active").count() >= 1,
        f"{name}: builder journey did not activate",
    )
    page.locator(".builder-evidence").scroll_into_view_if_needed()
    page.wait_for_function(
        """() => [...document.querySelectorAll('[data-count-value]')]
          .map(el => el.textContent.trim()).join(',') === '44,735,12,8.80'"""
    )
    require(
        page.locator('[data-count-value="44735"]').inner_text() == "44,735",
        f"{name}: request counter did not reach its final value",
    )
    require(
        page.locator('[data-count-value="12"]').inner_text() == "12",
        f"{name}: model counter did not reach its final value",
    )
    require(
        page.locator('[data-count-value="8.8"]').inner_text() == "8.80",
        f"{name}: token counter did not reach its final value",
    )

    page.locator('[data-project-trigger="gogowork"]').focus()
    page.locator('[data-project-trigger="gogowork"]').press("Enter")
    require(
        page.locator('[data-project-trigger="gogowork"]').get_attribute("aria-expanded")
        == "true",
        f"{name}: GoGoWork did not expand",
    )
    gogowork_secondary = page.locator(".gogowork-visual img:nth-of-type(2)")
    gogowork_secondary.wait_for(state="visible")
    page.wait_for_function(
        "() => document.querySelector('.gogowork-visual img:nth-of-type(2)')?.naturalWidth > 0"
    )
    image_fit = gogowork_secondary.evaluate(
        """img => {
          const box = img.getBoundingClientRect();
          return {
            naturalRatio: img.naturalWidth / img.naturalHeight,
            renderedRatio: box.width / box.height,
            objectFit: getComputedStyle(img).objectFit
          };
        }"""
    )
    require(
        image_fit["objectFit"] == "contain"
        and abs(image_fit["naturalRatio"] - image_fit["renderedRatio"]) < 0.03,
        f"{name}: GoGoWork secondary screenshot is cropped",
    )

    risk.locator("summary").focus()
    risk.locator("summary").press("Enter")
    require(
        risk.get_attribute("open") is not None,
        f"{name}: risk project did not expand",
    )

    page.locator('[data-project-trigger="mirror"]').focus()
    page.locator('[data-project-trigger="mirror"]').press("Enter")
    require(
        page.locator('[data-project-trigger="mirror"]').get_attribute("aria-expanded")
        == "true",
        f"{name}: Mirror did not expand",
    )
    require(
        not page.locator("#project-mirror").get_attribute("hidden"),
        f"{name}: Mirror panel is hidden",
    )

    state = page.evaluate(
        """() => ({
          bodyWidth: document.body.scrollWidth,
          documentWidth: document.documentElement.scrollWidth,
          viewportWidth: innerWidth,
          heroReady: document.querySelector('[data-hero]')?.classList.contains('is-ready'),
          builderReady: document.querySelector('[data-builder-journey]')?.dataset.motionReady === 'true',
          scrnaMetric: document.querySelector('#scrna-omics')?.textContent.includes('13'),
          publicVideos: document.querySelectorAll('[data-public-video]').length,
          resumeHref: document.querySelector('a[href*="AdventureX"]')?.getAttribute('href')
        })"""
    )
    require(
        state["bodyWidth"] == state["viewportWidth"]
        and state["documentWidth"] == state["viewportWidth"],
        f"{name}: horizontal overflow",
    )
    require(state["heroReady"], f"{name}: hero reveal did not initialize")
    require(state["builderReady"], f"{name}: builder motion did not initialize")
    require(state["scrnaMetric"], f"{name}: scrna evidence is missing")
    require(state["resumeHref"], f"{name}: resume link is missing")
    require(not errors, f"{name}: browser errors: {errors}")
    return state


def main() -> int:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        desktop = browser.new_page(viewport={"width": 1440, "height": 1000})
        tablet = browser.new_page(viewport={"width": 1024, "height": 768})
        mobile_context = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
        )
        mobile = mobile_context.new_page()
        reduced = browser.new_page(viewport={"width": 1440, "height": 1000})
        reduced.emulate_media(reduced_motion="reduce")

        results = {
            "desktop": inspect_page(desktop, "desktop"),
            "tablet": inspect_page(tablet, "tablet"),
            "mobile": inspect_page(mobile, "mobile"),
        }

        reduced.goto(BASE_URL, wait_until="domcontentloaded")
        reduced.wait_for_timeout(100)
        reduced.mouse.move(820, 520)
        results["reduced_motion"] = reduced.evaluate(
            """() => ({
              loaded: document.querySelector('[data-hero-video]')?.dataset.loaded || null,
              sourcesEmpty: [...document.querySelectorAll('[data-hero-video] source')]
                .every(source => !source.getAttribute('src')),
              overflow: document.body.scrollWidth === innerWidth
                && document.documentElement.scrollWidth === innerWidth,
              journeyReadable: [...document.querySelectorAll('[data-builder-step]')]
                .every(step => {
                  const style = getComputedStyle(step);
                  return style.opacity === '1' && style.transform === 'none';
                }),
              countersFinal: [...document.querySelectorAll('[data-count-value]')]
                .map(el => el.textContent.trim()).join(',') === '44,735,12,8.80',
              magneticDisabled: [...document.querySelectorAll('[data-magnetic]')]
                .every(el => getComputedStyle(el).transform === 'none'
                  && el.style.getPropertyValue('--magnetic-x') === '')
            })"""
        )
        require(
            results["reduced_motion"]["loaded"] is None,
            "reduced motion loaded the hero video",
        )
        require(
            results["reduced_motion"]["sourcesEmpty"],
            "reduced motion populated hero video sources",
        )
        require(
            results["reduced_motion"]["overflow"], "reduced-motion layout overflowed"
        )
        require(
            results["reduced_motion"]["journeyReadable"],
            "reduced motion hid the builder journey",
        )
        require(
            results["reduced_motion"]["countersFinal"],
            "reduced motion did not show final counter values",
        )
        require(
            results["reduced_motion"]["magneticDisabled"],
            "reduced motion left magnetic transforms enabled",
        )

        no_js_context = browser.new_context(
            viewport={"width": 1024, "height": 768}, java_script_enabled=False
        )
        no_js = no_js_context.new_page()
        no_js.goto(BASE_URL, wait_until="domcontentloaded")
        results["no_javascript"] = no_js.locator("[data-builder-step]").evaluate_all(
            """steps => steps.map(step => {
              const style = getComputedStyle(step);
              return { opacity: style.opacity, transform: style.transform };
            })"""
        )
        require(
            len(results["no_javascript"]) == 4
            and all(
                step == {"opacity": "1", "transform": "none"}
                for step in results["no_javascript"]
            ),
            "no-JavaScript fallback hid the builder journey",
        )
        no_js_context.close()
        mobile_context.close()
        browser.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
