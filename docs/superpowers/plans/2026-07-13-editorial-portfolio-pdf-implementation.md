# 12 页独立作品集 PDF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用独立分页源文件生成一份 12 页 A4 作品集，替换现有连续网页打印版。

**Architecture:** 新增 `portfolio-pdf/`，用 12 个固定 A4 `.page` section 承载独立构图，共享颜色、字体、页码与图注 token。`scripts/build_portfolio_pdf.py` 只打开该分页源并导出 PDF，不再展开主页 DOM；`tests/portfolio_pdf_check.py` 检查固定页数、关键事实、文本可提取和体积。

**Tech Stack:** 语义化 HTML、CSS paged media、Python、Playwright Chromium、pypdf、Poppler。

## Global Constraints

- 固定 A4 竖版 12 页，项目不得跨页硬切。
- 暖纸色、炭黑与朱红为统一色彩；scrna-omics 第 4–5 页使用黑底。
- 不使用真人头像、卡片墙、玻璃拟态、蓝紫渐变、发光按钮或装饰性仪表盘。
- TimeBox 只展示暖纸色 v2；GoGoWork 使用完整新版 PC 原型。
- PDF 文本可选择、链接可点击，最终文件小于 10 MB。
- 不修改个人网站信息架构，不覆盖用户已有未提交文件。

---

### Task 1: 锁定 PDF 验收合同

**Files:**
- Modify: `tests/portfolio_pdf_check.py`

**Interfaces:**
- Consumes: `output/pdf/陈思翰_AdventureX_个人作品集.pdf`
- Produces: 固定 12 页、关键事实与禁用内容的自动检查。

- [ ] **Step 1: 将页数检查改为固定 12 页，并加入核心证据**

```python
assert len(reader.pages) == 12, f"unexpected page count: {len(reader.pages)}"
required = [
    "跨医学、科研与产品的独立构建者",
    "scrna-omics",
    "67,742 个细胞",
    "CN120524301B",
    "镜子",
    "TimeBox",
    "社畜小猫",
    "GoGoWork",
    "小红书社群",
    "行以践智，目以鉴真",
]
forbidden = ["微信社群", "时机成熟了。我想参与其中。"]
```

- [ ] **Step 2: 运行测试并确认旧 PDF 失败**

Run: `python3 tests/portfolio_pdf_check.py`

Expected: FAIL，旧文件为 18 页。

- [ ] **Step 3: 提交验收合同**

```bash
git add tests/portfolio_pdf_check.py
git commit -m "test: lock editorial portfolio contract"
```

### Task 2: 建立分页源与全册设计系统

**Files:**
- Create: `portfolio-pdf/index.html`
- Create: `portfolio-pdf/styles.css`

**Interfaces:**
- Consumes: `assets/brand/*`、`assets/projects/*`、`assets/media/*`
- Produces: 12 个 `.page` 节点和共享的 `.folio`、`.kicker`、`.caption`、`.evidence-link` 样式。

- [ ] **Step 1: 建立 12 页语义骨架**

```html
<main class="book">
  <section class="page page-cover" data-page="01">...</section>
  <section class="page page-profile" data-page="02">...</section>
  <section class="page page-path" data-page="03">...</section>
  <section class="page page-scrna page-dark" data-page="04">...</section>
  <section class="page page-scrna-system page-dark" data-page="05">...</section>
  <section class="page page-research" data-page="06">...</section>
  <section class="page page-mirror" data-page="07">...</section>
  <section class="page page-timebox" data-page="08">...</section>
  <section class="page page-cat" data-page="09">...</section>
  <section class="page page-gogowork" data-page="10">...</section>
  <section class="page page-media" data-page="11">...</section>
  <section class="page page-contact" data-page="12">...</section>
</main>
```

- [ ] **Step 2: 锁定 A4、颜色、字体和分页规则**

```css
@page { size: A4; margin: 0; }
:root {
  --paper: #f2ede3;
  --paper-deep: #e5dccd;
  --ink: #171714;
  --muted: #69645b;
  --red: #cf3d2e;
  --line: rgba(23, 23, 20, 0.18);
}
.page {
  width: 210mm;
  height: 297mm;
  overflow: hidden;
  break-after: page;
  position: relative;
  background: var(--paper);
}
.page:last-child { break-after: auto; }
```

- [ ] **Step 3: 完成 1–3 页并浏览器截图检查**

Run: `python3 -m http.server 8765`，打开 `http://127.0.0.1:8765/portfolio-pdf/`。

Expected: 三页边界清楚；封面无真人头像；第二页是四段时间线；第三页为单一路径而非能力卡片。

### Task 3: 完成研究中心页 4–6

**Files:**
- Modify: `portfolio-pdf/index.html`
- Modify: `portfolio-pdf/styles.css`

**Interfaces:**
- Consumes: `assets/projects/scrna-hero.png`、`assets/projects/scrna-dashboard.png`、公开仓库链接。
- Produces: scrna-omics 问题页、系统页和单细胞研究证据页。

- [ ] **Step 1: 第 4 页使用一张大图解释产品问题**

