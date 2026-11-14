// Only the files named here and the generated pages enter the public artifact.
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const out = path.join(root, "dist");
const projects = JSON.parse(
  fs.readFileSync(path.join(__dirname, "projects.json"), "utf8"),
);
const mediaFile = path.join(__dirname, "media.json");
const media = fs.existsSync(mediaFile)
  ? JSON.parse(fs.readFileSync(mediaFile, "utf8"))
  : [];
const fallback = [
  {
    slug: "scrna-omics",
    kind: "image",
    path: "assets/scrna-dashboard.png",
    caption: "观测台样例界面局部",
  },
  {
    slug: "mirror",
    kind: "image",
    path: "assets/mirror-home.png",
    caption: "平台历史预览界面",
  },
  {
    slug: "timebox",
    kind: "image",
    path: "assets/timebox-timer-v2.png",
    caption: "TimeBox v2 · 历史界面",
  },
];
const visuals = [...media, ...fallback];
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const url = (p) => `/projects/${encodeURIComponent(p.slug)}/`;
const asset = (p) => "/" + p.replace(/^\/+/, "");
const visual = (p, cls = "", selected = null) => {
  const m = selected || visuals.find((x) => x.slug === p.slug);
  if (!m)
    return `<div class="text-visual ${cls}" aria-label="项目文字摘要"><span>${esc(p.category)}</span><strong>${esc(p.title)}</strong><p>${esc(p.summary)}</p><small>项目摘要 / ${esc(p.status)}</small></div>`;
  const caption = esc(m.caption || p.title);
  if (m.kind === "video")
    return `<figure class="media media-${esc(p.slug)} ${cls}"><video muted playsinline loop preload="none" poster="${esc(asset(m.poster))}" data-src="${esc(asset(m.path))}" aria-label="${caption}"></video><button class="video-control" type="button" aria-label="播放${esc(p.title)}视频" aria-pressed="false">播放影片 <span aria-hidden="true">▶</span></button><figcaption>${caption}</figcaption></figure>`;
  return `<figure class="media media-${esc(p.slug)} ${cls}"><img src="${esc(asset(m.path))}" alt="${caption}" loading="lazy"><figcaption>${caption}</figcaption></figure>`;
};
const nav = `<header class="site-header"><a class="brand" href="/" aria-label="陈思翰，返回首页">陈思翰 <span>CHEN SIHAN</span></a><nav aria-label="主导航"><a href="/projects/">全部项目</a><a href="/#about">关于</a><a href="/#contact">联系 ↗</a></nav></header>`;
const footer = `<footer id="contact" class="footer"><div><p class="eyebrow">KEEP IN TOUCH</p><h2>聊聊医学、研究与工具。</h2><p>欢迎交流医学学习、科研与工具创作。</p></div><div class="footer-links"><a href="mailto:2683973782@qq.com">2683973782@qq.com ↗</a><a href="https://github.com/cshinjnu-eng/">GitHub ↗</a><a href="/output/pdf/陈思翰_AdventureX_个人作品集.pdf">历史作品集 PDF ↗</a><a href="/output/pdf/陈思翰_AdventureX_个人简历.pdf">历史个人简历 PDF ↗</a><a href="/output/pdf/陈思翰_AdventureX_正式简历.pdf">历史正式简历 PDF ↗</a></div><p class="copyright">© 陈思翰 · 在学习中实践</p></footer>`;
const page = (title, body, desc) =>
  `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="${esc(desc)}"><title>${esc(title)} · 陈思翰</title><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head><body><a class="skip" href="#main">跳至内容</a>${nav}<main id="main">${body}</main>${footer}</body></html>`;
const intro = (p) =>
  `<div class="project-meta"><div><p class="category">${esc(p.category)} <span> / </span> ${p.parent ? "Jmate 模块 · " : ""}${esc(p.status)}</p><h3><a href="${url(p)}">${esc(p.title)} <span aria-hidden="true">↗</span></a></h3><p>${esc(p.summary)}</p></div><a class="round-link" href="${url(p)}" aria-label="查看${esc(p.title)}案例">↗</a></div>`;
