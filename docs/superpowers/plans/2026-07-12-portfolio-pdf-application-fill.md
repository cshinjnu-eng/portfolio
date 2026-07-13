# Portfolio PDF and Application Fill Implementation Plan

> **For agentic workers:** Use browser control for the signed-in form, Playwright for local print/PDF QA, and the PDF skill for rendered-page inspection.

**Goal:** Add public single-cell evidence, default-open videos, a fully expanded portfolio PDF, and a safely filled but unsubmitted AdventureX form.

**Architecture:** Keep screen interactions intact while adding evidence to existing sections and a dedicated print stylesheet that forces all expandable content open. Generate and validate the PDF locally before browser upload, then append or fill form fields without submitting.

**Tech Stack:** HTML, CSS, JavaScript, Playwright, Chromium PDF, Python/PDF inspection, browser control.

## Tasks

### 1. Evidence and default-open media

- [ ] Update smoke assertions first.
- [ ] Add the public repository to scrna-omics and the research index.
- [ ] Make the four-video archive open by default.
- [ ] Update the AdventureX Markdown draft and character counts.

### 2. Print-safe expanded portfolio

- [ ] Add `styles/print.css` and link it from `index.html`.
- [ ] Force all project panels and details content visible in print.
- [ ] Add a deterministic PDF build script and PDF content checks.
- [ ] Render every page and inspect visual continuity.

### 3. Browser form fill

- [ ] Connect to the signed-in browser and inspect the current form state.
- [ ] Append comparison versions to populated long fields within limits.
- [ ] Fill empty selected short answers and relevant links.
- [ ] Upload the formal resume and expanded portfolio PDF.
- [ ] Stop before submission and capture a final state summary.

### 4. Final validation and delivery

- [ ] Run website, application, and PDF checks.
- [ ] Commit and push repository changes.
- [ ] Report browser fill status without submitting.
