/* Keep native menus and error details; retire the old overlay and cryptic search cross. */
(() => {
  let queued = false;
  const polish = () => {
    queued = false;
    document.getElementById("homeai-floating-bar")?.remove();
    document.getElementById("homeai-modal-backdrop")?.remove();
    const label = document.documentElement.lang.startsWith("zh")
      ? "知识库搜索不可用 · 查看详情"
      : "Knowledge search unavailable · Details";
    const selector = '[id$="-tool-call"] > [role="button"], [id*="-detail-group-"] > div > [role="button"]';
    document.querySelectorAll(selector).forEach((row) => {
      // Only relabel failed knowledge activity. Leave other failures and all details intact.
      const names = row.textContent.match(/\b[a-z]+_[a-z_]+\b/g) || [];
      const knowledge = names.length > 0 && names.every((name) => /^(?:search|query|list|view|grep)_knowledge/.test(name));
      const failed = Boolean(row.querySelector('.text-red-500, .text-red-400'));
      const summary = row.querySelector('.line-clamp-1');
      if (!summary) return;
      if (knowledge && failed) {
        row.classList.add('homeai-search-unavailable');
        row.setAttribute('aria-label', label);
        summary.dataset.homeaiStatus = label;
      } else if (row.classList.contains('homeai-search-unavailable')) {
        row.classList.remove('homeai-search-unavailable');
        row.removeAttribute('aria-label');
        delete summary.dataset.homeaiStatus;
      }
    });
  };
  const start = () => {
    polish();
    new MutationObserver(() => {
      if (!queued) {
        queued = true;
        requestAnimationFrame(polish);
      }
    }).observe(document.body, {childList: true, subtree: true, characterData: true});
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, {once: true});
  } else start();
})();
