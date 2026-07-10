# AdventureX Resume Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Execute inline after the portfolio content contract is stable. Do not dispatch subagents.

**Goal:** Produce a formal, text-selectable, two-page Chinese A4 resume aligned with the AdventureX portfolio and optimized for research-product collaboration.

**Architecture:** Generate the resume from structured Python data into PDF using ReportLab with embedded CJK fonts. Keep content, layout, portrait processing, and PDF verification separate so factual changes do not require manual page editing.

**Tech Stack:** Python, ReportLab, Pillow, qrcode, Poppler, pdfplumber, Prettier for supporting Markdown.

## Global Constraints

- Follow `docs/superpowers/specs/2026-07-10-adventurex-resume-design.md`.
- Output exactly two A4 pages in Chinese.
- Keep text selectable and extraction order sensible.
- Use the supplied real portrait, not an AI-generated face.
- Reserve a website QR slot until the final public URL is confirmed.
- Preserve every factual guardrail from `DESIGN.md`.

---

### Task 1: Create Resume Content Source and Portrait Asset

**Files:**

- Create: `resume/resume_data.py`
- Create: `resume/assets/portrait.jpg`
- Create: `resume/assets/website-qr-placeholder.png`

**Interfaces:**

- Produces: `PROFILE`, `RESEARCH`, `PROJECTS`, `SKILLS`, `HONORS`, `CONTACT`, and `MEDIA` constants consumed by the PDF builder.

- [ ] **Step 1: Build the factual content source**

  Encode dates, roles, claims, URLs, and wording once in `resume_data.py`. Add comments only where a claim still needs the user's exact formal title.

- [ ] **Step 2: Crop and normalize the portrait**

  Create a neutral head-and-shoulders crop with no generative modification.

- [ ] **Step 3: Create a labeled QR placeholder**

  Use a deterministic placeholder that cannot be mistaken for a functional QR code.

- [ ] **Step 4: Validate the data source**

  Run:

  ```bash
  python3 -m py_compile resume/resume_data.py
  ```

  Expected: syntax passes.

### Task 2: Build the Two-page PDF Generator

**Files:**

- Create: `resume/build_resume.py`
- Create: `output/pdf/陈思翰_AdventureX_个人简历.pdf`

**Interfaces:**

- `build_resume(output_path: Path) -> Path`
- Consumes: constants from `resume.resume_data` and resume assets.

- [ ] **Step 1: Register embedded Chinese and Latin fonts**

  Use locally available OTF/TTF fonts and fail with a clear message if they cannot be found.

- [ ] **Step 2: Implement reusable layout primitives**

  Create functions for section headers, dated entries, project rows, metric strips, skill rows, and page footer.

- [ ] **Step 3: Build page one**

  Render header and portrait, profile, education, research experience, outputs, `scrna-omics`, and primary honors.

- [ ] **Step 4: Build page two**

  Render products, entrepreneurship, media/community, skill hierarchy, compact honors, collaboration CTA, and QR placeholder.

- [ ] **Step 5: Generate the PDF**

  Run:

  ```bash
  python3 resume/build_resume.py
  ```

  Expected: the stable output PDF exists under `output/pdf/`.

### Task 3: Render and Verify the Resume

**Files:**

- Create: `tmp/pdfs/adventurex-resume/page-1.png`
- Create: `tmp/pdfs/adventurex-resume/page-2.png`
- Create: `tests/resume_pdf_check.py`

**Interfaces:**

- Produces: rendered inspection pages and automated page/text checks.

- [ ] **Step 1: Render both pages**

  Run:

  ```bash
  mkdir -p tmp/pdfs/adventurex-resume
  pdftoppm -png -r 160 output/pdf/陈思翰_AdventureX_个人简历.pdf tmp/pdfs/adventurex-resume/page
  ```

  Expected: exactly two PNG files.

- [ ] **Step 2: Check page count and text extraction**

  Verify two A4 pages, contact details, `scrna-omics`, three manuscripts under review, school-level project wording, and no stale national-level claim.

- [ ] **Step 3: Visually inspect both pages**

  Confirm portrait crop, embedded glyphs, baseline alignment, no clipping, printable contrast, and a clearly labeled nonfunctional QR placeholder.

- [ ] **Step 4: Run final PDF checks**

  Run:

  ```bash
  python3 tests/resume_pdf_check.py
  pdfinfo output/pdf/陈思翰_AdventureX_个人简历.pdf
  ```

  Expected: two A4 pages, selectable Chinese text, and all factual assertions pass.
