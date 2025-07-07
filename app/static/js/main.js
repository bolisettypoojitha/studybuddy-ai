// AOS Init
AOS.init();

// Dark Mode Toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("toggleMode");
  const html = document.documentElement;

  const saved = localStorage.getItem("theme");
  if (saved) {
    html.setAttribute("data-bs-theme", saved);
    toggle.textContent = saved === "dark" ? "☀️" : "🌙";
  }

  toggle.addEventListener("click", () => {
    const current = html.getAttribute("data-bs-theme");
    const next = current === "dark" ? "light" : "dark";
    html.setAttribute("data-bs-theme", next);
    localStorage.setItem("theme", next);
    toggle.textContent = next === "dark" ? "☀️" : "🌙";
  });
});
// 🌙 Dark Mode Toggle Script
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('darkModeToggle');
  const currentMode = localStorage.getItem('darkMode');

  if (currentMode === 'enabled') {
    document.body.classList.add('dark-mode');
  }

  toggle.addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');

    if (document.body.classList.contains('dark-mode')) {
      localStorage.setItem('darkMode', 'enabled');
    } else {
      localStorage.setItem('darkMode', 'disabled');
    }
  });
});
