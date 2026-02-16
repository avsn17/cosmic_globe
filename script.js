let audioCtx, analyser, dataArray, source, audio;
const irohQuotes = ["Hope is something you give yourself.", "Destiny is a funny thing.", "Sharing tea is a delight."];

async function initPilot() {
    const sel = document.getElementById('freq-selector');
    document.body.className = 'theme-' + sel.options[sel.selectedIndex].getAttribute('data-theme');
    document.getElementById('login-sector').style.display = 'none';
    document.getElementById('mission-sector').style.display = 'block';

    if (!audioCtx) setupAudioSystem();
    if (audioCtx.state === 'suspended') await audioCtx.resume();
    
    audio.src = sel.value;
    audio.play();
    
    // UI Event Listeners
    document.getElementById('toggle-scanlines').addEventListener('change', (e) => {
        document.getElementById('scanline-layer').style.display = e.target.checked ? 'block' : 'none';
    });

    // Keyboard Shortcut: H to Hide Central HUD only
    window.addEventListener('keydown', (e) => {
        if (e.key.toLowerCase() === 'h') {
            const ui = document.getElementById('ui-container');
            // Toggle opacity of the central UI box
            ui.style.opacity = ui.style.opacity === '0' ? '1' : '0';
        }
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

    if (loadPercent < 40) loadBar.style.background = "var(--glow)";
    else if (loadPercent < 75) loadBar.style.background = "#ffcc33";
    else {
        loadBar.style.background = "#ff3333";
        if (document.getElementById('toggle-pulse').checked) {
            document.body.style.backgroundColor = "rgba(255, 0, 0, 0.1)";
            setTimeout(() => { document.body.style.backgroundColor = ""; }, 50);
        }
    }

    let bass = dataArray[0];
    if (bass > 195 && document.getElementById('toggle-meteors').checked) { 
        spawnLightStreak(bass);
    }
    requestAnimationFrame(renderEngine);
}

function spawnLightStreak(power) {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    const angle = Math.random() * Math.PI * 2;
    const dist = 1200;
    const x = Math.cos(angle) * dist, y = Math.sin(angle) * dist;
    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%'; m.style.top = '50%';
    m.style.transform = `translate(-50%, -50%) rotate(${angle + Math.PI/2}rad)`;
    m.style.animation = `zoom 0.5s linear forwards`;
    field.appendChild(m);
    setTimeout(() => m.remove(), 500);
}

function autoCycle() {
    let sec = 25 * 60;
    setInterval(() => {
        sec--;
        const mins = Math.floor(sec/60);
        const s = (sec%60).toString().padStart(2,'0');
        document.getElementById('timer').innerText = `${mins}:${s}`;
    }, 1000);
}

window.onload = () => {
    const stars = document.getElementById('star-container');
    for(let i=0; i<100; i++) {
        const s = document.createElement('div');
        s.className = 'star';
        s.style.left = Math.random()*100+'vw';
        s.style.top = Math.random()*100+'vh';
        s.style.position = 'absolute';
        s.style.width = '2px';
        s.style.height = '2px';
        s.style.background = 'white';
        stars.appendChild(s);
    }
};
