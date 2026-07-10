"use strict";

const cleanups = [
  window.initHeroMotion(document.querySelector("[data-hero]")),
  window.initScrollStory(document),
  window.initProjectExperience(
    document.querySelector("[data-project-experience]"),
  ),
  window.initMediaDialog(document.querySelector("[data-media-dialog]")),
].filter(Boolean);

window.addEventListener(
  "pagehide",
  () => {
    cleanups.forEach((cleanup) => cleanup());
  },
  { once: true },
);
