# AdventureX Resume Design Specification

## Objective

Create a formal two-page Chinese A4 resume for AdventureX that supports the same research-product collaboration goal as the website. It must print cleanly, remain text-selectable, and reserve a QR code for the finished portfolio.

## Format

- Output: PDF under `output/pdf/` plus an editable source artifact.
- Language: Chinese.
- Length: two A4 pages.
- Visual system: rice paper, ink black, restrained vermilion, editorial rules, and the same typography roles as the website.
- The background remains nearly white for reliable printing. Decorative texture stays below 3% opacity or is omitted.
- The supplied portrait is used in a small, professionally cropped frame on page one.
- Page two reserves a QR code labeled "个人网站". The QR is generated only after the final public URL is confirmed.

## Page One - Research Foundation and Signature Crossover

1. Header: name, research-product-builder positioning, phone, email, GitHub, Guangzhou, and portrait.
2. Profile: current oral-medicine study, one year of English-taught clinical-medicine education, bioinformatics and immunology research direction, and AI4S ambition.
3. Education: Jinan University, class of 2025, oral medicine. Avoid the old "降转 / 半 Gap" wording unless the user explicitly wants it retained.
4. Research experience: gamma-delta T-cell aging and bioinformatics responsibility; scRNA-seq and scTCR-seq analysis; immunology experimental design; Linux research infrastructure where relevant.
5. Research outputs: three SCI manuscripts under review, including submissions targeting journals in Q1/Q2 or above; leader of two research projects. Do not imply acceptance.
6. Signature project: `scrna-omics`, including independent system architecture, 13 Skills, 6 Agents, 12 Hooks, stable operation, and two real project analyses.
7. Honors: use only verified current wording. The 2025 school-level innovation and entrepreneurship project must not be called national-level.

## Page Two - Product Delivery, Entrepreneurship, and Reach

1. Selected products: TimeBox, Mirror, Worker Cat, and GoGoWork. State that all except GoGoWork are independently developed.
2. Entrepreneurship: Greater Bay Area innovation and entrepreneurship base shortlist/admission wording must match the latest evidence; GoGoWork core-team contribution; WTeam and AdventureX remain upcoming.
3. Media and community: "本硕博三无", AI consultation, medical research assistance, product sharing, two communities near 500 members each, nearly 5,000 likes and saves, and WeChat operations.
4. Skill hierarchy:
   - Research: bioinformatics analysis > immunology experimental design > literature crawling, bibliometrics, and knowledge-base construction.
   - Development: full stack, Android, backend architecture, and websites.
   - AI: workflows > memory systems > tool calling > model integration.
   - Product: research > content operations > UI.
5. Compact honors and links: patent, life-science competition, 2026 Jinan University AI+ Innovation Competition school second prize, and 2025 school-level innovation project, subject to final wording review.
6. QR slot and contact CTA: "科研 Agent / 单细胞分析平台合作".

## Factual Guardrails

- "三篇在投" means under review/submission, not published or accepted.
- The old resume's two-paper count is superseded.
- The innovation project is school-level, not national-level.
- The old resume's "正在申报国家级大创" line is removed.
- `scrna-omics` claims must distinguish architecture counts from project outcomes.
- GoGoWork is a team project; do not claim independent development.
- Future exhibition and promotion are labeled planned or upcoming.
- Do not publish a portrait generated from AI; use the supplied real photograph.

## Layout and Typography

- 14-16 mm margins with a strict baseline grid.
- Name: Noto Serif SC or equivalent embedded CJK serif, 26-30 pt.
- Section headings: Readex Pro / Noto Sans SC, 10-12 pt, vermilion label plus black title.
- Body: embedded CJK sans, 8.5-9.5 pt, minimum 1.4 line height.
- Dates and metrics: IBM Plex Mono or a compatible embedded mono face.
- Use rules, alignment, and spacing rather than boxed sections.
- No skill bars, star ratings, portrait filters, decorative icons, or nested cards.

## Production and Verification

- Build the editable source and PDF in the portfolio repository.
- Render every PDF revision to PNG at 160 DPI or higher.
- Inspect both pages for clipping, glyph substitution, alignment, print contrast, QR legibility, and inconsistent dates.
- Verify that text extraction preserves reading order and contact data.
- Keep the final PDF below a practical email/upload size while preserving the portrait and QR sharpness.

## Pending Inputs

- Confirm the exact formal wording and year for the Jinan University AI+ Innovation Competition award.
- Confirm whether the patent is granted or pending and its preferred public title.
- Confirm the final public portfolio URL before generating the QR code.
- Confirm whether the personal sentence should use the current draft or a revised line.
