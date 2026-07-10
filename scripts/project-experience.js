"use strict";

window.initProjectExperience = function initProjectExperience(root) {
  if (!root) return null;

  const items = [...root.querySelectorAll("[data-project-item]")];
  const triggers = [...root.querySelectorAll("[data-project-trigger]")];
  const preview = root.querySelector("[data-cursor-preview]");
  const previewImage = preview?.querySelector("img");
  const canHover = window.matchMedia("(pointer: fine)");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const projectMap = new Map(
    (window.PORTFOLIO_PROJECTS || []).map((project) => [project.id, project]),
  );
  let pointerFrame = 0;

  function openProject(id) {
    items.forEach((item) => {
      const isOpen = item.dataset.projectItem === id;
      const trigger = item.querySelector("[data-project-trigger]");
      const panel = item.querySelector(".project-panel");
      const label = trigger?.querySelector("i");
      item.classList.toggle("is-open", isOpen);
      trigger?.setAttribute("aria-expanded", String(isOpen));
      if (panel) panel.hidden = !isOpen;
      if (label) label.textContent = isOpen ? "CLOSE" : "OPEN";
    });
  }

  function showPreview(trigger) {
    if (!preview || !previewImage || !canHover.matches || reduceMotion.matches)
      return;
    const project = projectMap.get(trigger.dataset.projectTrigger);
    if (!project?.media?.poster) return;
    previewImage.src = project.media.poster;
    preview.classList.add("is-visible");
  }

  function movePreview(event) {
    if (!preview || !canHover.matches || reduceMotion.matches) return;
    window.cancelAnimationFrame(pointerFrame);
    pointerFrame = window.requestAnimationFrame(() => {
      const width = 300;
      const height = 190;
      const x = Math.min(window.innerWidth - width - 14, event.clientX + 22);
      const y = Math.min(window.innerHeight - height - 14, event.clientY + 22);
      preview.style.transform = `translate3d(${Math.max(14, x)}px, ${Math.max(14, y)}px, 0) rotate(-2deg)`;
    });
  }

  function hidePreview() {
    preview?.classList.remove("is-visible");
  }

  triggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      if (trigger.getAttribute("aria-expanded") === "true") return;
      openProject(trigger.dataset.projectTrigger);
    });
    trigger.addEventListener("pointerenter", () => showPreview(trigger));
    trigger.addEventListener("pointermove", movePreview, { passive: true });
    trigger.addEventListener("pointerleave", hidePreview);
    trigger.addEventListener("focus", () => showPreview(trigger));
    trigger.addEventListener("blur", hidePreview);
  });

  return () => {
    window.cancelAnimationFrame(pointerFrame);
    triggers.forEach((trigger) => {
      trigger.replaceWith(trigger.cloneNode(true));
    });
  };
};
