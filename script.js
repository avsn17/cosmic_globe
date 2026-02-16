cat << 'EOF' > script.js
let audioCtx, analyser, dataArray, source, audio;
let totalLY = parseInt(localStorage.getItem('aviDist')) || 0;
const irohQuotes = [
    "While it is always best to believe in oneself, a little help from others is a great blessing.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Sometimes the best way to solve your own problems is to help someone else."
];

// --- AUTO-BOOT ENGINE ---
async function initPilot() {
    const sel = document.getElementById('freq-selector');
    const url = sel.value;
    const theme = sel.options[sel.selectedIndex].getAttribute('data-theme');
    
    document.body.className = 'theme-' + theme;
    document.getElementById('login-sector').style.display = 'none';
    document.getElementById('mission-sector').style.display = 'block';

    if (!audioCtx) setupAudioSystem();
    if (audioCtx.state === 'suspended') await audioCtx.resume();
    
    audio.src = url;
    audio.play().catch(() => console.log("Waiting for user interaction..."));
    
    addLog("SYSTEM: NEURAL LINK AUTO-STABILIZED");
    autoCycle(); 
}

function setupAudioSystem() {
    audio = document.getElementById('space-radio');
    audio.crossOrigin = "anonymous";
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    analyser.fftSize = 128;
    dataArray = new Uint8Array(analyser.frequencyBinCount);
    renderMeteors();
}

// --- BEAT-DRIVEN VISUALS ---
function renderMeteors() {
    analyser.getByteFrequencyData(dataArray);
    let bass = (dataArray[0] + dataArray[1] + dataArray[2]) / 3;
    
    // Auto-adjust sensitivity based on volume
    if (bass > 140) {
        spawnMeteor(bass);
    }
    requestAnimationFrame(renderMeteors);
}

function spawnMeteor(intensity) {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    const x = (Math.random() - 0.5) * 2000, y = (Math.random() - 0.5) * 2000;
    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%'; m.style.top = '50%';
    m.style.animation = `zoom ${Math.max(0.3, 160/intensity)}s ease-out forwards`;
    field.appendChild(m);
    setTimeout(() => m.remove(), 800);
}

// --- PERPETUAL MISSION LOGIC ---
function autoCycle() {
    let sec = 25 * 60;
    addLog("MISSION: WARP SEQUENCE INITIATED");
    
    const timer = setInterval(() => {
        sec--;
        updateUI(sec);
        
        if (sec <= 0) {
            clearInterval(timer);
            completeMission();
        }
    }, 1000);
}

function updateUI(sec) {
    const mins = Math.floor(sec/60);
    const s = (sec%60).toString().padStart(2,'0');
    document.getElementById('timer').innerText = `${mins}:${s}`;
    document.getElementById('progress-bar').style.width = `${((1500-sec)/1500)*100}%`;
    
    // Auto-Quote change
    if (sec % 300 === 0) {
        const quote = irohQuotes[Math.floor(Math.random() * irohQuotes.length)];
        document.getElementById('iroh-quote').innerText = `"${quote}"`;
    }
}

function completeMission() {
    totalLY += 100;
    localStorage.setItem('aviDist', totalLY);
    addLog(`SUCCESS: +100LY SECURED. NEW TOTAL: ${totalLY}LY`);
    
    // Trigger Visual "Sonic Boom"
    document.body.style.filter = "invert(1)";
    setTimeout(() => {
        document.body.style.filter = "none";
        addLog("BREAK: REFUELING SYSTEMS (5m)");
        startBreak();
    }, 200);
}

function startBreak() {
    let breakSec = 5 * 60;
    const bTimer = setInterval(() => {
        breakSec--;
        document.getElementById('timer').innerText = `REST: ${Math.floor(breakSec/60)}:${(breakSec%60).toString().padStart(2,'0')}`;
        if (breakSec <= 0) {
            clearInterval(bTimer);
            autoCycle(); // Perpetual restart
        }
    }, 1000);
}

function addLog(msg) {
    const log = document.getElementById('mission-log');
    const entry = document.createElement('div');
    entry.innerHTML = `> ${new Date().toLocaleTimeString()}: ${msg}`;
    log.prepend(entry);
}

// Background Star Generation
window.onload = () => {
    const container = document.getElementById('star-container');
    for (let i=0; i<150; i++) {
        const s = document.createElement('div');
        s.className = 'star';
        s.style.left = Math.random()*100+'vw';
        s.style.top = Math.random()*100+'vh';
        s.style.animationDelay = Math.random()*5+'s';
        container.appendChild(s);
    }
};
EOF