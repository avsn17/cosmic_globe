const irohQuotes = [
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Failure is only the opportunity to begin again, only this time, more wisely.",
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "It is important to draw wisdom from many different places.",
    "Good times become good memories, but bad times become good lessons."
];

function initPilot() {
    const user = document.getElementById('username').value;
    if (user.trim() !== "") {
        document.getElementById('display-name').innerText = user.toUpperCase();
        document.getElementById('login-sector').style.display = "none";
        document.getElementById('mission-sector').style.display = "block";
    }
}

function handleIroh(event) {
    if (event.key === "Enter") {
        const quoteDisplay = document.getElementById('iroh-quote');
        const randomQuote = irohQuotes[Math.floor(Math.random() * irohQuotes.length)];
        quoteDisplay.innerText = `"${randomQuote}"`;
        document.getElementById('pilot-input').value = "";
    }
}

function startWarp() {
    const status = document.getElementById('status');
    const bar = document.getElementById('progress-bar');
    let seconds = 25 * 60;
    let total = seconds;

    status.innerText = "WARP ACTIVE";
    status.classList.add('locked-in');

    setInterval(() => {
        seconds--;
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        document.getElementById('timer').innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        bar.style.width = ((total - seconds) / total * 100) + "%";
    }, 1000);
}

function createStars() {
    const container = document.getElementById('star-container');
    const colors = ["#ffffff", "#00d4ff", "#ffcc33"];
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = Math.random() * 2 + 1 + 'px';
        star.style.height = star.style.width;
        star.style.background = colors[Math.floor(Math.random() * colors.length)];
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        container.appendChild(star);
    }
}
window.onload = createStars;
