# AdventureX Application and Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen the portfolio's visible interaction and builder narrative, then produce a complete, evidence-checked AdventureX 2026 application draft and synchronized two-page resume.

**Architecture:** Keep the current static HTML/CSS/JavaScript system. Add one focused builder-journey section and one focused interaction module that handles counters, magnetic controls, pointer depth, and scroll state while respecting reduced motion. Keep the application draft as a private local Markdown deliverable ordered exactly like the form; reuse verified portfolio facts instead of introducing a second data system.

**Tech Stack:** Semantic HTML, modular CSS, vanilla JavaScript, IntersectionObserver, requestAnimationFrame, Playwright smoke tests, ReportLab resume builder, PyPDF validation.

## Global Constraints

- Keep the static site architecture; do not migrate to React or add runtime dependencies.
- Use `humanizer-zh` on all new public Chinese copy and application responses.
- Preserve factual boundaries: three SCI manuscripts are under review, research establishment is school-level, GoGoWork is a team project, and future activities remain planned.
- Display only `近 30 天`, `8 个模型`, and `5B+ 上下文处理量`; explain that this is a local workflow-processing record, not product impact.
- Do not publish raw logs, provider names, cost, cookies, private sessions, or personal identifiers.
- Keep all primary content readable without JavaScript and fully static under reduced motion.
- Do not auto-fill or submit the AdventureX application.

---

### Task 1: Lock the interaction contract with smoke tests

**Files:**

- Modify: `tests/portfolio-smoke.py`
- Modify: `tests/resume_pdf_check.py`

**Interfaces:**

- Consumes: current homepage at `http://127.0.0.1:8765/`.
- Produces: assertions for `[data-builder-journey]`, four journey steps, three evidence counters, magnetic CTA behavior hooks, and reduced-motion final states.

- [ ] Add failing homepage assertions for one builder journey, four `[data-builder-step]` nodes, `[data-count-value]` values `30`, `8`, and `5`, the visible `5B+` label, and the workflow-record disclaimer.
- [ ] Add a desktop pointer interaction assertion that verifies a magnetic element receives a non-zero CSS transform after pointer movement and resets after pointer leave.
- [ ] Add a scroll assertion that at least one builder step becomes `.is-active` and all counters reach their final accessible text.
- [ ] Add reduced-motion assertions that the journey is readable, the hero video remains unloaded, counters show final values immediately, and magnetic transforms remain disabled.
- [ ] Run `python3 -m http.server 8765` plus `.venv/bin/python tests/portfolio-smoke.py`; expect failure because the new journey and hooks do not exist.

### Task 2: Add the Builder in Motion narrative

**Files:**

- Modify: `index.html`
- Create: `styles/builder-motion.css`
- Modify: `styles/responsive.css`

**Interfaces:**

- Consumes: existing design tokens from `styles/tokens.css` and section conventions from `styles/story.css`.
- Produces: semantic `[data-builder-journey]`, `[data-builder-step]`, `[data-count-value]`, and `[data-magnetic]` markup consumed by Task 3.

- [ ] Link `styles/builder-motion.css` after `styles/hero.css` so it can extend, not override, base tokens.
- [ ] Insert a semantic journey between the hero and the proof strip with four stages: `问题`, `实验`, `系统`, `产品`; each stage includes one concrete sentence and a compact evidence label.
- [ ] Add a three-part evidence rail showing `近 30 天`, `8 个模型`, and `5B+ 上下文处理量`, followed by the exact qualifier `本地工具记录的 Claude Code 与 Codex 工作流处理量，用于说明构建密度，不等同于产品成果。`
- [ ] Add `data-magnetic` to the two hero actions and mark the journey path/progress elements for progressive enhancement.
- [ ] Style the journey as one continuous asymmetrical path rather than four cards; use paper, ink, warm red, thin rules, large stage numerals, and staggered alignment.
- [ ] Add 1024 px and 390 px rules that turn the path vertical, prevent metric crowding, and keep all text left aligned.
- [ ] Add reduced-motion CSS that removes transitions, transforms, pulses, and animated path drawing while preserving final visibility.
- [ ] Run Prettier on the changed HTML/CSS and verify `git diff --check` passes.

### Task 3: Implement purposeful motion and interaction

**Files:**

- Modify: `scripts/hero-motion.js`
- Create: `scripts/builder-motion.js`
- Modify: `scripts/scroll-story.js`
- Modify: `app.js`

**Interfaces:**

- Consumes: Task 2 data attributes.
- Produces: `window.initBuilderMotion(scope): () => void` and enhanced `window.initHeroMotion(root): () => void` cleanup-safe modules.

- [ ] Increase hero pointer depth ranges while clamping values and add separate title drift variables so text and background move in opposite, subtle directions.
- [ ] Add a one-shot `.is-pulsed` state after hero readiness and remove it after the CSS animation finishes.
- [ ] Implement `initBuilderMotion` with one IntersectionObserver for active steps and one observer for evidence counters.
- [ ] Implement counters that animate from zero to their final integer and render suffixes through markup; under reduced motion, set the final values synchronously.
- [ ] Implement magnetic pointer movement using requestAnimationFrame, element-local coordinates, and maximum 10 px translation; reset on pointer leave and disable for coarse pointers/reduced motion.
- [ ] Update journey progress from its bounding rectangle during scroll, sharing the existing requestAnimationFrame discipline rather than creating continuous animation loops.
- [ ] Initialize the new module from `app.js` and return cleanup callbacks following current conventions.
- [ ] Run `node --check app.js scripts/*.js data/*.js` and rerun the portfolio smoke test; expect all new interaction assertions to pass.

