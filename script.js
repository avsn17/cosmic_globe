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
