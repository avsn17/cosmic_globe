// 1. Wisdom Database
const irohQuotes = [
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Failure is only the opportunity to begin again, only this time, more wisely.",
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "It is important to draw wisdom from many different places.",
    "Good times become good memories, but bad times become good lessons.",
    "You must look within yourself to save yourself from your other self."
];

// 2. Initialize Pilot (The Save Button)
function initPilot() {
    console.log("System: Initialization sequence started...");
    const usernameInput = document.getElementById('username');
    const missionSector = document.getElementById('mission-sector');
    const loginSector = document.getElementById('login-sector');
    const displayName = document.getElementById('display-name');

    if (usernameInput && usernameInput.value.trim() !== "") {
        displayName.innerText = usernameInput.value.toUpperCase();
        loginSector.style.display = "none";
        missionSector.style.display = "block";
        console.log("Pilot Identifed: " + usernameInput.value);
    } else {
        alert("CRITICAL ERROR: Pilot Callsign Required.");
    }
}

// 3. Warp Logic
function startWarp() {
    const status = document.getElementById('status');
    const bar = document.getElementById('progress-bar');
    let seconds = 25 * 60;
    let total = seconds;

    status.innerText = "WARP ACTIVE";
    status.classList.add('locked-in');

    const timerInterval = setInterval(() => {
        seconds--;
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        document.getElementById('timer').innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        bar.style.width = ((total - seconds) / total * 100) + "%";

        if (seconds <= 0) {
            clearInterval(timerInterval);
            status.innerText = "MISSION SUCCESS";
        }
    }, 1000);
}

// 4. Iroh Chat
function handleIroh(event) {
    if (event.key === "Enter") {
        const quoteDisplay = document.getElementById('iroh-quote');
        const randomQuote = irohQuotes[Math.floor(Math.random() * irohQuotes.length)];
        quoteDisplay.innerText = `"${randomQuote}"`;
        document.getElementById('pilot-input').value = "";
    }
}

// 5. Background Stars
function createStars() {
    const container = document.getElementById('star-container');
    if (!container) return;
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = '2px';
        star.style.height = '2px';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        container.appendChild(star);
    }
}
window.onload = createStars;
