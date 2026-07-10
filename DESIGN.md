# AdventureX Personal Brand Design System

## Visual Theme and Atmosphere

- Core idea: a living life-science research atlas where evidence, cells, decisions, and products grow along one continuous path.
- Mood: editorial, rigorous, personal, and quietly experimental.
- Brand posture: independent builder at the intersection of medicine, research, and products.
- Primary conversion: research-product collaboration around scientific agents and single-cell analysis platforms.
- References: Cyprien's immersive pacing and fluid navigation, Awwwards-scale typography, research notebooks, single-cell trajectories, Chinese ink wash, and modern editorial reports.

## Color Palette and Roles

- Rice paper: `#F3EFE5` - primary light background.
- Ink black: `#141513` - primary text and dark chapters.
- Vermilion: `#D84432` - active path, decision points, and calls to action.
- Botanical green: `#315746` - secondary scientific accent and community chapter.
- Warm gray: `#6F6B62` - secondary text.
- Hairline: `rgba(20, 21, 19, 0.18)` - dividers and evidence grids.
- Accent colors appear at most three times in one viewport. Do not create blue-purple gradients.

## Typography Rules

- Narrative display: `Noto Serif SC`, 700-900. Used for personal story, section propositions, and long-form research context.
- Decisive display: `Readex Pro`, 500-700, with `Noto Sans SC` fallback. Used for the hero, project names, metrics, and calls to action.
- Body: `Noto Sans SC`, 400-500, line height 1.7-1.9.
- Evidence and interface: `IBM Plex Mono`, 400-500. Used for metrics, dates, system labels, and code-adjacent copy.
- Personal annotation: `LXGW WenKai`, 400. Used sparingly for one short note per chapter.
- Hero title: letter spacing `-0.04em` to `-0.065em`; line height `0.92-0.98`.
- Typography, not color alone, must establish hierarchy.

## Layout Principles

- Homepage model: hybrid single-page portfolio with detailed project overlays or anchored chapters.
- Hero: full viewport with a quiet looping background motion layer, floating pill navigation, staggered oversized typography, and two clear actions.
- Main grid: asymmetric 12-column desktop grid with visible rules and generous negative space.
- Story sequence: medicine -> immunology and bioinformatics -> scrna-omics -> independent products -> entrepreneurship and media -> collaboration.
- `scrna-omics` occupies the largest project chapter and visually bridges the research and product sections.
- Project content uses full-bleed media, editorial splits, and dividers. Cards are reserved for genuinely independent or clickable objects.
- Mobile keeps all content accessible without hover and never hides essential proof behind animation.

## Motion and Interaction

- A vermilion evidence path grows as the user scrolls and connects story chapters.
- Hero typography enters in staggered lines with subtle blur-to-sharp motion.
- Generated ink and cell layers move at different low-amplitude parallax depths.
- Desktop project index supports image-follow-cursor previews.
- Project chapters reveal through masked media transitions, not nested accordion cards.
- `scrna-omics` video is click-to-play with a poster image; it does not autoplay or download its full 12.3 MB payload on initial load.
- Navigation may use restrained liquid-glass behavior only where it communicates floating depth.
- Motion uses transform and opacity wherever possible. Every effect respects `prefers-reduced-motion`.
- High-frequency interactions complete within roughly 180-260 ms; cinematic chapter transitions may take 450-700 ms.

## Image and Video Direction

- Image-2 assets share one visual grammar: rice paper or ink-black fields, graphite and ink textures, cellular contours, network nodes, one vermilion path, and sparse botanical green.
- Generated assets contain no text, logos, fake UI, or generic neon technology imagery.
- The hero loop is built from generated atlas layers and deterministic web animation, then exported as optimized MP4/WebM with a still poster fallback.
- Real project screenshots remain legible and are not restyled into fictional mockups.
- TimeBox uses the current beige visual materials and emphasizes personal growth records plus Hermes interaction.
- Claude risk self-test belongs to the media and community chapter.
- Mirror uses the degree report as its representative artifact.
- GoGoWork includes its WeChat article as external proof.

## Component Styling

- Floating navigation: one pill-shaped translucent dark surface, thin white border, restrained blur, no glow.
- Buttons: solid ink or vermilion with high contrast; secondary actions use underlined text.
- Project triggers: large typography on ruled rows, with media preview behavior on desktop.
- Metrics: open grid cells separated by rules; avoid rounded metric cards.
- Media frames: intentional single containers with 12-18 px radii only when the media is a discrete playable or clickable object.
- Focus states: visible 2 px vermilion outline with 3 px offset.

## Do and Do Not

- Do make the research-product intersection the first remembered idea.
- Do use real metrics and label future events as planned or upcoming.
- Do keep body copy left aligned and scannable.
- Do use the portrait in the personal story and resume, not as an oversized hero background.
- Do preserve the user's latest corrections: three SCI manuscripts under review; two research projects led; school-level innovation project; no national-level claim for that project.
- Do not use generic blue-purple gradients, glowing buttons, decorative glass cards, repeated icon containers, excessive centered sections, or nested cards.
- Do not autoplay audio or large videos.
- Do not turn the portfolio into a dashboard or make the visual system more complex than the projects.

## Responsive and Performance

- Breakpoints: 640 px, 900 px, 1200 px.
- Mobile: single column, 20 px side padding, minimum 16 px body text, touch targets at least 44 px.
- Tablet: asymmetric two-column project layouts where media remains readable.
- Desktop: maximum content width 1440 px and full-bleed chapter backgrounds.
- Hero poster is shown immediately; motion media loads after the critical content.
- Images use AVIF/WebP where practical, responsive sources, explicit dimensions, and lazy loading below the fold.
- Target: no horizontal overflow at 390 px; initial mobile transfer remains proportionate to a portfolio, with noncritical video deferred.

## Agent Prompt Guide

- Treat this file as the brand contract for the website, resume, posters, and generated images.
- Reuse only declared colors and type roles.
- Keep generated visuals abstract and evidence-oriented.
- Prefer spacing, alignment, rules, and typography over containers.
- Preserve real screenshots and factual wording.
- Any new motion must explain hierarchy, causality, or interactivity.
