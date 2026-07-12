"use strict";

window.initHeroMotion = function initHeroMotion(root) {
  if (!root) return null;

  const media = root.querySelector(".hero-media");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let frame = 0;

  const reveal = () => root.classList.add("is-ready");
  window.requestAnimationFrame(reveal);

  function updatePointer(event) {
    if (reduceMotion.matches || !media) return;
    window.cancelAnimationFrame(frame);
    frame = window.requestAnimationFrame(() => {
      const bounds = root.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width - 0.5;
      const y = (event.clientY - bounds.top) / bounds.height - 0.5;
      root.style.setProperty("--hero-x", `${x * -36}px`);
      root.style.setProperty("--hero-y", `${y * -24}px`);
      root.style.setProperty("--depth-x", `${x * 72}px`);
      root.style.setProperty("--depth-y", `${y * 52}px`);
      root.style.setProperty("--title-x", `${x * 16}px`);
      root.style.setProperty("--title-y", `${y * 11}px`);
      root.style.setProperty("--pointer-x", `${(x + 0.5) * 100}%`);
      root.style.setProperty("--pointer-y", `${(y + 0.5) * 100}%`);
    });
  }

  function activatePointer() {
    root.classList.add("is-pointer-active");
  }

  function resetPointer() {
    root.classList.remove("is-pointer-active");
    root.style.setProperty("--hero-x", "0px");
    root.style.setProperty("--hero-y", "0px");
    root.style.setProperty("--depth-x", "0px");
    root.style.setProperty("--depth-y", "0px");
    root.style.setProperty("--title-x", "0px");
    root.style.setProperty("--title-y", "0px");
    root.style.setProperty("--pointer-x", "68%");
    root.style.setProperty("--pointer-y", "42%");
  }

  if (window.matchMedia("(pointer: fine)").matches) {
    root.addEventListener("pointerenter", activatePointer);
    root.addEventListener("pointermove", updatePointer, { passive: true });
    root.addEventListener("pointerleave", resetPointer);
  }

  return () => {
    window.cancelAnimationFrame(frame);
    root.removeEventListener("pointerenter", activatePointer);
    root.removeEventListener("pointermove", updatePointer);
    root.removeEventListener("pointerleave", resetPointer);
  };
};
