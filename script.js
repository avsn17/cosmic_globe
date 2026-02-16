let audioCtx, analyser, dataArray;
const irohQuotes = [
    "While it is always best to believe in oneself, a little help is a blessing.",
    "Hope is something you give yourself.",
    "Destiny is a funny thing."
];

async function initPilot() {
    const selector = document.getElementById('freq-selector');
    const stream = selector.value;
    const theme = selector.options[selector.selectedIndex].getAttribute('data-theme');

    document.body.className = 'theme-' + theme;
    document.getElementById('login-sector').style.display = 'none';
    document.getElementById('mission-sector').style.display = 'block';

    // FIX: Initialize and Resume Audio Context on User Click
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    
    if (audioCtx.state === 'suspended') {
        await audioCtx.resume();
    }

    setupAudio(stream);
    startWarp();
}

function setupAudio(url) {
    const audio = document.getElementById('space-radio');
    audio.src = url;
    audio.setAttribute('crossorigin', 'anonymous'); // Essential for analyzing external streams
    
    analyser = audioCtx.createAnalyser();
    const source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    
    analyser.fftSize = 256;
    dataArray = new Uint8Array(analyser.frequencyBinCount);
    
    audio.play().catch(e => console.error("Playback failed:", e));
    renderLoop();
}

function renderLoop() {
    analyser.getByteFrequencyData(dataArray);
    // Focus on Bass/Mids for meteor triggers
    let volume = 0;
    for (let i = 0; i < 20; i++) volume += dataArray[i]; 
    let avg = volume / 20;

    if (avg > 80) { // Threshold for meteor advance
        spawnMeteor(avg);
    }
    requestAnimationFrame(renderLoop);
}

function spawnMeteor(intensity) {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    const x = (Math.random() - 0.5) * 2000;
    const y = (Math.random() - 0.5) * 2000;
    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%'; m.style.top = '50%';
    m.style.animation = `zoom ${255/intensity * 0.5}s ease-out forwards`;
    field.appendChild(m);
    setTimeout(() => m.remove(), 1000);
}

function startWarp() {
    let sec = 25 * 60;
    setInterval(() => {
        sec--;
        document.getElementById('timer').innerText = `${Math.floor(sec/60)}:${(sec%60).toString().padStart(2,'0')}`;
    }, 1000);
}
