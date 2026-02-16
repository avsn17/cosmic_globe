cat << 'EOF' > script.js
function createStars() {
    const container = document.getElementById('star-container');
    if (!container) return;

    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        const size = Math.random() * 2 + 1 + 'px';
        star.style.width = size;
        star.style.height = size;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        star.style.animationDelay = (Math.random() * 5) + 's';
        container.appendChild(star);
    }
}

function startWarp() {
    const status = document.getElementById('status');
    if (status) {
        status.innerText = "WARP ACTIVE";
        status.classList.add('locked-in');
    }
    
    console.log("NAV-COMPUTER: WARP ENGAGED. LOCKING INTERFACE.");
}

// Initialize stars on load
window.onload = createStars;
EOF