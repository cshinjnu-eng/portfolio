# AdventureX Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Execute inline in this session. Do not dispatch subagents. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the portfolio into an immersive, evidence-led AdventureX site that converts visitors into research-product collaborators.

**Architecture:** Keep the existing static delivery model. Replace the monolithic presentation with semantic HTML, modular CSS, and focused vanilla JavaScript modules for hero motion, scroll narrative, project media, and accessibility. Generated atlas imagery and real project assets remain separate from source code.

**Tech Stack:** HTML5, modular CSS, vanilla JavaScript, Canvas/CSS motion, Image-2 assets, Playwright QA, Prettier.

## Global Constraints

- Follow `/Users/chensihan/Desktop/📁开发项目/portfolio/DESIGN.md` exactly.
- Keep `scrna-omics` as the largest project and research-product bridge.
- Use the current beige TimeBox materials.
- Move Claude risk self-test into media/community.
- Never call the school-level innovation project national-level.
- Do not autoplay the 12.3 MB `scrna-omics` promotional video.
- Support `prefers-reduced-motion` and keyboard interaction.
- Do not add React, Tailwind, or build tooling unless static implementation becomes impossible.

---

### Task 1: Normalize Project Assets and Content Contract

**Files:**

- Create: `assets/brand/portrait.jpg`
- Create: `assets/brand/hero-atlas.webp`
- Create: `assets/brand/atlas-light.webp`
- Create: `assets/brand/story-path.webp`
- Create: `assets/brand/research-network.webp`
- Create: `assets/projects/timebox-beige.png`
- Create: `assets/projects/claude-risk.png`
- Create: `data/projects.js`

**Interfaces:**

- Produces: `window.PORTFOLIO_PROJECTS`, a read-only array consumed by project interactions.
- Produces: optimized visual assets referenced by semantic HTML and CSS.

- [ ] **Step 1: Import verified real assets**

  Copy the supplied portrait, beige TimeBox screenshot, Claude risk visual, current Mirror report, and existing project screenshots into stable project paths without overwriting unrelated user assets.

- [ ] **Step 2: Generate the unified atlas family with Image-2**

  Generate four text-free images using the exact visual constraints in `DESIGN.md`: landscape dark hero, landscape light transition, vertical story path, and dark research network.

- [ ] **Step 3: Optimize image delivery**

  Convert large generated and screenshot assets to WebP with explicit quality settings; preserve originals only where they are source evidence.

- [ ] **Step 4: Create the project content contract**

  Define stable project IDs, verified claims, links, media types, and category labels in `data/projects.js`. No HTML is stored in data values.

- [ ] **Step 5: Validate the asset set**

  Run:

  ```bash
  find assets/brand assets/projects -type f -maxdepth 2 -print
  node --check data/projects.js
  ```

  Expected: all required assets exist and JavaScript syntax passes.

### Task 2: Rebuild Semantic Homepage Structure

**Files:**

- Modify: `index.html`
- Create: `styles/tokens.css`
- Create: `styles/base.css`
- Create: `styles/hero.css`
- Create: `styles/story.css`
- Create: `styles/projects.css`
- Create: `styles/responsive.css`
- Remove references to: `style.css`

**Interfaces:**

- Consumes: brand assets and `window.PORTFOLIO_PROJECTS`.
- Produces: stable DOM hooks `[data-chapter]`, `[data-project-trigger]`, `[data-media-dialog]`, and `[data-path-progress]`.

- [ ] **Step 1: Replace the old hero**

  Build a full-screen hero with a poster-first motion layer, floating pill navigation, staggered title lines, a research-product collaboration CTA, and a reduced-motion fallback.

- [ ] **Step 2: Build the personal causal timeline**

  Add medical training, immunology research, bioinformatics responsibility, `scrna-omics`, independent products, and collaboration as one continuous path.

- [ ] **Step 3: Build the signature `scrna-omics` chapter**

  Include real product and observatory visuals, 13/6/12 architecture evidence, two completed analyses, and a click-to-load video poster.

- [ ] **Step 4: Build the selected project index**

  Present TimeBox, Mirror, Worker Cat, and GoGoWork as ruled editorial rows with full media chapters, not nested cards.

- [ ] **Step 5: Build media, research, experience, and collaboration chapters**

  Place Claude risk self-test with media/community; present research repositories compactly; include education, skills, awards, startup work, and the final collaboration request.

