"""Structural and factual checks for the AdventureX resume PDF."""

from __future__ import annotations

from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "陈思翰_AdventureX_个人简历.pdf"


def main() -> None:
    assert PDF.exists(), "resume PDF is missing"
    assert PDF.stat().st_size < 2_000_000, "resume PDF is too large"
    with pdfplumber.open(PDF) as document:
        assert len(document.pages) == 2, "resume must contain exactly two pages"
        for page in document.pages:
            width, height = page.width, page.height
            assert abs(width - 595.276) < 1, "page width is not A4"
            assert abs(height - 841.89) < 1, "page height is not A4"
        text = "\n".join(page.extract_text() or "" for page in document.pages)

    required = [
        "陈思翰",
        "3 篇 SCI 论文在投",
        "scrna-omics",
        "13 个领域 Skills",
        "2 个真实项目",
        "校级创新创业项目",
        "创业团队核心成员",
        "4 条公开视频",
        "三等奖 · 2025",
        "二等奖 · 2026",
        "科研 Agent / 单细胞分析平台",
    ]
    for phrase in required:
        assert phrase in text, f"required phrase is missing: {phrase}"

    forbidden = [
        "正在申报国家级",
        "已发表 3 篇",
        "GoGoWork · 独立开发",
        "入驻粤港澳",
        "校二等奖 · 2026",
    ]
    for phrase in forbidden:
        assert phrase not in text, f"forbidden stale claim found: {phrase}"

    print(f"PASS: {PDF} · 2 A4 pages · {PDF.stat().st_size} bytes")


if __name__ == "__main__":
    main()
