"use strict";

window.initScrollStory = function initScrollStory(scope) {
  const root = document.documentElement;
  const story = scope.querySelector("[data-path-root]");
  const builderJourney = scope.querySelector("[data-builder-journey]");
  const steps = [...scope.querySelectorAll("[data-story-step]")];
  const parallax = scope.querySelector("[data-parallax]");
  const nav = scope.querySelector("[data-nav]");
  const lightChapters = [
    ...scope.querySelectorAll(
      ".builder-journey, .story, .work, .experience, .media-community",
    ),
  ];
  let frame = 0;

  const stepObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) =>
        entry.target.classList.toggle("is-visible", entry.isIntersecting),
      );
    },
    { rootMargin: "-24% 0px -42%", threshold: 0.01 },
  );

  steps.forEach((step) => stepObserver.observe(step));

  const navObserver = new IntersectionObserver(
    (entries) => {
      const activeLight = entries.some((entry) => entry.isIntersecting);
      nav?.classList.toggle("is-light", activeLight);
    },
    { rootMargin: "-18% 0px -72%", threshold: 0 },
  );

  lightChapters.forEach((chapter) => navObserver.observe(chapter));

  function update() {
    const scrollRange = root.scrollHeight - window.innerHeight;
    const pageProgress =
      scrollRange > 0 ? (window.scrollY / scrollRange) * 100 : 0;
    root.style.setProperty("--page-progress", `${pageProgress}%`);

    if (story) {
      const bounds = story.getBoundingClientRect();
      const usable = Math.max(1, bounds.height - window.innerHeight * 0.45);
      const progress = Math.min(
        1,
        Math.max(0, (window.innerHeight * 0.38 - bounds.top) / usable),
      );
      story.style.setProperty("--path-progress", `${progress * 100}%`);
    }

    if (builderJourney) {
      const bounds = builderJourney.getBoundingClientRect();
      const usable = Math.max(1, bounds.height - window.innerHeight * 0.45);
      const progress = Math.min(
        1,
        Math.max(0, (window.innerHeight * 0.54 - bounds.top) / usable),
      );
      builderJourney.style.setProperty("--builder-progress", String(progress));
    }

    if (
      parallax &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      const bounds = parallax.getBoundingClientRect();
      const centerOffset =
        bounds.top + bounds.height / 2 - window.innerHeight / 2;
      const amount = Math.max(-28, Math.min(28, centerOffset * -0.035));
      parallax.style.setProperty("--story-parallax", `${amount}px`);
    }
  }

  function requestUpdate() {
    window.cancelAnimationFrame(frame);
    frame = window.requestAnimationFrame(update);
  }

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate, { passive: true });
  update();

  return () => {
    window.cancelAnimationFrame(frame);
    window.removeEventListener("scroll", requestUpdate);
    window.removeEventListener("resize", requestUpdate);
    stepObserver.disconnect();
    navObserver.disconnect();
  };
};
