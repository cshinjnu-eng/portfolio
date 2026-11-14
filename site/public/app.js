const list = document.querySelector("#project-list");
const filters = document.querySelector("#filters");
const detail = document.querySelector("#detail");
const detailContent = document.querySelector("#detail-content");
let projects = [];
let selected = "全部";
const escapeHTML = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (char) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        char
      ],
  );
function render() {
  const visible =
    selected === "全部"
      ? projects
      : projects.filter((project) => project.category === selected);
  document.querySelector("#result-count").textContent =
    `显示 ${visible.length} 个项目`;
  list.innerHTML = visible
    .map(
      (project, index) =>
        `<a class="project-row" href="#project/${encodeURIComponent(project.id)}"><span class="row-number">${String(index + 1).padStart(2, "0")}</span><span class="row-main"><strong>${escapeHTML(project.title)}</strong><span>${escapeHTML(project.summary)}</span></span><span class="row-meta">${escapeHTML(project.category)}<small>${escapeHTML(project.status)}</small></span><span class="row-arrow" aria-hidden="true">↗</span></a>`,
    )
    .join("");
  filters
    .querySelectorAll("button")
    .forEach((button) =>
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.filter === selected),
      ),
    );
}
function syncDetail() {
  const match = location.hash.match(/^#project\/([a-z0-9-]+)$/);
  const project = match && projects.find((item) => item.id === match[1]);
  if (!project) {
    if (detail.open) detail.close();
    return;
  }
  detailContent.innerHTML = `<p class="label">${escapeHTML(project.category)} / ${escapeHTML(project.status)}</p><h2 id="detail-title">${escapeHTML(project.title)}</h2><p class="detail-lead">${escapeHTML(project.summary)}</p>${project.image ? `<figure><img src="${escapeHTML(project.image)}" alt="${escapeHTML(project.imageAlt)}"><figcaption>${escapeHTML(project.imageCaption || "项目界面截图")}</figcaption></figure>` : ""}<div class="detail-grid"><h3>问题</h3><p>${escapeHTML(project.problem)}</p><h3>做法</h3><p>${escapeHTML(project.approach)}</p><h3>参与与归属</h3><p>${escapeHTML(project.role)}</p><h3>项目边界</h3><p>${escapeHTML(project.boundary)}</p></div>${project.links.length ? `<div class="detail-links">${project.links.map((link) => `<a href="${escapeHTML(link.url)}" target="_blank" rel="noreferrer">${escapeHTML(link.label)} ↗</a>`).join("")}</div>` : ""}`;
  if (!detail.open) detail.showModal();
}
filters.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-filter]");
  if (button) {
    selected = button.dataset.filter;
    render();
  }
});
detail.querySelector(".close").addEventListener("click", () => detail.close());
detail.addEventListener("close", () => {
  if (location.hash.startsWith("#project/"))
    history.replaceState(null, "", "#projects");
});
window.addEventListener("hashchange", syncDetail);
fetch("/projects.json")
  .then((response) => {
    if (!response.ok) throw new Error("请求失败");
    return response.json();
  })
  .then((data) => {
    projects = data;
    [...new Set(projects.map((project) => project.category))].forEach(
      (category) => {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.filter = category;
        button.textContent = category;
        filters.append(button);
      },
    );
    render();
    syncDetail();
  })
  .catch(() => {
    list.textContent = "作品暂时无法加载，请稍后刷新页面。";
  });
