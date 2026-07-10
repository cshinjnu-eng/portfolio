"use strict";

window.initHeroMotion = function initHeroMotion(root) {
  if (!root) return null;

  const media = root.querySelector(".hero-media");
  const video = root.querySelector("[data-hero-video]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let frame = 0;
  let idleCallback = 0;

  const reveal = () => root.classList.add("is-ready");
  window.requestAnimationFrame(reveal);

  function activateVideo() {
    if (!video || reduceMotion.matches || video.dataset.loaded === "true")
      return;
    video.querySelectorAll("source[data-src]").forEach((source) => {
      source.src = source.dataset.src;
    });
    video.dataset.loaded = "true";
    video.load();
    video.play().catch(() => undefined);
  }

  function markPlaying() {
    video?.classList.add("is-playing");
  }

  function scheduleVideo() {
    if ("requestIdleCallback" in window) {
      idleCallback = window.requestIdleCallback(activateVideo, {
        timeout: 1800,
      });
    } else {
      window.setTimeout(activateVideo, 900);
    }
  }

  video?.addEventListener("playing", markPlaying);
  if (document.readyState === "complete") scheduleVideo();
  else window.addEventListener("load", scheduleVideo, { once: true });

  function updatePointer(event) {
    if (reduceMotion.matches || !media) return;
    window.cancelAnimationFrame(frame);
    if (idleCallback && "cancelIdleCallback" in window)
      window.cancelIdleCallback(idleCallback);
    video?.pause();
    video?.removeEventListener("playing", markPlaying);
    frame = window.requestAnimationFrame(() => {
      const bounds = root.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width - 0.5;
      const y = (event.clientY - bounds.top) / bounds.height - 0.5;
      root.style.setProperty("--hero-x", `${x * -12}px`);
      root.style.setProperty("--hero-y", `${y * -8}px`);
      root.style.setProperty("--depth-x", `${x * 22}px`);
      root.style.setProperty("--depth-y", `${y * 16}px`);
    });
  }

  function resetPointer() {
    root.style.setProperty("--hero-x", "0px");
    root.style.setProperty("--hero-y", "0px");
    root.style.setProperty("--depth-x", "0px");
    root.style.setProperty("--depth-y", "0px");
  }

  if (window.matchMedia("(pointer: fine)").matches) {
    root.addEventListener("pointermove", updatePointer, { passive: true });
    root.addEventListener("pointerleave", resetPointer);
  }

  return () => {
    window.cancelAnimationFrame(frame);
    root.removeEventListener("pointermove", updatePointer);
    root.removeEventListener("pointerleave", resetPointer);
  };
};
