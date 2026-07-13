# Formal LaTeX Resume Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use the installed `latex-document-skill` and execute inline with PDF visual QA.

**Goal:** Build and verify a formal two-page Chinese LaTeX resume for AdventureX 2026.

**Architecture:** Create a standalone single-column LaTeX source, compile it with the local Tectonic engine, and validate both extracted text and rendered pages. Preserve the existing ReportLab resume as a separate legacy artifact.

**Tech Stack:** LaTeX, Tectonic, Poppler, Python PDF assertions.

## Global Constraints

- Exactly two A4 pages.
- White background, black/gray text, one dark-blue accent.
- Standard resume headings and linear reading order.
- Photo and QR are optional visual aids; all contact information must also exist as text.
- No Token metrics, dashboard blocks, marketing section names, or unsupported claims.

---

### Task 1: Add formal-resume assertions

**Files:**
- Create: `tests/formal_resume_check.py`

- [x] Check that the target PDF exists and is exactly two A4 pages.
- [x] Extract text and assert required sections and factual guardrails.
- [x] Reject Token metrics, promotional headings, and stale website URLs.

### Task 2: Build the LaTeX source

**Files:**
- Create: `resume/latex/chen_sihan_adventurex_resume.tex`

- [x] Implement the single-column two-page layout.
- [x] Add education, research, scrna-omics, selected products, team experience, media, honors, skills, photo, and QR.
- [x] Compile with `tectonic` to the stable output filename.

### Task 3: Render and refine

**Files:**
- Verify: `output/pdf/陈思翰_AdventureX_正式简历.pdf`
- Render: `tmp/pdfs/formal-resume/`

- [x] Render both pages to PNG and inspect at full resolution.
- [x] Fix overflow, spacing, hierarchy, and weak content density.
- [x] Run the PDF assertions and LaTeX log checks.
- [x] Commit the source, test, and PDF; push `main`.
