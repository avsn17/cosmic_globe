cat << 'EOF' > script.js
let audioCtx, analyser, dataArray, source, audio;
const irohQuotes = [
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Hope is something you give yourself.",
    "Destiny is a funny thing."
];

async function initPilot() {
    const selector = document.getElementById('freq-selector');
    const streamUrl = selector.value;
    const theme = selector.options[selector.selectedIndex].getAttribute('data-theme');

    document.body.className = 'theme-' + theme;
    document.getElementById('login-sector').style.display = 'none';
    document.getElementById('mission-sector').style.display = 'block';

    // 1. Initialize Audio Graph only once
    if (!audioCtx) {
        setupAudioSystem();
    }
    
    if (audioCtx.state === 'suspended') {
        await audioCtx.resume();
    }

    // 2. Load the specific stream and play
    audio.src = streamUrl;
    audio.play().then(() => {
        console.log("Neural Link Synced: " + streamUrl);
    }).catch(err => {
        console.error("Link Failed: ", err);
    });

    startWarp();
}

function setupAudioSystem() {
    audio = document.getElementById('space-radio');
    audio.crossOrigin = "anonymous"; 
    
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    
    // Connect source only once per lifecycle
    source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    
    analyser.fftSize = 128; 
    dataArray = new Uint8Array(analyser.frequencyBinCount);
    
    renderMeteors();
}

function renderMeteors() {
    analyser.getByteFrequencyData(dataArray);
    
    // 3. Bass Detection Logic (Adjust 140 for more/less sensitivity)
    let bassIntensity = (dataArray[0] + dataArray[1] + dataArray[2]) / 3;

    if (bassIntensity > 140) { 
        spawnMeteor(bassIntensity);
    }
    
    requestAnimationFrame(renderMeteors);
}

function spawnMeteor(intensity) {
    const field = document.getElementById('meteor-field');
    if (!field) return;

    const m = document.createElement('div');
    m.className = 'meteor';
    
    const x = (Math.random() - 0.5) * window.innerWidth * 2.5;
    const y = (Math.random() - 0.5) * window.innerHeight * 2.5;
    
    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%';
    m.style.top = '50%';
    
    // Smooth zoom duration based on music power
    const duration = Math.max(0.3, 150 / intensity); 
    m.style.animation = `zoom ${duration}s ease-out forwards`;
    
    field.appendChild(m);
    setTimeout(() => m.remove(), 1000);
}

function startWarp() {
    let sec = 25 * 60;
    const timerDisplay = document.getElementById('timer');
    
    // Clear any existing intervals if pilot re-logs
    if (window.warpInterval) clearInterval(window.warpInterval);

    window.warpInterval = setInterval(() => {
        sec--;
        let mins = Math.floor(sec/60);
        let s = (sec%60).toString().padStart(2,'0');
        if (timerDisplay) timerDisplay.innerText = `${mins}:${s}`;
        
        if (sec <= 0) clearInterval(window.warpInterval);
    }, 1000);
}
EOF