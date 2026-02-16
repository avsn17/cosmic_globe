let audioCtx, analyser, dataArray, source, audio;
let totalFocusSeconds = parseInt(localStorage.getItem('cosmic_focus_time')) || 0;
const irohQuotes = ["Hope is something you give yourself.", "Sharing tea is a delight.", "Destiny is funny.", "Be the person you think you are."];

async function initPilot() {
    const sel = document.getElementById('freq-selector');
    const theme = sel.options[sel.selectedIndex].getAttribute('data-theme');
    
    // 🌌 START BACKGROUND SYSTEMS
    document.body.className = 'theme-' + theme;
    document.getElementById('star-container').style.opacity = '1'; // Fade in stars
    document.getElementById('login-sector').style.display = 'none';
    document.getElementById('mission-sector').style.display = 'block';
    document.getElementById('track-info').innerText = sel.options[sel.selectedIndex].text;

    if (!audioCtx) setupAudioSystem();
    if (audioCtx.state === 'suspended') await audioCtx.resume();
    
    audio.src = sel.value;
    audio.play();

    // Listeners
    document.getElementById('toggle-scanlines').addEventListener('change', (e) => {
        document.getElementById('scanline-layer').style.display = e.target.checked ? 'block' : 'none';
    });
    document.getElementById('toggle-mute').addEventListener('change', (e) => audio.muted = e.target.checked);
    
    window.addEventListener('keydown', (e) => {
        if (e.key.toLowerCase() === 'h') toggleHUD();
    });

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

    if (loadPercent > 75) {
        loadBar.style.background = "#ff3333";
        if (document.getElementById('toggle-pulse').checked) {
            document.body.style.backgroundColor = "rgba(255, 0, 0, 0.1)";
            setTimeout(() => { document.body.style.backgroundColor = ""; }, 50);
        }
        if (document.getElementById('toggle-shake').checked) document.body.classList.add('shake-active');
    } else {
        document.body.classList.remove('shake-active');
        loadBar.style.background = loadPercent < 40 ? "var(--glow)" : "#ffcc33";
    }

    let bass = dataArray[0];
    if (bass > 195 && document.getElementById('toggle-meteors').checked) spawnLightStreak();
    requestAnimationFrame(renderEngine);
}

function spawnLightStreak() {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    const speed = document.getElementById('warp-speed').value;
    const dur = 0.6 / speed;
    const angle = Math.random() * Math.PI * 2;
    const dist = 1200;
    m.style.setProperty('--x', `${Math.cos(angle)*dist}px`);
    m.style.setProperty('--y', `${Math.sin(angle)*dist}px`);
    m.style.left = '50%'; m.style.top = '50%';
    m.style.transform = `translate(-50%, -50%) rotate(${angle + Math.PI/2}rad)`;
    m.style.animation = `zoom ${dur}s linear forwards`;
    field.appendChild(m);
    setTimeout(() => m.remove(), dur * 1000);
}

function updatePilotLog() {
    totalFocusSeconds++;
    localStorage.setItem('cosmic_focus_time', totalFocusSeconds);
    const h = Math.floor(totalFocusSeconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((totalFocusSeconds % 3600) / 60).toString().padStart(2, '0');
    const s = (totalFocusSeconds % 60).toString().padStart(2, '0');
    const display = document.getElementById('total-time');
    if(display) display.innerText = `${h}h ${m}m ${s}s`;
}

function autoCycle() {
    let sec = 25 * 60;
    setInterval(() => {
        sec--;
        document.getElementById('timer').innerText = `${Math.floor(sec/60)}:${(sec%60).toString().padStart(2,'0')}`;
        updatePilotLog();
    }, 1000);
}

function toggleMenu() {
    const content = document.getElementById('menu-content');
    content.style.display = content.style.display === "none" ? "block" : "none";
}

function toggleHUD() {
    const ui = document.getElementById('ui-container');
    ui.style.opacity = ui.style.opacity === '0' ? '1' : '0';
}

function toggleFullscreen() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else if (document.exitFullscreen) document.exitFullscreen();
}

function resetLog() {
    if(confirm("Wipe Pilot Log?")) {
        totalFocusSeconds = 0;
        localStorage.setItem('cosmic_focus_time', 0);
        updatePilotLog();
    }
}

function nextQuote() {
    document.getElementById('iroh-quote').innerText = irohQuotes[Math.floor(Math.random() * irohQuotes.length)];
}

window.onload = () => {
    const stars = document.getElementById('star-container');
    stars.style.opacity = '0'; // Hidden initially
    stars.style.transition = 'opacity 2s ease-in';
    for(let i=0; i<150; i++) {
        const s = document.createElement('div');
        s.className = 'star';
        s.style.left = Math.random()*100+'vw';
        s.style.top = Math.random()*100+'vh';
        stars.appendChild(s);
    }
};
