const irohQuotes = [
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Failure is only the opportunity to begin again, only this time, more wisely.",
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "It is important to draw wisdom from many different places.",
    "Good times become good memories, but bad times become good lessons.",
    "You must look within yourself to save yourself from your other self. Only then will your true self reveal itself.",
    "Protection and power are overrated. I think you are very wise to choose happiness and love.",
    "Be careful what you wish for, Admiral. History is not always kind to its subjects."
];

function handleIroh(event) {
    if (event.key === "Enter") {
        const input = document.getElementById('pilot-input');
        const quoteDisplay = document.getElementById('iroh-quote');
        
        // Pick a random piece of wisdom
        const randomQuote = irohQuotes[Math.floor(Math.random() * irohQuotes.length)];
        
        // Visual feedback
        quoteDisplay.style.opacity = 0;
        setTimeout(() => {
            quoteDisplay.innerText = `"${randomQuote}"`;
            quoteDisplay.style.opacity = 1;
            input.value = ""; // Clear input
        }, 300);
    }
}

function initPilot() {
    const user = document.getElementById('username').value;
    if (user.trim() === "") return alert("PILOT CALLSIGN REQUIRED");
    document.getElementById('display-name').innerText = user.toUpperCase();
    document.getElementById('login-sector').style.display = "none";
    document.getElementById('mission-sector').style.display = "block";
}

function startWarp() {
    const status = document.getElementById('status');
    const ui = document.getElementById('ui-container');
    const bar = document.getElementById('progress-bar');
    let seconds = 25 * 60;
    let total = seconds;

    status.innerText = "WARP ACTIVE";
    status.classList.add('locked-in');
    ui.classList.add('shaking');

    const timerInterval = setInterval(() => {
        seconds--;
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        document.getElementById('timer').innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        bar.style.width = ((total - seconds) / total * 100) + "%";

        if (seconds <= 0) {
            clearInterval(timerInterval);
            status.innerText = "MISSION SUCCESS";
            status.classList.remove('locked-in');
        }
    }, 1000);

    setTimeout(() => ui.classList.remove('shaking'), 2000);
}

function createStars() {
    const container = document.getElementById('star-container');
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = Math.random() * 2 + 1 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        container.appendChild(star);
    }
}
window.onload = createStars;
