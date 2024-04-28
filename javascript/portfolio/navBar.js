// Select elements
const menuToggle = document.getElementById("menu-toggle");
const navMenu = document.getElementById("nav-menu");
const closeBtn = document.getElementById("close-btn");
const navBar = document.getElementById("navbar");

// Toggle nav menu visibility
/// Slide in the nav menu
menuToggle.addEventListener("click", () => {
  navMenu.style.transform = "translateX(0)";
});

// Toggle nav menu visibility
/// Slide in the nav menu
menuToggle.addEventListener("click", () => {
  navBar.style.transform = "translateX(0)";
});

// Close nav menu
closeBtn.addEventListener("click", () => {
  navMenu.style.transform = "translateX(-200px)"; // Slide out the nav menu
});

// Close nav menu
closeBtn.addEventListener("click", () => {
  navBar.style.transform = "translateX(-200px)"; // Slide out the nav menu
});
