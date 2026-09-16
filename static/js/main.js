// Small progressive-enhancement helpers for counter staff.
document.addEventListener("DOMContentLoaded", () => {
  // Auto-submit the search filter as the user types (debounced).
  const search = document.querySelector("input[data-autosubmit]");
  if (search) {
    let timer;
    search.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(() => search.form.submit(), 350);
    });
  }

  // Confirm before destructive actions.
  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!window.confirm(form.dataset.confirm)) e.preventDefault();
    });
  });
});
