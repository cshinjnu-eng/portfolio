"""Validate the expanded AdventureX portfolio PDF."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "陈思翰_AdventureX_个人作品集.pdf"


def main() -> None:
    assert PDF.exists(), "portfolio PDF is missing"
    assert PDF.stat().st_size < 10 * 1024 * 1024, "portfolio PDF exceeds 10 MB"

    reader = PdfReader(str(PDF))
    assert 8 <= len(reader.pages) <= 24, f"unexpected page count: {len(reader.pages)}"
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    normalized = re.sub(r"\s+", "", text)
    required = [
        "scrna-omics",
        "67,742 个细胞",
        "8 个亚群",
        "TimeBox",
        "镜子",
        "社畜小猫",
        "GoGoWork",
        "Claude 使用风险自测",
        "未来已至-生信分析新范式",
        "你会用怎样一句话来描绘你的初恋",
        "你过的这一生，真的是你自己选的吗",
        "面对用户的倾述，AI 在想些什么",
    ]
    for item in required:
        assert re.sub(r"\s+", "", item) in normalized, (
            f"portfolio PDF is missing expanded content: {item}"
        )

    print(f"PASS: {PDF} · {len(reader.pages)} pages · {PDF.stat().st_size} bytes")


if __name__ == "__main__":
    main()
