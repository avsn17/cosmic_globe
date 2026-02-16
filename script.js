let audioCtx, analyser, dataArray, source, audio;
let totalFocusSeconds = parseInt(localStorage.getItem('cosmic_focus_time')) || 0;
let sessionSeconds = 0;
let timeLeft = 25 * 60;
let timerInterval;

const irohQuotes = ["Hope is something you give yourself.", "Sharing tea is a delight.", "Destiny is funny.", "Be the person you think you are."];

async function initPilot() {
    const sel = document.getElementById('freq-selector');
    document.body.className = 'theme-' + sel.options[sel.selectedIndex].getAttribute('data-theme');
    document.getElementById('star-container').style.opacity = '1';
    document.getElementById('login-sector').style.display = 'none';
    document.getElementById('mission-sector').style.display = 'block';
    document.getElementById('track-info').innerText = sel.options[sel.selectedIndex].text;

    if (!audioCtx) setupAudioSystem();
    if (audioCtx.state === 'suspended') await audioCtx.resume();
    
    audio.src = sel.value;
    audio.play();

    // Event Listeners
    window.addEventListener('keydown', (e) => { if (e.key.toLowerCase() === 'h') toggleHUD(); });
    window.addEventListener('beforeunload', saveFlightData); // AUTO-SAVE ON EXIT

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
        if (document.getElementById('toggle-shake').checked) document.body.classList.add('shake-active');
    } else {
        document.body.classList.remove('shake-active');
        loadBar.style.background = loadPercent < 40 ? "var(--glow)" : "#ffcc33";
    }

    if (dataArray[0] > 195 && document.getElementById('toggle-meteors').checked) spawnLightStreak();
    requestAnimationFrame(renderEngine);
}

function spawnLightStreak() {
    const field = document.getElementById('meteor-field');
    const m = document.createElement('div');
    m.className = 'meteor';
    const dur = 0.6 / document.getElementById('warp-speed').value;
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

function autoCycle() {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            sessionSeconds++;
            updateTimerDisplay();
        } else {
            endSession();
        }
        updatePilotLog();
    }, 1000);
}

function endSession() {
    clearInterval(timerInterval);
    saveFlightData();
    alert(`MISSION COMPLETE, PILOT.\nSession Time: ${Math.floor(sessionSeconds/60)}m recorded to Black Box.`);
    sessionSeconds = 0; // Reset for next loop
}

function saveFlightData() {
    localStorage.setItem('cosmic_focus_time', totalFocusSeconds);
    // Optional: Log last session date
    localStorage.setItem('last_session_end', new Date().toISOString());
    console.log("Flight Data Synced to Local Storage.");
}

function updatePilotLog() {
    totalFocusSeconds++;
    const h = Math.floor(totalFocusSeconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((totalFocusSeconds % 3600) / 60).toString().padStart(2, '0');
    const s = (totalFocusSeconds % 60).toString().padStart(2, '0');
    const display = document.getElementById('total-time');
    if(display) display.innerText = `${h}h ${m}m ${s}s`;
}

function updateTimerDisplay() {
    const m = Math.floor(timeLeft / 60).toString().padStart(2, '0');
    const s = (timeLeft % 60).toString().padStart(2, '0');
    document.getElementById('timer').innerText = `${m}:${s}`;
}

function setCustomTimer() {
    const mins = document.getElementById('custom-timer-input').value;
    if (mins > 0) {
        timeLeft = mins * 60;
        updateTimerDisplay();
    }
}

function toggleMenu() {
    const content = document.getElementById('menu-content');
    content.style.display = content.style.display === "none" ? "block" : "none";
}

function toggleHUD() {
    const ui = document.getElementById('ui-container');
    ui.style.opacity = ui.style.opacity === '0' ? '1' : '0';
}

function resetLog() {
    if(confirm("Wipe Pilot Log?")) {
        totalFocusSeconds = 0;
        localStorage.setItem('cosmic_focus_time', 0);
        updatePilotLog();
    }
}

window.onload = () => {
    const stars = document.getElementById('star-container');
    stars.style.opacity = '0';
    stars.style.transition = 'opacity 2s ease-in';
    for(let i=0; i<150; i++) {
        const s = document.createElement('div');
        s.className = 'star';
        s.style.left = Math.random()*100+'vw';
        s.style.top = Math.random()*100+'vh';
        stars.appendChild(s);
    }
    updatePilotLog(); // Load initial stats
};

function checkGoalStatus() {
    const goalHours = document.getElementById('goal-input').value;
    const currentHours = totalFocusSeconds / 3600;
    
    if (currentHours >= goalHours) {
        // ACHIEVED GOLD STATUS
        document.documentElement.style.setProperty('--glow', '#FFD700');
        document.documentElement.style.setProperty('--accent', '#B8860B');
        if (!document.body.classList.contains('gold-achieved')) {
            document.body.classList.add('gold-achieved');
            console.log("🏆 GOLD STATUS ACHIEVED");
            document.getElementById('track-info').innerText = "🏆 ELITE_PILOT_STATUS_ACTIVE";
        }
    } else {
        // RESET TO THEME COLOR IF BELOW GOAL (e.g. after reset)
        document.body.classList.remove('gold-achieved');
        // Theme defaults would apply from CSS classes
    }
}

// Wrap updatePilotLog to include the goal check
const baseUpdateLog = updatePilotLog;
updatePilotLog = function() {
    baseUpdateLog();
    checkGoalStatus();
};

function launchFireworks() {
    const container = document.getElementById('meteor-field');
    const colors = ['#FFD700', '#FFA500', '#FFFFFF', '#00FF41'];
    
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            const originX = Math.random() * window.innerWidth;
            const originY = Math.random() * window.innerHeight;
            
            for (let j = 0; j < 30; j++) {
                const p = document.createElement('div');
                p.className = 'firework-particle';
                const angle = Math.random() * Math.PI * 2;
                const velocity = 50 + Math.random() * 100;
                const tx = Math.cos(angle) * velocity;
                const ty = Math.sin(angle) * velocity;
                
                p.style.left = originX + 'px';
                p.style.top = originY + 'px';
                p.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                p.style.setProperty('--tx', `${tx}px`);
                p.style.setProperty('--ty', `${ty}px`);
                
                container.appendChild(p);
                setTimeout(() => p.remove(), 1000);
            }
        }, i * 300);
    }
}

// Update checkGoalStatus to trigger the fireworks once
let goalReachedNotified = false;

const originalGoalCheck = checkGoalStatus;
checkGoalStatus = function() {
    const goalHours = document.getElementById('goal-input').value;
    const currentHours = totalFocusSeconds / 3600;
    
    if (currentHours >= goalHours && !goalReachedNotified) {
        goalReachedNotified = true;
        launchFireworks();
        // Optional: Alert or visual cue
        document.getElementById('track-info').innerText = "🏆 GOAL REACHED: ELITE PILOT";
    }
    originalGoalCheck();
};