页面只保留一句主判断、两段短文、一张大幅 `scrna-hero.png` 和产品链接。

- [ ] **Step 2: 第 5 页将 13/6/12/2 映射到流程**

数字必须贴近对应的分析、执行、留档和项目使用环节，不单独组成四宫格仪表盘。

- [ ] **Step 3: 第 6 页建立公开研究证据**

写明 6 个文库、67,742 个细胞、8 个亚群、主要高级分析、个人职责与公开仓库；不得写成已发表论文或 SaaS。

- [ ] **Step 4: 导出 1–6 页临时 PDF 并渲染检查**

Run: `pdftoppm -png tmp/pdfs/editorial-half.pdf tmp/pdfs/editorial-half/page`

Expected: 黑底只出现在 4–5 页；第 6 页回到纸色；图片和文字无裁切。

### Task 4: 完成项目与内容页 7–12

**Files:**
- Modify: `portfolio-pdf/index.html`
- Modify: `portfolio-pdf/styles.css`

**Interfaces:**
- Consumes: 镜子、TimeBox v2、社畜小猫、GoGoWork、小红书四条视频封面与小产品链接。
- Produces: 六个完整、页内闭合的编辑页面。

- [ ] **Step 1: 第 7 页以 degree 报告截图为主视觉**

将长截图裁成报告封面与关键段落两个视窗，附代表报告链接。

- [ ] **Step 2: 第 8 页只放 TimeBox 暖纸色 v2 双界面**

并行计时与 Hermes 两张手机图分别对应“记录”和“复盘”，不引用旧深色截图。

- [ ] **Step 3: 第 9 页编排社畜小猫界面与动作素材**

用一张手机界面和一张动作表解释状态、动作、长期记忆和主动信件。

- [ ] **Step 4: 第 10 页完整展示 GoGoWork PC 原型**

任务市场占主图，交付详情占辅助图；文字说明团队身份、个人职责和 OPC 履约路径。

- [ ] **Step 5: 第 11 页压缩四条视频与小产品索引**

四条视频封面使用统一小尺寸；社群写为“小红书社群”，微信只写同步内容；小产品每项不超过一行。

- [ ] **Step 6: 第 12 页收束合作方向、联系方式与二维码**

链接到个人网站、GitHub、邮箱和科研项目，使用“行以践智，目以鉴真”收尾。

### Task 5: 替换构建链路

**Files:**
- Modify: `scripts/build_portfolio_pdf.py`

**Interfaces:**
- Consumes: `http://127.0.0.1:8765/portfolio-pdf/`
- Produces: `output/pdf/陈思翰_AdventureX_个人作品集.pdf`

- [ ] **Step 1: 删除主页展开和素材替换逻辑**

构建脚本只启动本地服务器、打开分页源、等待字体与图片完成、模拟 print media 并导出。

- [ ] **Step 2: 设置无边距 A4 输出**

```python
page.goto(f"{URL}portfolio-pdf/", wait_until="networkidle")
page.emulate_media(media="print")
page.pdf(
    path=str(OUTPUT),
    format="A4",
    print_background=True,
    prefer_css_page_size=True,
    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
)
```

- [ ] **Step 3: 构建并运行自动检查**

Run: `python3 scripts/build_portfolio_pdf.py && python3 tests/portfolio_pdf_check.py`

Expected: PASS，12 pages，文件小于 10 MB。

### Task 6: 逐页视觉 QA 与交付

**Files:**
- Modify: `portfolio-pdf/index.html`
- Modify: `portfolio-pdf/styles.css`
- Modify: `CHECKPOINT_PORTFOLIO_PDF.md`

**Interfaces:**
- Consumes: 最终 PDF 的 12 张页面渲染图。
- Produces: 通过视觉检查的最终作品集和完成的 checkpoint。

- [ ] **Step 1: 以 144 DPI 渲染全部页面**

Run: `rm -rf tmp/pdfs/editorial && mkdir -p tmp/pdfs/editorial && pdftoppm -png -r 144 output/pdf/陈思翰_AdventureX_个人作品集.pdf tmp/pdfs/editorial/page`

- [ ] **Step 2: 生成 12 页 contact sheet 并逐页检查**

检查裁切、溢出、孤行、低清图片、重复构图、异常空白、错误版本截图和文字过密；发现问题后修改源文件并重新构建。

- [ ] **Step 3: 运行最终验证**

Run: `python3 tests/portfolio_pdf_check.py && pdfinfo output/pdf/陈思翰_AdventureX_个人作品集.pdf && git diff --check`

Expected: 12 页 A4、体积小于 10 MB、文本与事实检查通过、无空白错误。

- [ ] **Step 4: 更新 checkpoint 并提交**

```bash
git add portfolio-pdf scripts/build_portfolio_pdf.py tests/portfolio_pdf_check.py output/pdf/陈思翰_AdventureX_个人作品集.pdf CHECKPOINT_PORTFOLIO_PDF.md
git commit -m "feat: rebuild portfolio as 12-page editorial PDF"
```