- [ ] **Step 6: Validate document structure**

  Run:

  ```bash
  prettier --write index.html styles/*.css data/projects.js
  rg -n '国家级大创|入驻粤港澳|timebox\.bsbsanwu\.xyz' index.html data/projects.js
  ```

  Expected: formatting passes and forbidden stale claims return no matches.

### Task 3: Implement Purposeful Motion and Project Interaction

**Files:**

- Replace: `app.js`
- Create: `scripts/hero-motion.js`
- Create: `scripts/scroll-path.js`
- Create: `scripts/project-experience.js`
- Create: `scripts/media-dialog.js`

**Interfaces:**

- `initHeroMotion(root: HTMLElement): () => void`
- `initScrollPath(path: HTMLElement): () => void`
- `initProjectExperience(root: HTMLElement): () => void`
- `initMediaDialog(dialog: HTMLDialogElement): () => void`

- [ ] **Step 1: Add hero text and atlas motion**

  Use CSS classes plus pointer-normalized transforms. Do not animate layout properties.

- [ ] **Step 2: Add the growing vermilion evidence path**

  Update one CSS custom property from scroll progress and reveal chapter markers via IntersectionObserver.

- [ ] **Step 3: Add desktop cursor-follow project media**

  Enable only for fine pointers, constrain previews to the viewport, and disable entirely under reduced motion.

- [ ] **Step 4: Add project chapter transitions**

  Use one open chapter at a time, explicit `aria-expanded`, and mask/opacity transitions with content remaining in document flow on mobile.

- [ ] **Step 5: Add accessible video loading**

  Set the remote video source only after the play action. Support play/pause, mute, Escape close, and focus return.

- [ ] **Step 6: Validate JavaScript**

  Run:

  ```bash
  node --check app.js
  node --check scripts/*.js
  ```

  Expected: every module passes syntax checking.

### Task 4: Create and Integrate the Hero Loop

**Files:**

- Create: `motion/hero-loop.html`
- Create: `assets/brand/hero-loop.mp4`
- Create: `assets/brand/hero-loop.webm`
- Modify: `index.html`

**Interfaces:**

- Produces: 8-second seamless muted motion loop and static `hero-atlas.webp` fallback.

- [ ] **Step 1: Author deterministic atlas motion**

  Compose generated layers with CSS transforms, path growth, grain, and low-amplitude parallax in a fixed 1920 x 1080 scene.

- [ ] **Step 2: Export MP4 and WebM**

  Use the `html-animation-to-mp4` workflow and FFmpeg to produce browser-compatible media without audio.

- [ ] **Step 3: Compare live layers versus video**

  Measure file sizes and visual quality. Use poster-first video only if the initial page does not preload the full motion asset.

- [ ] **Step 4: Validate media metadata**

  Run:

  ```bash
  ffprobe -v error -show_entries format=duration,size -of default=nw=1 assets/brand/hero-loop.mp4
  ffprobe -v error -show_entries format=duration,size -of default=nw=1 assets/brand/hero-loop.webm
  ```

  Expected: both files are approximately 8 seconds, have no audio stream, and remain proportionate for a portfolio hero.

### Task 5: Cross-device, Accessibility, and Performance QA

**Files:**

- Create: `tests/portfolio-smoke.py`
- Update: `CHECKPOINT.md`

**Interfaces:**

- Produces: desktop/mobile screenshots and a machine-readable pass/fail summary.

- [ ] **Step 1: Write the Playwright smoke test**

  Test status 200, no horizontal overflow, required identity copy, project expansion, lazy video source, image loading, keyboard focus, and reduced-motion behavior.

- [ ] **Step 2: Run desktop and mobile tests**

  Run:

  ```bash
  python3 -m http.server 8765
  /opt/homebrew/opt/python@3.14/bin/python3.14 tests/portfolio-smoke.py
  ```

  Expected: 1440 x 1000 and 390 x 844 both pass.

- [ ] **Step 3: Visually inspect screenshots**

  Confirm typography, crop, story continuity, project evidence, and no generic AI-design patterns.

- [ ] **Step 4: Run final source checks**

  Run:

  ```bash
  prettier --check index.html styles/*.css scripts/*.js data/*.js
  git diff --check
  ```

  Expected: all checks pass with no whitespace errors.
