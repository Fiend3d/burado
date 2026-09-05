(() => {
  const storage_key = "burado-theme";
  const system_theme = window.matchMedia("(prefers-color-scheme: dark)");
  let preference;

  try {
    const stored = localStorage.getItem(storage_key);
    if (stored === "light" || stored === "dark") preference = stored;
  } catch {
    // Theme switching still works when browser storage is unavailable.
  }

  function apply_theme() {
    const theme = preference || (system_theme.matches ? "dark" : "light");
    document.documentElement.dataset.bsTheme = theme;
    for (const input of document.querySelectorAll('input[name="theme"]')) {
      input.checked = input.value === theme;
    }
  }

  // Run before styles load to avoid flashing the wrong theme on page load.
  apply_theme();
  system_theme.addEventListener("change", apply_theme);

  document.addEventListener("DOMContentLoaded", () => {
    apply_theme();
    for (const input of document.querySelectorAll('input[name="theme"]')) {
      input.addEventListener("change", () => {
        if (!input.checked) return;
        preference = input.value;
        apply_theme();
        try {
          localStorage.setItem(storage_key, preference);
        } catch {
          // Keep the selection for this page even if it cannot be persisted.
        }
      });
    }
  });
})();
