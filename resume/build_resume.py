"""Build the two-page Chinese AdventureX resume."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from resume.resume_data import (  # noqa: E402
    COLLABORATION,
    CONTACT,
    EDUCATION,
    HONORS,
    MEDIA,
    PROFILE,
    PROJECTS,
    RESEARCH,
    SCRNA_OMICS,
    SKILLS,
)

PAGE_W, PAGE_H = A4
MARGIN_X = 40
TOP = PAGE_H - 38
BOTTOM = 35

PAPER = HexColor("#FBF8F1")
INK = HexColor("#141513")
MUTED = HexColor("#68645D")
RED = HexColor("#D84432")
GREEN = HexColor("#315746")
LINE = HexColor("#D8D1C4")
PALE_RED = HexColor("#F5E4DE")

FONT_BODY = "ArialUnicode"
FONT_SERIF = "Songti"
FONT_MONO = "Mono"


def register_fonts() -> None:
    font_specs = [
        (FONT_BODY, "/System/Library/Fonts/Supplemental/Arial Unicode.ttf", None),
        (FONT_SERIF, "/System/Library/Fonts/Supplemental/Songti.ttc", 0),
        (FONT_MONO, "/System/Library/Fonts/SFNSMono.ttf", None),
    ]
    for name, path, subfont in font_specs:
        if not Path(path).exists():
            raise FileNotFoundError(f"Required local font is missing: {path}")
        font = TTFont(name, path, subfontIndex=subfont) if subfont is not None else TTFont(name, path)
        pdfmetrics.registerFont(font)


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        candidate = current + char
        if current and pdfmetrics.stringWidth(candidate, font, size) > max_width:
            lines.append(current.rstrip())
            current = char.lstrip()
        else:
            current = candidate
    if current:
        lines.append(current.rstrip())
    return lines


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    font: str = FONT_BODY,
    size: float = 8.4,
    leading: float = 13.2,
    color=MUTED,
) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def section_label(c: canvas.Canvas, label: str, title: str, y: float) -> float:
    c.setFillColor(RED)
    c.setFont(FONT_MONO, 6.5)
    c.drawString(MARGIN_X, y, label.upper())
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 15)
    c.drawString(MARGIN_X, y - 18, title)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(MARGIN_X, y - 26, PAGE_W - MARGIN_X, y - 26)
    return y - 40


def draw_cover_image(c: canvas.Canvas, image_path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(image_path) as image:
        image_w, image_h = image.size
    scale = max(w / image_w, h / image_h)
    draw_w, draw_h = image_w * scale, image_h * scale
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    c.saveState()
    path = c.beginPath()
    path.roundRect(x, y, w, h, 5)
    c.clipPath(path, stroke=0, fill=0)
    c.drawImage(ImageReader(str(image_path)), draw_x, draw_y, draw_w, draw_h, mask="auto")
    c.restoreState()


def draw_footer(c: canvas.Canvas, page_number: int) -> None:
    c.setStrokeColor(LINE)
    c.line(MARGIN_X, BOTTOM + 11, PAGE_W - MARGIN_X, BOTTOM + 11)
    c.setFillColor(MUTED)
    c.setFont(FONT_MONO, 6.2)
    c.drawString(MARGIN_X, BOTTOM, "CHEN SIHAN · ADVENTUREX · RESEARCH PRODUCT BUILDER")
    c.drawRightString(PAGE_W - MARGIN_X, BOTTOM, f"0{page_number} / 02")


def draw_header_page_one(c: canvas.Canvas) -> float:
    portrait = ROOT / "resume" / "assets" / "portrait.jpg"
    c.setFillColor(RED)
    c.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 28)
    c.drawString(MARGIN_X, TOP - 18, CONTACT["name"])
    c.setFont(FONT_BODY, 10)
    c.drawString(MARGIN_X, TOP - 38, "医学 × 生物信息学 × AI 产品")
    c.setFillColor(RED)
    c.setFont(FONT_MONO, 6.8)
    c.drawString(MARGIN_X, TOP - 55, "RESEARCH PRODUCT BUILDER / AI4S")

    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 7.4)
    contact_lines = [
        f"{CONTACT['phone']}  ·  {CONTACT['email']}",
        f"{CONTACT['github']}  ·  {CONTACT['location']}",
    ]
    for index, line in enumerate(contact_lines):
        c.drawString(MARGIN_X, TOP - 75 - index * 13, line)

    draw_cover_image(c, portrait, PAGE_W - MARGIN_X - 78, TOP - 100, 78, 100)
    c.setStrokeColor(INK)
    c.setLineWidth(1.4)
    c.line(MARGIN_X, TOP - 112, PAGE_W - MARGIN_X, TOP - 112)
    return TOP - 130


def draw_profile(c: canvas.Canvas, y: float) -> float:
    c.setFillColor(PALE_RED)
    c.roundRect(MARGIN_X, y - 53, PAGE_W - 2 * MARGIN_X, 53, 5, fill=1, stroke=0)
    c.setFillColor(RED)
    c.setFont(FONT_MONO, 6.5)
    c.drawString(MARGIN_X + 12, y - 15, "PROFILE")
    return draw_wrapped(c, PROFILE, MARGIN_X + 12, y - 31, PAGE_W - 2 * MARGIN_X - 24, size=8.2, leading=12.4, color=INK) - 14


def draw_page_one(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    y = draw_header_page_one(c)
    y = draw_profile(c, y)

    y = section_label(c, "01 / EDUCATION", "教育背景", y)
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 10.5)
    c.drawString(MARGIN_X, y, f"{EDUCATION['school']}  ·  {EDUCATION['major']}")
    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 6.8)
    c.drawRightString(PAGE_W - MARGIN_X, y, f"{EDUCATION['date']}  ·  {EDUCATION['location']}")
    y -= 27

    y = section_label(c, "02 / RESEARCH", "科研经历", y)
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 10.5)
    c.drawString(MARGIN_X, y, RESEARCH["role"])
    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 7.5)
    c.drawString(MARGIN_X, y - 14, RESEARCH["institution"])
    c.setFont(FONT_BODY, 6.8)
    c.drawRightString(PAGE_W - MARGIN_X, y, RESEARCH["date"])
    y -= 31
    for bullet in RESEARCH["bullets"]:
        c.setFillColor(RED)
        c.circle(MARGIN_X + 2.5, y + 2.5, 1.5, fill=1, stroke=0)
        y = draw_wrapped(c, bullet, MARGIN_X + 12, y + 6, PAGE_W - 2 * MARGIN_X - 12, size=7.9, leading=11.5, color=INK) - 4

    y = section_label(c, "03 / SIGNATURE CROSSOVER", "核心项目", y - 2)
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 12)
    c.drawString(MARGIN_X, y, SCRNA_OMICS["title"])
    c.setFillColor(RED)
    c.setFont(FONT_BODY, 6.5)
    c.drawRightString(PAGE_W - MARGIN_X, y, SCRNA_OMICS["date"])
    y = draw_wrapped(c, SCRNA_OMICS["summary"], MARGIN_X, y - 18, PAGE_W - 2 * MARGIN_X, size=7.9, leading=11.8, color=INK) - 3
    c.setFillColor(MUTED)
    c.setFont(FONT_MONO, 5.9)
    c.drawString(MARGIN_X, y, SCRNA_OMICS["links"])
    y -= 26

    c.setFillColor(INK)
    c.roundRect(MARGIN_X, y - 63, PAGE_W - 2 * MARGIN_X, 63, 5, fill=1, stroke=0)
    metric_width = (PAGE_W - 2 * MARGIN_X) / 4
    metrics = [("13", "SKILLS"), ("6", "AGENTS"), ("12", "HOOKS"), ("2", "REAL ANALYSES")]
    for index, (value, label) in enumerate(metrics):
        metric_x = MARGIN_X + index * metric_width
        if index:
            c.setStrokeColor(HexColor("#41413C"))
            c.line(metric_x, y - 52, metric_x, y - 11)
        c.setFillColor(RED)
        c.setFont(FONT_MONO, 15)
        c.drawString(metric_x + 12, y - 25, value)
        c.setFillColor(HexColor("#B9B5AC"))
        c.setFont(FONT_MONO, 5.5)
        c.drawString(metric_x + 12, y - 43, label)
    y -= 82

    c.setFillColor(RED)
    c.setFont(FONT_MONO, 6.2)
    c.drawString(MARGIN_X, y, "RESEARCH TOOLKIT")
    c.setFillColor(INK)
    c.setFont(FONT_BODY, 7.5)
    c.drawString(
        MARGIN_X + 92,
        y,
        "R / Python · Seurat / Scanpy · scRNA-seq / scTCR-seq · 细胞通讯 · 轨迹推断 · Linux",
    )
    draw_footer(c, 1)


def draw_header_page_two(c: canvas.Canvas) -> float:
    c.setFillColor(GREEN)
    c.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 24)
    c.drawString(MARGIN_X, TOP - 18, "产品交付与公共影响")
    c.setFillColor(RED)
    c.setFont(FONT_MONO, 6.8)
    c.drawString(MARGIN_X, TOP - 38, "PRODUCT / VENTURE / MEDIA / COMMUNITY")

    slot_x = PAGE_W - MARGIN_X - 72
    slot_y = TOP - 76
    c.setStrokeColor(MUTED)
    c.setDash(3, 2)
    c.roundRect(slot_x, slot_y, 72, 72, 4, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 7)
    c.drawCentredString(slot_x + 36, slot_y + 39, "个人网站二维码")
    c.setFont(FONT_MONO, 5.5)
    c.drawCentredString(slot_x + 36, slot_y + 26, "FINAL URL PENDING")
    c.setStrokeColor(INK)
    c.setLineWidth(1.4)
    c.line(MARGIN_X, TOP - 92, PAGE_W - MARGIN_X, TOP - 92)
    return TOP - 110


def draw_project(c: canvas.Canvas, project: dict[str, str], y: float) -> float:
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 10.5)
    c.drawString(MARGIN_X, y, project["title"])
    c.setFillColor(RED)
    c.setFont(FONT_BODY, 6.2)
    c.drawString(MARGIN_X + 78, y, project["tag"])
    c.setFillColor(MUTED)
    c.setFont(FONT_BODY, 6.2)
    c.drawRightString(PAGE_W - MARGIN_X, y, project["date"])
    y = draw_wrapped(c, project["summary"], MARGIN_X, y - 14, PAGE_W - 2 * MARGIN_X, size=7.7, leading=11.2, color=MUTED)
    c.setStrokeColor(LINE)
    c.line(MARGIN_X, y - 3, PAGE_W - MARGIN_X, y - 3)
    return y - 14


def draw_page_two(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    y = draw_header_page_two(c)

    y = section_label(c, "04 / SELECTED PRODUCTS", "产品经历", y)
    for project in PROJECTS:
        y = draw_project(c, project, y)

    y = section_label(c, "05 / MEDIA + COMMUNITY", "内容与社群", y + 2)
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 10.5)
    c.drawString(MARGIN_X, y, MEDIA["account"])
    y = draw_wrapped(c, MEDIA["summary"], MARGIN_X, y - 15, PAGE_W - 2 * MARGIN_X, size=7.7, leading=11.2, color=MUTED)
    c.setFillColor(RED)
    c.setFont(FONT_BODY, 6.2)
    c.drawString(MARGIN_X, y - 1, "  ·  ".join(MEDIA["facts"]))
    y -= 23

    y = section_label(c, "06 / SKILL MAP", "能力结构", y)
    for label, detail in SKILLS:
        c.setFillColor(RED)
        c.setFont(FONT_BODY, 6.5)
        c.drawString(MARGIN_X, y, label.upper())
        c.setFillColor(INK)
        c.setFont(FONT_BODY, 7.8)
        c.drawString(MARGIN_X + 58, y, detail)
        y -= 16
    y -= 5

    y = section_label(c, "07 / OPEN SOURCE", "研究与开源", y)
    open_source = [
        ("scAIreport", "结构化单细胞结果复核"),
        ("γδT cells in psoriasis", "67,742 个细胞 · 8 个亚群 · 完整分析链"),
        ("Claude 风险自测", "独立调查转化为公众可用的数据产品"),
        ("Paper4AI", "面向模型的结构化论文阅读工具"),
    ]
    for title, detail in open_source:
        c.setFillColor(INK)
        c.setFont(FONT_SERIF, 8.5)
        c.drawString(MARGIN_X, y, title)
        c.setFillColor(MUTED)
        c.setFont(FONT_BODY, 6.8)
        c.drawString(MARGIN_X + 155, y, detail)
        y -= 14
    y -= 4

    y = section_label(c, "08 / HONORS + COLLABORATION", "荣誉与合作", y)
    left_width = 275
    honor_y = y
    for title, result in HONORS:
        c.setFillColor(INK)
        c.setFont(FONT_BODY, 7.6)
        c.drawString(MARGIN_X, honor_y, title)
        c.setFillColor(MUTED)
        c.setFont(FONT_BODY, 6)
        c.drawRightString(MARGIN_X + left_width, honor_y, result)
        honor_y -= 15

    box_x = MARGIN_X + left_width + 24
    box_w = PAGE_W - MARGIN_X - box_x
    c.setFillColor(GREEN)
    c.roundRect(box_x, y - 58, box_w, 66, 5, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont(FONT_MONO, 6.2)
    c.drawString(box_x + 12, y - 9, "RESEARCH PRODUCT COLLABORATION")
    draw_wrapped(c, COLLABORATION, box_x + 12, y - 25, box_w - 24, size=7.4, leading=10.5, color=HexColor("#FFFFFF"))
    draw_footer(c, 2)


def build_resume(output_path: Path) -> Path:
    register_fonts()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=A4, pageCompression=1)
    c.setTitle("陈思翰 AdventureX 个人简历")
    c.setAuthor("陈思翰")
    draw_page_one(c)
    c.showPage()
    draw_page_two(c)
    c.save()
    return output_path


if __name__ == "__main__":
    target = ROOT / "output" / "pdf" / "陈思翰_AdventureX_个人简历.pdf"
    print(build_resume(target))