### Task 4: Draft every AdventureX application field

**Files:**

- Create: `output/application/AdventureX_2026_报名填写稿.md`
- Reference only: `docs/handoff/简历补充信息与证据目录.md`
- Reference only: `docs/insights/小红书账号只读审计-2026-07.md`
- Reference only: the four supplied application screenshots

**Interfaces:**

- Consumes: verified identity, project, award, media, and CC-Switch facts.
- Produces: one copy-ready Markdown document with a fact note and character count under every editable response.

- [ ] Create sections matching the form order: basic information, skill category, self-introduction, capability description, recent Idea, activities/projects/awards, links, reason for joining, expectations, three selected short answers, optional free response, attachments, and final declarations.
- [ ] Rewrite the skill field so it names life science research, bioinformatics, AI workflow design, full-stack delivery, and product research without claiming unsupported seniority.
- [ ] Write a self-introduction that establishes oral-medicine training, immunology/bioinformatics work, the research-to-product transition, and collaboration value within 1000 Chinese characters.
- [ ] Use `scrna-omics` as the recent exciting Idea, explaining the concrete single-cell workflow gap, existing two-project validation, and the next product question within 1000 characters.
- [ ] Structure project/award entries with role and status: four primary projects, two AI+ awards, school-level innovation establishment, content/community operations, and GoGoWork team work.
- [ ] Provide verified links only: portfolio, GitHub, scrna-omics site, Mirror representative report, Xiaohongshu profile, GoGoWork article, and GoGoWork demo.
- [ ] Write the reason and expectations as reciprocal collaboration: what the applicant contributes in five days, what feedback/resources would unlock, and what a successful prototype looks like.
- [ ] Write complementary short answers for the 2036 letter, underestimated Agent infrastructure trend, and an absurd useless invention; keep each under 1000 characters and avoid repeating AI4S language across all three.
- [ ] Use one concise personal sentence for the optional 200-character field.
- [ ] Run `humanizer-zh` review manually against every response: remove slogans, false contrasts, generic enthusiasm, overused triplets, and unsupported conclusions.
- [ ] Use a small local character-count command to verify every answer stays below its form limit with at least 10% spare capacity.

### Task 5: Synchronize the formal resume

**Files:**

- Modify: `resume/resume_data.py`
- Modify: `resume/build_resume.py` only if text fitting requires it
- Modify: `output/pdf/陈思翰_AdventureX_个人简历.pdf`
- Modify: `tests/resume_pdf_check.py`

**Interfaces:**

- Consumes: finalized positioning and factual claims from Task 4.
- Produces: two-page A4 selectable-text PDF with application-consistent wording.

- [ ] Replace any remaining generic capability phrases with concrete research, AI workflow, full-stack, and product actions from the application draft.
- [ ] Add a restrained builder-density fact only if it fits without displacing project evidence; label it as a local 30-day workflow record rather than impact.
- [ ] Keep the portrait in the resume, the school-level and under-review qualifiers, and the two separate AI+ award rows.
- [ ] Rebuild with `.venv/bin/python resume/build_resume.py`.
- [ ] Run `.venv/bin/python tests/resume_pdf_check.py`; expect exactly two A4 pages, selectable Chinese text, and all factual guardrails to pass.

### Task 6: Visual QA, checkpoint, and publish

**Files:**

- Modify: `CHECKPOINT.md`
- Modify: `tests/portfolio-smoke.py` only for verified test corrections

**Interfaces:**

- Consumes: completed website, application draft, and resume.
- Produces: verified screenshots, clean target diff, commit, and pushed `main`.

- [ ] Run the local HTTP server and the complete portfolio smoke test at 1440 × 1000, 1024 × 768, 390 × 844, and reduced motion.
- [ ] Capture the hero and builder journey at desktop and mobile widths; inspect hierarchy, motion state, text wrapping, and absence of horizontal overflow.
- [ ] Verify keyboard focus, project expansion, media archive expansion, video lazy loading, and magnetic controls that do not interfere with clicking.
- [ ] Run `prettier --check index.html styles/*.css docs/superpowers/**/*.md`, `node --check` for all JavaScript, both Python checks, and `git diff --check` excluding the binary PDF.
- [ ] Update `CHECKPOINT.md` with the verified motion, application, resume, and responsive outcomes.
- [ ] Stage only scoped implementation files; keep `CHECKPOINT_INSIGHT.md`, `docs/content-packages/`, `docs/handoff/`, and `docs/insights/` untracked unless they were already tracked.
- [ ] Commit with `feat: strengthen AdventureX builder story` and push `main` after confirming it is ahead of, not divergent from, `origin/main`.
