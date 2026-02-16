let audioCtx, analyser, dataArray, source, audio;
let totalLY = localStorage.getItem('aviDist') || 0;
const irohQuotes = ["Hope is something you give yourself.", "Sharing tea is a delight.", "Destiny is funny."];

async function initPilot() {
    const sel = document.getElementById('freq-selector');
    const url = sel.value;
    document.body.className = 'theme-' + sel.options[sel.selectedIndex].getAttribute('data-theme');
    
    document.getElementById('login-sector').style.display = 'none';
    document.getElementById('mission-sector').style.display = 'block';

    if (!audioCtx) setupAudioSystem();
    if (audioCtx.state === 'suspended') await audioCtx.resume();
    
    audio.src = url;
    audio.play();
    addLog("NEURAL LINK ESTABLISHED");
    startWarp();
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

function renderMeteors() {
    analyser.getByteFrequencyData(dataArray);
    let bass = (dataArray[0] + dataArray[1] + dataArray[2]) / 3;
    if (bass > 145) {
        const m = document.createElement('div');
        m.className = 'meteor';
        const x = (Math.random() - 0.5) * 2000, y = (Math.random() - 0.5) * 2000;
        m.style.setProperty('--x', `${x}px`); m.style.setProperty('--y', `${y}px`);
        m.style.left = '50%'; m.style.top = '50%';
        m.style.animation = `zoom 0.5s ease-out forwards`;
        document.getElementById('meteor-field').appendChild(m);
        setTimeout(() => m.remove(), 600);
    }
    requestAnimationFrame(renderMeteors);
}

function startWarp() {
    let sec = 25 * 60;
    const interval = setInterval(() => {
        sec--;
        document.getElementById('timer').innerText = `${Math.floor(sec/60)}:${(sec%60).toString().padStart(2,'0')}`;
        document.getElementById('progress-bar').style.width = ((1500-sec)/1500*100) + "%";
        
        if (sec <= 0) {
            clearInterval(interval);
            completeJump();
        }
    }, 1000);
}

function completeJump() {
    totalLY = parseInt(totalLY) + 100;
    localStorage.setItem('aviDist', totalLY);
    addLog(`JUMP SUCCESS: +100LY. TOTAL: ${totalLY}LY`);
    document.getElementById('ui-container').classList.add('shaking');
    setTimeout(() => {
        document.getElementById('ui-container').classList.remove('shaking');
        startWarp(); // Auto-restart
    }, 5000);
}

function addLog(msg) {
    const log = document.getElementById('mission-log');
    log.innerHTML = `> ${msg}<br>` + log.innerHTML;
}

window.onload = () => {
    // Generate Stars
    const container = document.getElementById('star-container');
    for (let i=0; i<100; i++) {
        const s = document.createElement('div');
        s.style.position = 'absolute'; s.style.width = '2px'; s.style.height = '2px';
        s.style.background = 'white'; s.style.left = Math.random()*100+'vw';
        s.style.top = Math.random()*100+'vh'; container.appendChild(s);
    }
};
