# Media Output and Resume Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight, verifiable four-video content archive to the media section and correct the two AI+ awards across the website and two-page resume.

**Architecture:** Use native HTML disclosure for the archive, local compressed cover images, and stable public XiaoHongShu note URLs. Keep the resume data-driven and extend existing tests to assert the verified IDs, snapshot facts, and both awards.

**Tech Stack:** Static HTML/CSS, native `<details>`, ImageMagick/cwebp-compatible asset optimization, Python/ReportLab, Playwright, pdfplumber.

## Global Constraints

- Do not save cookies, xsec tokens, raw platform responses, or private note data in the repository.
- Store only compressed public cover images; do not copy the four video files into the repository.
- Treat account statistics as a dated 2026-07 snapshot.
- Preserve two A4 resume pages and existing factual guardrails.
- Do not add JavaScript state for the disclosure.

---

### Task 1: Localize verified public covers

**Files:**
- Create: `assets/media/xhs-scrna.webp`
- Create: `assets/media/xhs-first-love.webp`
- Create: `assets/media/xhs-destiny.webp`
- Create: `assets/media/xhs-llm-story.webp`

- [ ] Download the four public cover images from the current read-only audit results.
- [ ] Convert each to WebP, cap the longest edge at 1200px, and visually inspect the output.

### Task 2: Add the disclosure archive and snapshot

**Files:**
- Modify: `index.html`
- Modify: `styles/projects.css`
- Modify: `styles/responsive.css`

- [ ] Update the media metrics to the dated audit snapshot without presenting it as a permanent baseline.
- [ ] Add one native disclosure with four linked video entries and stable `/explore/<note-id>` URLs.
- [ ] Style two desktop columns and one mobile column using dividers rather than nested cards.

### Task 3: Correct resume and honor evidence

**Files:**
- Modify: `resume/resume_data.py`
- Modify if required for fit: `resume/build_resume.py`
- Replace: `output/pdf/陈思翰_AdventureX_个人简历.pdf`

- [ ] Add the 24-public-note / four-video content evidence and a concise production capability statement.
- [ ] Split the AI+ award into 2025 third prize and 2026 second prize in both website and resume.
- [ ] Rebuild and visually verify exactly two A4 pages.

### Task 4: Validate and publish

**Files:**
- Modify: `tests/portfolio-smoke.py`
- Modify: `tests/resume_pdf_check.py`
- Update: `CHECKPOINT.md`

- [ ] Assert exactly four video entries, the verified note IDs, native disclosure behavior, and both awards.
- [ ] Run formatting, JavaScript syntax, desktop/mobile/reduced-motion smoke checks, and PDF checks.
- [ ] Commit only implementation-owned files, push `main`, and verify the remote commit.
