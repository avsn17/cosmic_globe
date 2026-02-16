function startWarp() {
    const status = document.getElementById('status');
    const ui = document.getElementById('ui-container');
    
    status.innerText = "WARP ACTIVE";
    status.classList.add('locked-in');
    
    // Add shake to the whole UI
    ui.classList.add('shaking');
    
    // Stop shaking after 2 seconds but keep the warp active
    setTimeout(() => {
        ui.classList.remove('shaking');
    }, 2000);
    
    console.log("NAV-COMPUTER: WARP ENGAGED.");
}

function createStars() {
    const container = document.getElementById('star-container');
    if (!container) return;
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = Math.random() * 2 + 1 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        container.appendChild(star);
    }
}
window.onload = createStars;
