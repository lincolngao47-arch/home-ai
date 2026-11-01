/* Retire the old floating guide/language controls. Native WebUI menus remain. */
(() => {
  const removeLegacyOverlay = () => {
    document.getElementById("homeai-floating-bar")?.remove();
    document.getElementById("homeai-modal-backdrop")?.remove();
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", removeLegacyOverlay, {
      once: true,
    });
  } else {
    removeLegacyOverlay();
  }
})();
