const irohQuotes = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "While it is best to believe in oneself, a little help from others is a blessing.",
    "Sometimes the best way to solve your own problems is to help someone else."
];

let totalLY = 0;

function initPilot() {
    const user = document.getElementById('username').value;
    if (user.trim() !== "") {
        document.getElementById('login-sector').style.display = "none";
        document.getElementById('mission-sector').style.display = "block";
        startAutomatedMission();
    }
}

function startAutomatedMission() {
    let seconds = 25 * 60;
    const ui = document.getElementById('ui-container');
    const timerDisplay = document.getElementById('timer');
    
    ui.classList.add('warp-active');
    
    const cycle = setInterval(() => {
        seconds--;
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        timerDisplay.innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;

        // RANDOM HAZARD: 1% chance every second of an "Asteroid Field"
        if (Math.random() < 0.01) triggerHazard();

        if (seconds <= 0) {
            clearInterval(cycle);
            totalLY += 100;
            triggerMilestone();
            setTimeout(startAutomatedMission, 5000); // 5 sec reset
        }
    }, 1000);
}

function triggerHazard() {
    const ui = document.getElementById('ui-container');
    ui.classList.add('hazard-alert', 'shaking');
    const originalQuote = document.getElementById('iroh-quote').innerText;
    document.getElementById('iroh-quote').innerText = "Stay calm, pilot. This storm will pass.";
    
    setTimeout(() => {
        ui.classList.remove('hazard-alert', 'shaking');
        document.getElementById('iroh-quote').innerText = originalQuote;
    }, 3000);
}

function triggerMilestone() {
    document.body.style.backgroundColor = "white";
    setTimeout(() => { document.body.style.backgroundColor = "#050505"; }, 200);
}

function createStars() {
    const container = document.getElementById('star-container');
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.animationDuration = (Math.random() * 2 + 1) + 's';
        star.style.animationDelay = Math.random() * 5 + 's';
        container.appendChild(star);
    }
}
window.onload = createStars;
