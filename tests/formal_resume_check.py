"""Structural and factual checks for the formal AdventureX LaTeX resume."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "陈思翰_AdventureX_正式简历.pdf"


def main() -> None:
    assert PDF.exists(), f"formal resume is missing: {PDF}"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 2, "formal resume must contain exactly two pages"

    for page in reader.pages:
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        assert abs(width - 595.28) < 1.0, f"unexpected A4 width: {width}"
        assert abs(height - 841.89) < 1.0, f"unexpected A4 height: {height}"

    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    required = [
        "教育背景",
        "科研经历",
        "核心项目",
        "产品与团队经历",
        "专利、荣誉与项目立项",
        "技术能力",
        "3 篇 SCI 论文在投",
        "2 个真实研究项目",
        "创业团队核心成员",
        "暨南大学 AI+ 创新大赛｜三等奖",
        "暨南大学 AI+ 创新大赛｜二等奖",
        "校级创新创业项目",
        "csh.bsbsanwu.xyz",
        "国家发明专利（已授权）",
        "CN120524301B",
        "CN202511016189.8",
        "主要发明人之一",
    ]
    for phrase in required:
        assert phrase in text, f"required resume text is missing: {phrase}"

    forbidden = [
        "8.80B",
        "Token",
        "44,735",
        "产品交付与公共影响",
        "RESEARCH PRODUCT BUILDER",
        "portfolio-theta-lemon-56.vercel.app",
        "已发表 3 篇",
    ]
    for phrase in forbidden:
        assert phrase not in text, f"forbidden resume text remains: {phrase}"

    print(f"PASS: {PDF} · 2 A4 pages · {PDF.stat().st_size} bytes")


if __name__ == "__main__":
    main()
