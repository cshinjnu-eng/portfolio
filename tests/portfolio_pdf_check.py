"""Validate the 12-page editorial AdventureX portfolio PDF."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "陈思翰_AdventureX_个人作品集.pdf"


def main() -> None:
    assert PDF.exists(), "portfolio PDF is missing"
    assert PDF.stat().st_size < 10 * 1024 * 1024, "portfolio PDF exceeds 10 MB"

    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 12, f"unexpected page count: {len(reader.pages)}"
    assert reader.metadata.title == "陈思翰｜跨医学、科研与产品的独立构建者"
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    normalized = re.sub(r"\s+", "", unicodedata.normalize("NFKC", text))
    required = [
        "跨医学、科研与产品的独立构建者",
        "scrna-omics",
        "67,742 个细胞",
        "8 个亚群",
        "CN120524301B",
        "TimeBox",
        "镜子",
        "社畜小猫",
        "GoGoWork",
        "小红书社群",
        "行以践智，目以鉴真",
        "未来已至-生信分析新范式",
        "你会用怎样一句话来描绘你的初恋",
        "你过的这一生，真的是你自己选的吗",
        "面对用户的倾述，AI 在想些什么",
    ]
    for item in required:
        assert re.sub(r"\s+", "", unicodedata.normalize("NFKC", item)) in normalized, (
            f"portfolio PDF is missing expanded content: {item}"
        )

    forbidden = ["微信社群", "时机成熟了。我想参与其中。"]
    for item in forbidden:
        assert (
            re.sub(r"\s+", "", unicodedata.normalize("NFKC", item)) not in normalized
        ), f"portfolio PDF contains forbidden wording: {item}"

    link_count = sum(len(page.get("/Annots") or []) for page in reader.pages)
    assert link_count >= 25, f"too few clickable links: {link_count}"

    print(f"PASS: {PDF} · {len(reader.pages)} pages · {PDF.stat().st_size} bytes")


if __name__ == "__main__":
    main()
