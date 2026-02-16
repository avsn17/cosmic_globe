let timerInterval;

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
    const warpBtn = document.getElementById('warp-btn');
    const bar = document.getElementById('progress-bar');
    
    let minutes = 25;
    let seconds = minutes * 60;
    let totalSeconds = seconds;

    status.innerText = "WARP ACTIVE";
    status.classList.add('locked-in');
    ui.classList.add('shaking');
    warpBtn.disabled = true;
    warpBtn.style.opacity = "0.3";

    timerInterval = setInterval(() => {
        seconds--;
        
        // Update Timer Text
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        document.getElementById('timer').innerText = 
            `${mins}:${secs < 10 ? '0' : ''}${secs}`;

        // Update Progress Bar
        let percent = ((totalSeconds - seconds) / totalSeconds) * 100;
        bar.style.width = percent + "%";

        if (seconds <= 0) {
            clearInterval(timerInterval);
            status.innerText = "MISSION SUCCESS";
            status.classList.remove('locked-in');
            alert("OBJECTIVE REACHED. WELL DONE, PILOT.");
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
