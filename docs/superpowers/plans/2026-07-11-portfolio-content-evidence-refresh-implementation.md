# Portfolio Content and Evidence Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace awkward personal and project evidence, humanize all visible Chinese copy, expand small-project descriptions, regenerate the resume, and publish the verified result.

**Architecture:** Keep the static-site information architecture and modular CSS/JS intact. Replace media assets in `assets/`, revise visible copy in the HTML/data/resume sources, extend the existing research index rather than introducing a new card system, then rebuild and test the PDF and site.

**Tech Stack:** Static HTML/CSS/JavaScript, Image-2, Python/ReportLab, Playwright, Git/GitHub CLI.

## Global Constraints

- Preserve the approved Direction A visual system and existing Hero motion.
- Do not use the user's portrait anywhere on the website; the formal resume keeps it.
- TimeBox evidence must come from the warm-paper v2 worktree and contain no private user data or code.
- GoGoWork remains identified as a team project; prototype numbers are not business metrics.
- Chinese copy must follow `humanizer-zh` and retain all factual guardrails.

---

### Task 1: Replace project and personal media

**Files:**
- Create: `assets/brand/builder-silhouette.webp`
- Replace: `assets/projects/timebox-beige.png`, `assets/projects/timebox-hermes.jpg`, `assets/projects/timebox-radar.jpg`
- Replace: `assets/projects/gogowork-demo.png`, `assets/projects/gogowork-workflow.png`

- [ ] Generate and visually inspect the non-identifiable research-builder silhouette.
- [ ] Run the TimeBox v2 worktree and capture warm-paper growth and AI views using development-only data.
- [ ] Render the GoGoWork PC prototype and capture marketplace plus delivery/matching views.
- [ ] Optimize final assets and verify dimensions and file sizes.

### Task 2: Humanize website copy and update the layouts

**Files:**
- Modify: `index.html`
- Modify: `data/projects.js`
- Modify: `styles/story.css`, `styles/projects.css`, `styles/responsive.css`
- Modify: `design-board/index.html`

- [ ] Remove the portrait and rejected phrase, add the silhouette and the story signature.
- [ ] Rewrite all visible Chinese copy with concrete first-person statements and factual results.
- [ ] Replace TimeBox and GoGoWork compositions with the new evidence assets.
- [ ] Expand the research/open-source index to eight concise rows with type, role/output, and link.
- [ ] Check the active design board for stale rejected public-facing copy.

### Task 3: Humanize and regenerate the resume

**Files:**
- Modify: `resume/resume_data.py`
- Modify if required: `resume/build_resume.py`
- Replace: `output/pdf/陈思翰_AdventureX_个人简历.pdf`

- [ ] Rewrite summary, research, product, media, skill, and collaboration copy without changing claims.
- [ ] Rebuild the PDF and verify exactly two A4 pages with selectable Chinese text.
- [ ] Run the factual guardrail test.

### Task 4: Cross-device verification and publication

**Files:**
- Modify if coverage requires: `tests/portfolio-smoke.py`, `tests/resume_pdf_check.py`
- Update: `CHECKPOINT.md`

- [ ] Add assertions for removed portrait/rejected copy and the eight-item small-product index.
- [ ] Run JavaScript syntax, formatting check, site smoke tests, and PDF tests.
- [ ] Visually inspect 1440px and 390px renders, including expanded TimeBox and GoGoWork panels.
- [ ] Commit the implementation, push `main` to `origin`, and verify the remote commit.
