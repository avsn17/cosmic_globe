let audioCtx, analyser, dataArray;
const irohQuotes = ["Hope is something you give yourself.", "Failure is the opportunity to begin again."];

function initPilot() {
    const user = document.getElementById('username').value;
    if (user.trim() !== "") {
        document.getElementById('login-sector').style.display = "none";
        document.getElementById('mission-sector').style.display = "block";
        setupAudio();
        startWarp();
    }
}

function setupAudio() {
    const audio = document.getElementById('space-radio');
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    const source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    analyser.fftSize = 256;
    dataArray = new Uint8Array(analyser.frequencyBinCount);
    
    audio.play();
    detectBeat();
}

function detectBeat() {
    analyser.getByteFrequencyData(dataArray);
    // Use low-frequency (bass) data to trigger meteors
    let sum = 0;
    for (let i = 0; i < 10; i++) sum += dataArray[i];
    let average = sum / 10;

    if (average > 180) { // Threshold for "beat"
        spawnMeteor();
    }
    requestAnimationFrame(detectBeat);
}

function spawnMeteor() {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    
    // Random directions for the chase feel
    const x = (Math.random() - 0.5) * 1000;
    const y = (Math.random() - 0.5) * 1000;
    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%';
    m.style.top = '50%';
    m.style.animation = 'meteor-zoom 0.6s ease-out forwards';
    
    field.appendChild(m);
    setTimeout(() => m.remove(), 600);
}

function startWarp() {
    let seconds = 25 * 60;
    setInterval(() => {
        seconds--;
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        document.getElementById('timer').innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }, 1000);
}
