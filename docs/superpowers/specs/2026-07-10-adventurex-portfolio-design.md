# AdventureX Portfolio Design Specification

## Objective

Rebuild Chen Sihan's personal website to generate research-product collaborations at AdventureX. Within 30 seconds, a visitor must understand that Chen is a medical student and bioinformatics researcher who independently turns scientific judgment into working AI products, with `scrna-omics` as the strongest proof.

## Audience and Conversion

Primary audiences are AI4S founders, life-science platform teams, research infrastructure builders, laboratories, and collaborators who can provide compute or a larger delivery platform. The primary action is to start a conversation about research agents or single-cell analysis platforms. GitHub and project demos are secondary proof actions.

## Narrative Architecture

1. **Hero - the proposition.** "跨医学、科研与产品的独立构建者" remains the identity line. A sharper supporting proposition explains the ambition to make scientific judgment runnable in AI products.
2. **Origin - why this builder.** One year of English-taught clinical medicine, current oral-medicine training, and hands-on immunology research establish the medical lens.
3. **Research path.** Gamma-delta T-cell aging research, bioinformatics responsibility, three SCI manuscripts under review, and leadership of two research projects establish evidence discipline.
4. **Signature crossover - scrna-omics.** The largest chapter demonstrates the self-built multi-agent architecture, 13 Skills, 6 Agents, 12 deterministic Hooks, stable operation, and two completed real analyses.
5. **Independent product range.** TimeBox, Mirror, and Worker Cat demonstrate growth records, AI interaction, workflow systems, long-term memory, model integration, and complete product delivery.
6. **Team entrepreneurship.** GoGoWork demonstrates collaboration beyond solo building, with the WeChat article and online demo as proof. WTeam and AdventureX remain explicitly upcoming.
7. **Media as research distribution.** "本硕博三无", two communities of nearly 500 people, nearly 5,000 likes and saves, and the Claude risk self-test show research communication and AI consultation capability.
8. **Research repositories and smaller builds.** scAIreport, the psoriasis gamma-delta T-cell repository, Paper4AI, and selected tools remain compact proof links.
9. **Collaboration interface.** Close with a direct request: Chen offers research-product development experience and seeks compute plus a larger scientific platform.

## Hero Experience

- Full-screen hero inspired by the supplied Securify reference: looping full-viewport background motion, floating pill navigation, and staggered oversized typography.
- The reference is used for composition and pacing, not for its generic black SaaS styling.
- Motion visual: an abstract life-science atlas with rice-paper and ink-black states, cellular contours, network nodes, and a single vermilion evidence path.
- Desktop title uses Readex Pro and Noto Sans SC at `clamp(64px, 9vw, 148px)`, letter spacing near `-0.055em`, line height `0.94`.
- A small handwritten annotation adds the personal sentence "时机成熟了，我想参与其中" after the main proposition.
- Primary CTA: view `scrna-omics`. Secondary CTA: discuss research-product collaboration.
- Background video is muted, looped, inline, and nonessential. A still poster and reduced-motion mode preserve the composition without video.

## Core Project Presentation

### scrna-omics

- Occupies one full chapter rather than a standard card.
- Opens with the product website, then crosses into the real research observatory.
- Includes a click-to-play video using `https://scrna-omics.bsbsanwu.xyz/assets/video/scrna-omics-promo.mp4` and its existing poster.
- Explicitly states that every system component was independently completed and that two real analyses were delivered efficiently.
- Provides links to the promotional site, investor demo, scAIreport, and relevant repository where public.

### TimeBox

- Uses the beige current interface from the private project materials.
- The story emphasizes personal growth records, behavior traces, Hermes long-term context, and AI interaction.
- The current URL is `https://timebox-private.bsbsanwu.xyz/`.
- Old dark or blue-purple promotional frames are not used as the main preview.

### Mirror

- Uses `https://mirror-opinion.bsbsanwu.xyz/r/degree/` as the representative report.
- Shows the service home, research workflow, and the degree report as a delivered artifact.

