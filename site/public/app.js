const search = document.querySelector("#search");
const filters = [...document.querySelectorAll("[data-filter]")];
const items = [...document.querySelectorAll(".archive-item")];
let category = "all";
function updateArchive() {
  const query = search.value.trim().toLowerCase();
  let count = 0;
  for (const item of items) {
    const visible =
      (category === "all" || item.dataset.category === category) &&
      item.dataset.search.includes(query);
    item.hidden = !visible;
    if (visible) count++;
  }
  document.querySelector("#result-count").textContent = `显示 ${count} 个项目`;
  document.querySelector("#empty").hidden = count !== 0;
}
if (search) {
  search.addEventListener("input", updateArchive);
  filters.forEach((button) =>
    button.addEventListener("click", () => {
      category = button.dataset.filter;
      filters.forEach((b) => {
        b.classList.toggle("active", b === button);
        b.setAttribute("aria-pressed", String(b === button));
      });
      updateArchive();
    }),
  );
}
const reduce = matchMedia("(prefers-reduced-motion: reduce)");
const saveData = navigator.connection?.saveData;
const videos = [...document.querySelectorAll("video[data-src]")];
const state = new WeakMap();
function load(video) {
  if (!video.src) {
    video.src = video.dataset.src;
    video.load();
  }
}
function sync(video) {
  const button = video.parentElement.querySelector(".video-control");
  const playing = !video.paused;
  button.innerHTML = `${playing ? "暂停影片" : "播放影片"} <span aria-hidden="true">${playing ? "Ⅱ" : "▶"}</span>`;
  button.setAttribute("aria-pressed", String(playing));
  button.setAttribute(
    "aria-label",
    `${playing ? "暂停" : "播放"}${video.getAttribute("aria-label")}`,
  );
}
function play(video) {
  load(video);
  video.play().catch(() => sync(video));
}
const observer =
  "IntersectionObserver" in window
    ? new IntersectionObserver(
        (entries) =>
          entries.forEach((entry) => {
            const video = entry.target,
              s = state.get(video);
            s.visible = entry.isIntersecting;
            if (
              s.visible &&
              !document.hidden &&
              !s.manualPause &&
              ((!reduce.matches && !saveData) || s.manualPlay)
            )
              play(video);
            else if (!s.visible) video.pause();
          }),
        { rootMargin: "0px", threshold: 0.1 },
      )
    : null;
for (const video of videos) {
  state.set(video, { visible: false, manualPause: false, manualPlay: false });
  video.addEventListener("play", () => sync(video));
  video.addEventListener("pause", () => sync(video));
  video.parentElement
    .querySelector(".video-control")
    .addEventListener("click", () => {
      const s = state.get(video);
      if (video.paused) {
        s.manualPause = false;
        s.manualPlay = true;
        play(video);
      } else {
        s.manualPause = true;
        s.manualPlay = false;
        video.pause();
      }
    });
  observer?.observe(video);
}
document.addEventListener("visibilitychange", () =>
  videos.forEach((video) => {
    const s = state.get(video);
    if (document.hidden) video.pause();
    else if (
      s.visible &&
      !s.manualPause &&
      ((!reduce.matches && !saveData) || s.manualPlay)
    )
      play(video);
  }),
);

reduce.addEventListener("change", () =>
  videos.forEach((video) => {
    const s = state.get(video);
    if (reduce.matches && !s.manualPlay) video.pause();
    else if (
      !reduce.matches &&
      s.visible &&
      !s.manualPause &&
      !document.hidden &&
      !saveData
    )
      play(video);
  }),
);
