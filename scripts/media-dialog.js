"use strict";

window.initMediaDialog = function initMediaDialog(dialog) {
  if (!dialog) return null;

  const trigger = document.querySelector("[data-video-trigger]");
  const close = dialog.querySelector("[data-video-close]");
  const video = dialog.querySelector("video");
  let returnFocus = null;

  function openDialog() {
    if (!trigger || !video) return;
    returnFocus = document.activeElement;
    if (!video.src) video.src = trigger.dataset.videoSrc;
    dialog.showModal();
    document.body.classList.add("has-dialog");
    video.play().catch(() => undefined);
  }

  function closeDialog() {
    if (!video) return;
    video.pause();
    dialog.close();
    document.body.classList.remove("has-dialog");
    if (returnFocus instanceof HTMLElement) returnFocus.focus();
  }

  function handleBackdrop(event) {
    if (event.target === dialog) closeDialog();
  }

  trigger?.addEventListener("click", openDialog);
  close?.addEventListener("click", closeDialog);
  dialog.addEventListener("click", handleBackdrop);
  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    closeDialog();
  });

  return () => {
    trigger?.removeEventListener("click", openDialog);
    close?.removeEventListener("click", closeDialog);
    dialog.removeEventListener("click", handleBackdrop);
  };
};
