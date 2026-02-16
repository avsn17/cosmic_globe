let audioCtx, analyser, dataArray;
const irohQuotes = [
    "Hope is something you give yourself.",
    "Destiny is a funny thing.",
    "While it is always best to believe in oneself, a little help is a blessing."
];

function initPilot() {
    const user = document.getElementById('username').value;
    const streamUrl = document.getElementById('freq-selector').value;
    
    if (user.trim() !== "") {
        document.getElementById('login-sector').style.display = "none";
        document.getElementById('mission-sector').style.display = "block";
        setupAudio(streamUrl);
        startWarp();
    }
}

function setupAudio(url) {
    const audio = document.getElementById('space-radio');
    audio.src = url;
    
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
    
    // Calculate volume/intensity
    let volume = 0;
    for (let i = 0; i < dataArray.length; i++) volume += dataArray[i];
    let average = volume / dataArray.length;

    // Trigger meteors based on audio intensity
    // Lower threshold for CAS/Lana, higher for Techno
    if (average > 60) { 
        spawnMeteor(average);
    }
    requestAnimationFrame(detectBeat);
}

function spawnMeteor(intensity) {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    
    // Faster music = Faster meteors
    const speed = (255 / intensity) * 0.5;
    const x = (Math.random() - 0.5) * 1200;
    const y = (Math.random() - 0.5) * 1200;

    m.style.setProperty('--x', `${x}px`);
    m.style.setProperty('--y', `${y}px`);
    m.style.left = '50%';
    m.style.top = '50%';
    m.style.animation = `meteor-zoom ${speed}s ease-out forwards`;
    
    field.appendChild(m);
    setTimeout(() => m.remove(), 1000);
}

function startWarp() {
    let seconds = 25 * 60;
    setInterval(() => {
        seconds--;
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        document.getElementById('timer').innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        
        // Change Iroh quote every 5 minutes
        if (seconds % 300 === 0) {
            document.getElementById('iroh-quote').innerText = irohQuotes[Math.floor(Math.random()*irohQuotes.length)];
        }
    }, 1000);
}