### Worker Cat

- Uses real H5 interface and frame animation assets.
- Demonstrates long-term memory, model integration, tools, and playful product judgment.

### GoGoWork

- Describes Chen as a core startup-team member rather than a solo developer.
- Links the demo and the WeChat article at `https://mp.weixin.qq.com/s/SlfiV_kPU5RST9fHOxSfCg`.
- WTeam exhibition and AdventureX promotion are phrased as planned.

### Claude Risk Self-test

- Moves from the research repository list into the media and community chapter.
- Links `http://claude-risk.bsbsanwu.xyz` and uses the verified campaign poster and website imagery recovered from the named Codex session.
- Presents it as a public research-communication product based on 315 questionnaires, 249 included accounts, and 1,872 risk days, with evidence boundaries clearly stated.

## Personal Story

- A visible timeline connects medical training, immunology research, becoming a bioinformatics node, building `scrna-omics`, expanding into independent products, and seeking AI4S collaboration.
- The portrait supplied on 2026-07-10 appears in this chapter in a restrained editorial crop.
- The story does not frame the transition as leaving medicine. It frames product building as the next layer for life-science research.
- The draft remembered sentence is: "我发现时机成熟了。生命科学需要真正理解科研边界的 AI4S 产品，而我希望参与其中。"

## Interaction Model

- A vermilion path grows through the page as chapters enter the viewport.
- The project index shows cursor-following media previews on fine-pointer desktops.
- Selecting a project transitions to a full chapter using a mask or clip-path reveal.
- Images use low-amplitude parallax; generated ink layers move independently.
- Hero text reveals line by line; evidence metrics count only once and remain readable without animation.
- The floating pill navigation changes contrast by chapter and exposes the current location.
- Video opens inline or in a controlled overlay with play, pause, mute, captions where available, and a close action.
- All content remains accessible with JavaScript disabled except enhanced motion and project overlays.

## Generated Asset Set

Use Image-2 to create a coherent asset family, not unrelated posters:

1. Hero atlas, landscape 16:9, with ink-black negative space for typography.
2. Light atlas transition, landscape 16:10, rice-paper dominant.
3. Vertical research-path artwork, 4:5, for the personal story and mobile transition.
4. Dark network texture, landscape, for the `scrna-omics` chapter.
5. Optional small vermilion/ink texture masks for section reveals.

Every prompt specifies: abstract life-science atlas, Chinese ink wash plus scientific plotting, graphite cellular contours, fine network nodes, vermilion evidence path, sparse botanical green, tactile paper, no text, no logo, no fake UI, no neon, no blue-purple gradient, no glass cards.

## Implementation Shape

- Preserve the current static delivery model unless the motion requirements demonstrate a clear need for React. The supplied React/Tailwind reference is a design reference, not a mandatory framework migration.
- Split the current monolithic assets into focused CSS and JavaScript modules for hero motion, project navigation, media overlay, and scroll path.
- Use semantic HTML first. CSS custom properties implement `DESIGN.md` tokens.
- Use IntersectionObserver and requestAnimationFrame only for purposeful motion.
- The hero loop is built with generated imagery and deterministic HTML/CSS/canvas animation, then exported to MP4/WebM if the performance test favors video over live layers.

## Validation

- Verify at 1440 x 1000, 1024 x 768, 390 x 844, and a reduced-motion environment.
- No horizontal overflow.
- Every project link and media source resolves.
- Initial load does not fetch the full `scrna-omics` video.
- Hero still poster appears before any motion asset.
- Keyboard navigation reaches all project triggers, video controls, external links, and contact actions.
- Contrast meets WCAG AA for body text.
- The first 30-second view exposes identity, signature project, strongest research proof, and collaboration CTA.

## Scope Boundary

This iteration rebuilds the portfolio homepage and its interactions. It does not redesign the external project websites, publish new project claims without evidence, or add a backend contact form.
