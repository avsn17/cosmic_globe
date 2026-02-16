cat << 'EOF' > script.js
let audioCtx, analyser, dataArray, source, audio;
let totalLY = parseInt(localStorage.getItem('aviDist')) || 0;
const irohQuotes = [
    "While it is always best to believe in oneself, a little help from others is a great blessing.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "Hope is something you give yourself.",
    "Good times become good memories, but bad times become good lessons."
];

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
    audio.play();
    addLog("NEURAL LINK: ESTABLISHED");
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
    analyser.fftSize = 256;
    dataArray = new Uint8Array(analyser.frequencyBinCount);
    renderEngine();
}

function renderEngine() {
    analyser.getByteFrequencyData(dataArray);
    
    let sum = 0;
    for(let i=0; i<30; i++) sum += dataArray[i];
    let intensity = sum / 30;
    
    const loadBar = document.getElementById('load-bar');
    const loadPercent = Math.min(100, intensity * 0.9);
    loadBar.style.width = `${loadPercent}%`;

    // --- COLOR SHIFT LOGIC ---
    if (loadPercent < 40) {
        loadBar.style.background = "var(--glow)"; // Normal
        loadBar.style.boxShadow = "0 0 10px var(--glow)";
    } else if (loadPercent < 75) {
        loadBar.style.background = "#ffcc33"; // Warning (Gold)
        loadBar.style.boxShadow = "0 0 15px #ffcc33";
    } else {
        loadBar.style.background = "#ff3333"; // Critical (Red)
        loadBar.style.boxShadow = "0 0 20px #ff3333";
    }

    let bass = dataArray[0];
    if (bass > 195) { 
        spawnLightStreak(bass);
    }
    requestAnimationFrame(renderEngine);
}

function spawnLightStreak(power) {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    
    const angle = Math.random() * Math.PI * 2;
    const dist = 1200 + Math.random() * 600;
    const x = Math.cos(angle) * dist;
    const y = Math.sin(angle) * dist;
    
    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%'; m.style.top = '50%';
    m.style.transform = `translate(-50%, -50%) rotate(${angle + Math.PI/2}rad)`;
    
    m.style.animation = `zoom ${0.3 + Math.random() * 0.4}s cubic-bezier(0.1, 0, 0.9, 1) forwards`;
    
    field.appendChild(m);
    setTimeout(() => m.remove(), 750);
}

function autoCycle() {
    let sec = 25 * 60;
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
    
    if (sec % 300 === 0) {
        document.getElementById('iroh-quote').innerText = irohQuotes[Math.floor(Math.random() * irohQuotes.length)];
        addLog("COMMS: MESSAGE DECODED");
    }
}

function completeMission() {
    totalLY += 100;
    localStorage.setItem('aviDist', totalLY);
    addLog(`JUMP SUCCESS: +100LY. TOTAL: ${totalLY}LY`);
    document.body.style.filter = "invert(1) hue-rotate(180deg)";
    setTimeout(() => {
        document.body.style.filter = "none";
        startBreak();
    }, 300);
}

function startBreak() {
    let bSec = 5 * 60;
    addLog("SYSTEM: REFUELING...");
    const bTimer = setInterval(() => {
        bSec--;
        document.getElementById('timer').innerText = `REST: ${Math.floor(bSec/60)}:${(bSec%60).toString().padStart(2,'0')}`;
        if (bSec <= 0) {
            clearInterval(bTimer);
            autoCycle();
        }
    }, 1000);
}

function addLog(msg) {
    const log = document.getElementById('mission-log');
    const d = new Date();
    log.innerHTML = `<div style="border-left:2px solid var(--accent); padding-left:5px; margin-bottom:5px">> ${d.getHours()}:${d.getMinutes()} - ${msg}</div>` + log.innerHTML;
}

window.onload = () => {
    const stars = document.getElementById('star-container');
    for(let i=0; i<150; i++) {
        const s = document.createElement('div');
        s.style.position = 'absolute'; s.style.width = '1px'; s.style.height = '1px';
        s.style.background = '#fff'; s.style.left = Math.random()*100+'vw';
        s.style.top = Math.random()*100+'vh'; s.style.opacity = Math.random();
        stars.appendChild(s);
    }
};
EOF