const featured = [
  "scrna-omics",
  "dental-trauma",
  "timebox",
  "jmate-photo",
  "mirror",
  "cat",
  "jmate",
  "genealogy",
].map((slug) => projects.find((p) => p.slug === slug));
const hero = projects.find((p) => p.slug === "scrna-omics");
const home = `<section class="hero"><div class="hero-copy"><p class="eyebrow">MEDICINE / RESEARCH / MAKING</p><h1>学口腔医学，<br><em>也做研究与工具。</em></h1><p class="hero-intro">我是陈思翰，暨南大学口腔医学学生。关注临床、科研与 AI 工具，也喜欢把想法做成可以使用的东西。</p><a class="text-link" href="#selected">探索精选项目 <span>↓</span></a></div><div class="hero-image"><figure class="media brand-image"><img src="/assets/brand-concept.webp" alt="牙冠、玻片与抽象细胞组成的概念静物"><figcaption>Jmate 生成的概念视觉</figcaption></figure></div><div class="hero-bottom"><span>学习、研究，也动手创造。</span><span>向下浏览 ↓</span></div></section><section class="selected section" id="selected"><div class="section-heading"><div><p class="eyebrow">SELECTED WORK</p><h2>一些正在做的事<span class="red">。</span></h2></div><p>从科研工作流到互动体验，<br>看看这些项目如何展开。</p></div><div class="work-grid">${featured.map((p, i) => `<article class="work work-${i + 1}">${visual(p)}${intro(p)}</article>`).join("")}</div><div class="archive-callout"><p>还有更多想法与实践</p><a href="/projects/">浏览全部 ${projects.length} 个项目与模块 <span>↗</span></a></div></section><section class="about section" id="about"><p class="eyebrow">ABOUT</p><div><h2>我在学什么，<br>也在做什么。</h2><p>我在暨南大学学习口腔医学，未来希望成为一名口腔医生。我也关注科研方法与 AI 工具，尝试用代码、设计和协作，把复杂的问题拆解成可以理解、可以尝试的过程。</p><a class="text-link" href="/projects/">看看我的项目 <span>↗</span></a></div></section>`;
const categories = [...new Set(projects.map((p) => p.category))];
const archive = `<section class="archive section"><div class="archive-head"><p class="eyebrow">PROJECT INDEX / 项目索引</p><h1>所有探索<span class="red">。</span></h1><p>这里收录了 ${projects.length} 个项目与模块，从医学学习、研究到工具和互动创作。</p></div><div class="filters"><label for="search">搜索项目</label><input id="search" type="search" placeholder="输入名称或关键词" autocomplete="off"><div class="filter-buttons" role="group" aria-label="项目分类"><button type="button" class="active" data-filter="all" aria-pressed="true">全部</button>${categories.map((c) => `<button type="button" data-filter="${esc(c)}" aria-pressed="false">${esc(c)}</button>`).join("")}</div><p id="result-count" aria-live="polite">显示 ${projects.length} 个项目</p></div><div class="archive-grid">${projects.map((p) => `<article class="archive-item" data-category="${esc(p.category)}" data-search="${esc([p.title, p.slug, p.summary, p.status, p.category, p.parent, projects.find((parent) => parent.slug === p.parent)?.title].filter(Boolean).join(" ").toLowerCase())}">${visual(p)}${intro(p)}</article>`).join("")}</div><p id="empty" hidden>没有找到匹配的项目。试试其他关键词或分类。</p></section>`;
function casePage(p) {
  const related = projects
    .filter(
      (x) =>
        x.slug !== p.slug &&
        (x.category === p.category ||
          x.slug === p.parent ||
          x.parent === p.slug),
    )
    .sort(
      (a, b) =>
        Number(b.slug === p.parent || b.parent === p.slug) -
        Number(a.slug === p.parent || a.parent === p.slug),
    )
    .slice(0, 3);
  const parent = p.parent && projects.find((x) => x.slug === p.parent);
  return `<article class="case section"><a class="back" href="/projects/">← 返回全部项目</a><header class="case-heading"><div><p class="eyebrow">${esc(p.category)} / ${esc(p.status)}</p><h1>${esc(p.title)}</h1><p class="case-lead">${esc(p.summary)}</p>${parent ? `<p class="parent-note">${esc(parent.title)}的模块 · <a href="${url(parent)}">查看父项目 ↗</a></p>` : ""}</div><div class="case-role"><span>我的角色</span><p>${esc(p.role)}</p></div></header>${visual(p, "case-media")}<div class="case-story"><div class="story-aside"><p class="eyebrow">THE PROJECT</p><p>${esc(p.status)}</p></div><div class="story-body"><section><h2>从什么问题出发</h2><p>${esc(p.problem)}</p></section><section><h2>如何展开</h2><p>${esc(p.implementation)}</p></section><section><h2>目前的成果</h2><p>${esc(p.outcome)}</p></section><section class="boundary"><h2>状态与边界</h2><p>${esc(p.boundary)}</p></section>${p.links.length ? `<div class="case-links">${p.links.map((l) => `<a href="${esc(l.url)}">${esc(l.label)} ↗</a>`).join("")}</div>` : ""}</div></div>${
    visuals.filter((x) => x.slug === p.slug).slice(1).length
      ? `<section class="case-gallery"><p class="eyebrow">MORE VIEWS / 项目画面</p><div>${visuals
          .filter((x) => x.slug === p.slug)
          .slice(1)
          .map((m) => visual(p, "", m))
          .join("")}</div></section>`
      : ""
  }<div class="related"><div class="section-heading"><h2>继续探索</h2><a class="text-link" href="/projects/">全部项目 ↗</a></div><div>${related.map((x) => `<a href="${url(x)}"><span>${esc(x.category)}</span><strong>${esc(x.title)}</strong><span>↗</span></a>`).join("")}</div></div></article>`;
}
fs.rmSync(out, { recursive: true, force: true });
function write(dest, value) {
  const target = path.join(out, dest);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, value);
}
function copy(source, dest) {
  const target = path.join(out, dest);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(path.join(__dirname, source), target);
}
for (const f of ["style.css", "app.js"]) copy(`public/${f}`, f);
for (const f of [
  "scrna-dashboard.png",
  "mirror-home.png",
  "timebox-timer-v2.png",
  "brand-concept.webp",
])
  copy(`public/assets/${f}`, `assets/${f}`);
for (const m of media)
  for (const f of [m.path, m.poster].filter(Boolean)) copy(`public/${f}`, f);
for (const name of [
  "陈思翰_AdventureX_个人作品集.pdf",
  "陈思翰_AdventureX_个人简历.pdf",
  "陈思翰_AdventureX_正式简历.pdf",
])
  copy(`../output/pdf/${name}`, `output/pdf/${name}`);
write("projects.json", JSON.stringify(projects, null, 2));
write(
  "index.html",
  page("首页", home, "陈思翰的个人作品集：医学学习、科研与工具创作。"),
);
write(
  "projects/index.html",
  page("全部项目", archive, "浏览陈思翰的项目索引。"),
);
for (const p of projects)
  write(`projects/${p.slug}/index.html`, page(p.title, casePage(p), p.summary));
console.log(`Built ${projects.length} project pages to dist/`);
