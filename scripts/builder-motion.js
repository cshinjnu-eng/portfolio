"use strict";

window.initBuilderMotion = function initBuilderMotion(scope) {
  const root = scope?.querySelector("[data-builder-journey]");
  if (!root) return null;

  const steps = [...root.querySelectorAll("[data-builder-step]")];
  const counters = [...root.querySelectorAll("[data-count-value]")];
  const evidence = root.querySelector(".builder-evidence");
  const magneticItems = [...scope.querySelectorAll("[data-magnetic]")];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const coarsePointer = window.matchMedia("(pointer: coarse)");
  const cleanups = [];
  let counterFrame = 0;
  let countersStarted = false;

  root.dataset.motionReady = "true";

  function formatCounter(counter, value) {
    const decimals = Number(counter.dataset.countDecimals || 0);
    return value.toLocaleString("en-US", {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  }

  function setFinalCounters() {
    counters.forEach((counter) => {
      counter.textContent = formatCounter(
        counter,
        Number(counter.dataset.countValue || 0),
      );
    });
  }

  function animateCounters() {
    if (countersStarted) return;
    countersStarted = true;

    if (reduceMotion.matches) {
      setFinalCounters();
      return;
    }

    const start = window.performance.now();
    const duration = 420;

    function tick(now) {
      const progress = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - progress, 3);
      counters.forEach((counter) => {
        const target = Number(counter.dataset.countValue || 0);
        const decimals = Number(counter.dataset.countDecimals || 0);
        const factor = 10 ** decimals;
        const value = Math.round(target * eased * factor) / factor;
        counter.textContent = formatCounter(counter, value);
      });
      if (progress < 1) counterFrame = window.requestAnimationFrame(tick);
      else setFinalCounters();
    }

    counters.forEach((counter) => {
      counter.textContent = "0";
    });
    counterFrame = window.requestAnimationFrame(tick);
  }

  if (reduceMotion.matches) {
    steps.forEach((step) => step.classList.add("is-active"));
    setFinalCounters();
    root.style.setProperty("--builder-progress", "1");
  } else {
    const stepObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("is-active");
        });
      },
      { rootMargin: "-18% 0px -28%", threshold: 0.08 },
    );
    steps.forEach((step) => stepObserver.observe(step));
    cleanups.push(() => stepObserver.disconnect());

    const evidenceObserver = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          animateCounters();
          evidenceObserver.disconnect();
        }
      },
      { rootMargin: "10% 0px", threshold: 0.08 },
    );
    if (evidence) evidenceObserver.observe(evidence);
    else animateCounters();
    cleanups.push(() => evidenceObserver.disconnect());
  }

  if (!reduceMotion.matches && !coarsePointer.matches) {
    magneticItems.forEach((item) => {
      let pointerFrame = 0;
      let pointerBounds = null;

      function cacheBounds() {
        pointerBounds = item.getBoundingClientRect();
      }

      function updatePointer(event) {
        window.cancelAnimationFrame(pointerFrame);
        pointerFrame = window.requestAnimationFrame(() => {
          const bounds = pointerBounds || item.getBoundingClientRect();
          const x = (event.clientX - bounds.left) / bounds.width - 0.5;
          const y = (event.clientY - bounds.top) / bounds.height - 0.5;
          item.style.setProperty("--magnetic-x", `${x * 18}px`);
          item.style.setProperty("--magnetic-y", `${y * 14}px`);
          item.classList.add("is-magnetic");
        });
      }

      function resetPointer() {
        window.cancelAnimationFrame(pointerFrame);
        item.style.setProperty("--magnetic-x", "0px");
        item.style.setProperty("--magnetic-y", "0px");
        item.classList.remove("is-magnetic");
        pointerBounds = null;
      }

      item.addEventListener("pointerenter", cacheBounds);
      item.addEventListener("pointermove", updatePointer, { passive: true });
      item.addEventListener("pointerleave", resetPointer);
      cleanups.push(() => {
        window.cancelAnimationFrame(pointerFrame);
        item.removeEventListener("pointerenter", cacheBounds);
        item.removeEventListener("pointermove", updatePointer);
        item.removeEventListener("pointerleave", resetPointer);
      });
    });
  }

  return () => {
    window.cancelAnimationFrame(counterFrame);
    cleanups.forEach((cleanup) => cleanup());
  };
};
