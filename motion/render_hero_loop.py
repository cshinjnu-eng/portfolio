"""Render the deterministic hero atlas animation to MP4 and WebM."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "motion" / "hero-loop.html"
OUTPUT_DIR = ROOT / "assets" / "brand"
FPS = 24
DURATION = 8
WIDTH = 1440
HEIGHT = 810


def render_frames(frame_dir: Path) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1)
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.evaluate("window.__renderAt(0)")
        for frame in range(FPS * DURATION):
            time_ms = (frame / FPS) * 1000
            page.evaluate("time => window.__renderAt(time)", time_ms)
            page.screenshot(path=str(frame_dir / f"frame-{frame:04d}.png"))
        browser.close()


def encode(frame_dir: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required")
    source = str(frame_dir / "frame-%04d.png")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-framerate",
            str(FPS),
            "-i",
            source,
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "22",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(OUTPUT_DIR / "hero-loop.mp4"),
        ],
        check=True,
    )
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-framerate",
            str(FPS),
            "-i",
            source,
            "-c:v",
            "libvpx-vp9",
            "-crf",
            "34",
            "-b:v",
            "0",
            "-pix_fmt",
            "yuv420p",
            str(OUTPUT_DIR / "hero-loop.webm"),
        ],
        check=True,
    )


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="portfolio-hero-frames-") as temp:
        frames = Path(temp)
        render_frames(frames)
        encode(frames)
    print(OUTPUT_DIR / "hero-loop.mp4")
    print(OUTPUT_DIR / "hero-loop.webm")
