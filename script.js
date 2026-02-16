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
    
    // Calculate Neural Load (Music Intensity)
    let sum = 0;
    for(let i=0; i<30; i++) sum += dataArray[i];
    let intensity = sum / 30;
    
    // Update Load Bar
    document.getElementById('load-bar').style.width = `${Math.min(100, intensity * 0.8)}%`;

    // Bass Peak Detection for Meteors
    let bass = dataArray[0];
    if (bass > 190) { // High threshold for "clean" hits
        spawnLightStreak(bass);
    }
    requestAnimationFrame(renderEngine);
}

function spawnLightStreak(power) {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    
    // Calculate polar coordinates for a circular explosion effect
    const angle = Math.random() * Math.PI * 2;
    const dist = 1000 + Math.random() * 500;
    const x = Math.cos(angle) * dist;
    const y = Math.sin(angle) * dist;
    
    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%'; m.style.top = '50%';
    m.style.transformOrigin = 'center';
    m.style.transform = `rotate(${angle + Math.PI/2}rad)`;
    
    m.style.animation = `zoom ${0.4 + Math.random() * 0.3}s cubic-bezier(0.1, 0, 0.9, 1) forwards`;
    
    field.appendChild(m);
    setTimeout(() => m.remove(), 700);
}

function autoCycle() {
    let sec = 25 * 60;
    const timer = setInterval(() => {
        sec--;
        const mins = Math.floor(sec/60);
        const s = (sec%60).toString().padStart(2,'0');
        document.getElementById('timer').innerText = `${mins}:${s}`;
        document.getElementById('progress-bar').style.width = `${((1500-sec)/1500)*100}%`;
        
        if (sec % 300 === 0) {
            document.getElementById('iroh-quote').innerText = irohQuotes[Math.floor(Math.random()*irohQuotes.length)];
            addLog("COMMS: NEW MESSAGE FROM IROH");
        }

        if (sec <= 0) {
            clearInterval(timer);
            completeMission();
        }
    }, 1000);
}

function completeMission() {
    totalLY += 100;
    localStorage.setItem('aviDist', totalLY);
    addLog(`JUMP SUCCESS: +100LY. CURRENT: ${totalLY}LY`);
    document.body.style.animation = "shake 0.5s";
    setTimeout(() => {
        document.body.style.animation = "";
        startBreak();
    }, 500);
}

function startBreak() {
    let bSec = 5 * 60;
    addLog("SYSTEM: ENTERING REFUELING MODE");
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
    log.innerHTML = `<div style="margin-bottom:5px">> ${d.getHours()}:${d.getMinutes()} - ${msg}</div>` + log.innerHTML;
}

window.onload = () => {
    const stars = document.getElementById('star-container');
    for(let i=0; i<150; i++) {
        const s = document.createElement('div');
        s.style.position = 'absolute';
        s.style.width = '1px'; s.style.height = '1px';
        s.style.background = '#fff';
        s.style.left = Math.random()*100+'vw';
        s.style.top = Math.random()*100+'vh';
        s.style.opacity = Math.random();
        stars.appendChild(s);
    }
};
EOF