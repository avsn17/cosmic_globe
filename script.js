function startWarp() {
    const status = document.getElementById('status');
    const container = document.body;
    
    // Trigger animations
    status.classList.add('locked-in');
    container.style.boxShadow = "inset 0 0 100px #00ff41";
    
    console.log("SYSTEM: NAV-COMPUTER ENGAGED. LOCKING INTERFACE.");
    
    // Create floating "Data Bits" particles
    for(let i=0; i<20; i++) {
        let bit = document.createElement('div');
        bit.innerText = Math.random() > 0.5 ? "1" : "0";
        bit.style.position = "absolute";
        bit.style.left = Math.random() * 100 + "vw";
        bit.style.top = "100vh";
        bit.style.transition = "transform 2s linear";
        document.body.appendChild(bit);
        
        setTimeout(() => {
            bit.style.transform = "translateY(-110vh)";
        }, 100);
    }
}
cat << 'EOF' > script.js
function createStars() {
    const container = document.body;
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        const size = Math.random() * 3 + 'px';
        star.style.width = size;
        star.style.height = size;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        container.appendChild(star);
    }
}

function startWarp() {
    document.getElementById('status').innerText = "LOCKING IN...";
    document.getElementById('status').classList.add('locked-in');
    console.log("WARP ENGAGED");
}

window.onload = createStars;
EOF