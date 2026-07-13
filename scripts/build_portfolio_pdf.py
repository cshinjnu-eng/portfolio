#!/usr/bin/env python3
"""Build the fully expanded AdventureX portfolio PDF."""

from __future__ import annotations

import contextlib
import json
import shutil
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "陈思翰_AdventureX_个人作品集.pdf"
URL = "http://127.0.0.1:8765/"


def prepare_print_assets() -> dict[str, str]:
    """Create smaller JPEG copies without touching website source assets."""
    target_root = ROOT / "tmp" / "pdfs" / "portfolio-assets"
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True)

    replacements: dict[str, str] = {}
    for source in (ROOT / "assets").rglob("*"):
        if source.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        if source.stat().st_size < 120_000:
            continue
        relative = source.relative_to(ROOT)
        target = target_root / relative.with_suffix(".jpg")
        target.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                "sips",
                "-Z",
                "1500",
                "-s",
                "format",
                "jpeg",
                "-s",
                "formatOptions",
                "68",
                str(source),
                "--out",
                str(target),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and target.exists():
            replacements[relative.as_posix()] = target.relative_to(ROOT).as_posix()
    return replacements


def wait_for_server() -> None:
    for _ in range(50):
        try:
            with urlopen(URL, timeout=0.3) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("local portfolio server did not start")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    print_assets = prepare_print_assets()
    server = subprocess.Popen(
        ["python3", "-m", "http.server", "8765", "--bind", "127.0.0.1"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_for_server()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome")
            page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.goto(URL, wait_until="networkidle")
            page.evaluate(
                """(printAssets) => {
                  document.querySelectorAll('details').forEach((node) => {
                    node.open = true;
                  });
                  document.querySelectorAll('.project-panel').forEach((node) => {
                    node.hidden = false;
                  });
                  document.querySelectorAll('.project-item').forEach((node) => {
                    node.classList.add('is-open');
                  });
                  document.querySelectorAll('.project-trigger').forEach((node) => {
                    node.setAttribute('aria-expanded', 'true');
                  });
                  document.querySelectorAll('img').forEach((image) => {
                    image.loading = 'eager';
                    const source = image.getAttribute('src');
                    if (printAssets[source]) image.src = printAssets[source];
                  });
                  document.documentElement.dataset.pdfExport = 'expanded';
                }""",
                json.loads(json.dumps(print_assets)),
            )
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1800)
            page.evaluate("window.scrollTo(0, 0)")
            page.emulate_media(media="print")
            page.pdf(
                path=str(OUTPUT),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
            )
            browser.close()
    finally:
        server.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            server.wait(timeout=3)
        if server.poll() is None:
            server.kill()

    size = OUTPUT.stat().st_size
    if size >= 10 * 1024 * 1024:
        raise RuntimeError(f"portfolio PDF exceeds 10 MB: {size} bytes")
    print(f"Built {OUTPUT} ({size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
