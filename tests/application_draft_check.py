"""Content, character-limit, and factual checks for the AdventureX draft."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "output" / "application" / "AdventureX_2026_报名填写稿.md"


def main() -> None:
    assert DRAFT.exists(), "AdventureX application draft is missing"
    text = DRAFT.read_text(encoding="utf-8")

    required_sections = [
        "第一页：基本信息",
        "请用一段话做一个自我介绍",
        "请说明你掌握或者正在学习的技术或能力",
        "请描述一个最近让你感到兴奋的 Idea",
        "你的其他过往活动／项目／奖项／实习列表",
        "你为什么选择参与 AdventureX 2026",
        "请告诉我们你对 AdventureX 2026 的期望",
        "自我认知、价值观与愿景",
        "逻辑思维、团队协作与黑客精神",
        "想象力、哲学与生命观",
        "第四页：最后确认",
    ]
    for section in required_sections:
        assert section in text, f"application section is missing: {section}"

    answer_pattern = re.compile(
        r"```text\n(?P<answer>.*?)\n```\n\n字符数：(?P<count>\d+)／(?P<limit>[^。\n]+)",
        re.DOTALL,
    )
    answers = list(answer_pattern.finditer(text))
    assert len(answers) >= 20, "too few copy-ready application answers"
    copy_text = "\n".join(match.group("answer") for match in answers)

    limited_answers = 0
    for match in answers:
        answer = match.group("answer")
        stated_count = int(match.group("count"))
        assert len(answer) == stated_count, (
            f"stale character count: stated {stated_count}, actual {len(answer)} "
            f"for {answer[:24]!r}"
        )
        limit_text = match.group("limit")
        if limit_text.isdigit():
            limited_answers += 1
            limit = int(limit_text)
            assert len(answer) <= limit * 0.9, (
                f"answer leaves less than 10% spare capacity: {answer[:24]!r}"
            )

    assert limited_answers == 9, "expected nine form-limited responses"
    assert text.count("简历中的二维码指向同一个最终网址") == 1

    required_facts = [
        "3 篇 SCI 论文在投",
        "校级创新创业项目",
        "创业团队核心成员",
        "2025 年三等奖、2026 年二等奖",
        "https://portfolio-theta-lemon-56.vercel.app/",
        "不上传未公开研究数据",
    ]
    for fact in required_facts:
        assert fact in text, f"required application fact is missing: {fact}"

    forbidden = [
        "example.com",
        "已发表 3 篇",
        "GoGoWork｜2026—至今｜独立",
        "发明专利 1 项｜主要发明人",
    ]
    for phrase in forbidden:
        assert phrase not in copy_text, (
            f"stale or unsupported content remains in a copy-ready answer: {phrase}"
        )

    print(
        f"PASS: {DRAFT} · {len(answers)} copy-ready answers · "
        f"{limited_answers} limited responses"
    )


if __name__ == "__main__":
    main()
