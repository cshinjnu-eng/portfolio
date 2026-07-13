#!/usr/bin/env python3
"""Build the 12-page editorial AdventureX portfolio PDF."""

from __future__ import annotations

import contextlib
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "陈思翰_AdventureX_个人作品集.pdf"
URL = "http://127.0.0.1:8765/"


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
    runtime_python = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "python"
        / "bin"
        / "python3"
    )
    qr_python = str(runtime_python) if runtime_python.exists() else "python3"
    subprocess.run(
        [qr_python, str(ROOT / "scripts" / "generate_portfolio_qr.py")], check=True
    )
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
            page = browser.new_page(viewport={"width": 1120, "height": 1584})
            page.goto(f"{URL}portfolio-pdf/", wait_until="networkidle")
            page.evaluate(
                """async () => {
                  await document.fonts.ready;
                  await Promise.all([...document.images].map((image) => {
                    if (image.complete) return Promise.resolve();
                    return new Promise((resolve) => {
                      image.addEventListener('load', resolve, { once: true });
                      image.addEventListener('error', resolve, { once: true });
                    });
                  }));
                }"""
            )
            page_count = page.locator(".page").count()
            if page_count != 12:
                raise RuntimeError(
                    f"editorial source has {page_count} pages, expected 12"
                )
            overflowing = page.evaluate(
                """() => [...document.querySelectorAll('.page')]
                  .filter((node) => node.scrollHeight > node.clientHeight + 1)
                  .map((node) => node.dataset.page)"""
            )
            if overflowing:
                raise RuntimeError(f"page overflow detected: {overflowing}")
            page.emulate_media(media="print")
            page.pdf(
                path=str(OUTPUT),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
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
