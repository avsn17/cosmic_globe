let time = 1500, timerId = null;
let totalXP = parseInt(localStorage.getItem('cg_xp')) || 0;
let totalMeters = parseFloat(localStorage.getItem('cg_meters')) || 0;

const affirmations = [
    "BOLD: THE GLOBE IS YOURS. DON'T FLOP.",
    "BOLD: BIG SIGMA ENERGY DETECTED. LOCK IN.",
    "BOLD: IMAGINE BEING AN NPC IN 2026. CRINGE."
];

function updateDisplay() {
    let m = Math.floor(time / 60), s = time % 60;
    document.getElementById('timer-display').innerText = `${m}:${s < 10 ? '0'+s : s}`;
    document.getElementById('meters').innerText = totalMeters.toFixed(2);
    document.getElementById('xp').innerText = totalXP;
    document.getElementById('fuel-fill').style.width = `${((1500 - time) / 1500) * 100}%`;
}

function addLog(msg) {
    const log = document.getElementById('log');
    log.innerHTML += `<br>> [${new Date().toLocaleTimeString()}] ${msg}`;
    log.scrollTop = log.scrollHeight;
}

function startWarp(mins) {
    if(timerId) clearInterval(timerId);
    time = mins * 60;
    addLog(`COSMIC_GLOBE: WARP INITIATED TO ${mins} MIN SECTOR.`);
    document.getElementById('affirmation-bot').innerText = affirmations[Math.floor(Math.random() * affirmations.length)];

    timerId = setInterval(() => {
        if(time > 0) {
            time--;
            totalMeters += 0.00833; // 10 mins = 5m
            localStorage.setItem('cg_meters', totalMeters);
            updateDisplay();
        } else {
            completeMission();
        }
    }, 1000);
}

function completeMission() {
    clearInterval(timerId);
    totalXP += 50;
    localStorage.setItem('cg_xp', totalXP);
    addLog("BOLD: MISSION_PASSED. YOU ARE THE MAIN CHARACTER.");
    window.speechSynthesis.speak(new SpeechSynthesisUtterance("Mission complete. Stay cosmic."));
    updateDisplay();
}

document.getElementById('cmd-line').addEventListener('keypress', (e) => {
    if(e.key === 'Enter') {
        const input = e.target.value.toLowerCase().split(' ');
        const cmd = input[0], val = input[1];

        if(cmd === 'warp') startWarp(parseFloat(val) || 25);
        if(cmd === 'stats') addLog(`LIFETIME DIST: ${totalMeters.toFixed(2)}m | XP: ${totalXP}`);
        if(cmd === 'clear') document.getElementById('log').innerHTML = '> Logs purged.';

        e.target.value = '';
    }
});

updateDisplay();