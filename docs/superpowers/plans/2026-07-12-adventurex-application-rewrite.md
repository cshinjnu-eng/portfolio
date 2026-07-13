# AdventureX Application Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Execute this plan task-by-task in the current session. Do not delegate because the task is a single tightly coupled editorial pass.

**Goal:** Rewrite the AdventureX 2026 application so each answer has one purpose, matches Chen Sihan's direct exploratory voice, and uses the three newly selected short-answer prompts.

**Architecture:** Treat the application as one narrative system with three memorable claims, then give every field a unique job. Update the automated content checks before replacing the draft so repetition, stale prompts, unsupported claims, and character limits remain testable.

**Tech Stack:** Markdown, Python 3 content assertions, `humanizer-zh` editorial rules.

## Global Constraints

- Keep three facts memorable: medical research origin, demonstrated ability to build working tools, and desire for sustained AI4S collaboration.
- Do not repeat scrna-omics architecture metrics outside its project-list entry.
- Do not use model token counts, model counts, or the eight-product catalogue in copy-ready answers.
- Preserve the factual boundaries `在投`, `校级`, and `团队项目`.
- Match the user's concise, direct, ambitious, exploratory tone.

---

### Task 1: Turn editorial decisions into regression checks

**Files:**
- Modify: `tests/application_draft_check.py`

- [x] Assert that all three newly selected prompt texts are present.
- [x] Assert that the old 2036 letter prompt is absent from copy-ready content.
- [x] Assert that token usage and repetitive architecture counts are absent from long-form answers.
- [x] Assert that the single central message of each key answer is present.
- [x] Run `.venv/bin/python tests/application_draft_check.py` and confirm it fails against the old draft.

### Task 2: Rewrite the copy-ready application

**Files:**
- Modify: `output/application/AdventureX_2026_报名填写稿.md`

- [x] Rewrite self-introduction, skill summary, Idea, project selection, participation reason, and expectations according to the design spec.
- [x] Replace all three short answers with the newly selected prompts.
- [x] Move evidence commentary into a compact internal review section.
- [x] Recalculate every displayed character count.
- [x] Apply the `humanizer-zh` checklist: remove slogan endings, symmetry, inflated claims, and explanations that do not answer the prompt.

### Task 3: Validate and deliver

**Files:**
- Test: `tests/application_draft_check.py`
- Verify: `output/application/AdventureX_2026_报名填写稿.md`

- [x] Run `.venv/bin/python tests/application_draft_check.py` and expect PASS.
- [x] Run `rg` checks for stale prompts, token metrics, repeated architecture counts, and unsupported claims.
- [x] Run `ruff format tests/application_draft_check.py` when available.
- [x] Run `git diff --check`, review the final diff, commit the rewrite, and push `main`.
