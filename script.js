// Final refinement of the Centered & Docked logic
function toggleMenu() {
    const menu = document.getElementById('command-menu');
    const content = document.getElementById('menu-content');
    
    if (content.style.display === "none") {
        // Expand to Center
        content.style.display = "block";
        menu.style.top = "50%";
        menu.style.transform = "translate(-50%, -50%)";
    } else {
        // Dock to Top Center
        content.style.display = "none";
        menu.style.top = "10px";
        menu.style.transform = "translate(-50%, 0)";
    }
}
