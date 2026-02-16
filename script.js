const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_KEY = 'YOUR_SUPABASE_ANON_KEY';

const irohQuotes = [
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Failure is only the opportunity to begin again, only this time, more wisely.",
    "Hope is something you give yourself.",
    "A moment of patience in a moment of anger saves you a hundred moments of regret."
];

let pilotName = "";
let totalLY = 0;
let isWarping = false;

// --- AUTOMATED MISSION ENGINE ---
function startAutomatedCycle() {
    if (isWarping) return;
    isWarping = true;
    
    let seconds = 25 * 60; 
    const status = document.getElementById('status');
    const bar = document.getElementById('progress-bar');
    const timer = document.getElementById('timer');

    status.innerText = "WARP ACTIVE";
    status.className = "locked-in";
    document.getElementById('ui-container').classList.add('shaking');
    setTimeout(() => document.getElementById('ui-container').classList.remove('shaking'), 2000);

    const mission = setInterval(() => {
        seconds--;
        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;
        timer.innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        bar.style.width = (( (25*60) - seconds) / (25*60) * 100) + "%";

        if (seconds <= 0) {
            clearInterval(mission);
            completeMission();
        }
    }, 1000);
}

async function completeMission() {
    totalLY += 100;
    status.innerText = "REFUELING / MEDITATION";
    status.className = "";
    document.getElementById('user-dist').innerText = totalLY;
    
    // Auto-save to Live Leaderboard
    await saveDistance(totalLY);
    updateEnvironment(totalLY);

    // 5 Minute Break then Auto-Restart
    let breakTime = 5 * 60;
    const breakClock = setInterval(() => {
        breakTime--;
        document.getElementById('timer').innerText = `REST: ${Math.floor(breakTime/60)}:${breakTime%60}`;
        if (breakTime <= 0) {
            clearInterval(breakClock);
            isWarping = false;
            startAutomatedCycle();
        }
    }, 1000);
}

// --- PLANETARY LANDMARKS ---
function updateEnvironment(dist) {
    const nebula = document.getElementById('nebula');
    if (dist >= 500) nebula.style.background = "radial-gradient(circle, rgba(255,100,0,0.1) 0%, transparent 70%)"; // Mars Orbit
    if (dist >= 1000) nebula.style.background = "radial-gradient(circle, rgba(0,255,200,0.1) 0%, transparent 70%)"; // Uranus Orbit
    if (dist >= 2000) nebula.style.background = "radial-gradient(circle, rgba(200,0,255,0.1) 0%, transparent 70%)"; // Deep Nebula
}

async function saveDistance(newDist) {
    try {
        await fetch(`${SUPABASE_URL}/rest/v1/leaderboard`, {
            method: 'POST',
            headers: { 
                "apikey": SUPABASE_KEY, 
                "Authorization": `Bearer ${SUPABASE_KEY}`,
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates" 
            },
            body: JSON.stringify({ username: pilotName, distance: newDist })
        });
        fetchLeaderboard();
    } catch(e) { console.log("Offline mode active."); }
}

async function fetchLeaderboard() {
    try {
        const response = await fetch(`${SUPABASE_URL}/rest/v1/leaderboard?select=*&order=distance.desc&limit=5`, {
            headers: { "apikey": SUPABASE_KEY, "Authorization": `Bearer ${SUPABASE_KEY}` }
        });
        const data = await response.json();
        const list = document.getElementById('leaderboard-list');
        list.innerHTML = ''; 
        data.forEach((entry, index) => {
            const li = document.createElement('li');
            li.innerHTML = `<span class="rank">${index + 1}.</span> ${entry.username} <span class="dist">${entry.distance} LY</span>`;
            list.appendChild(li);
        });
    } catch(e) {}
}

function initPilot() {
    const input = document.getElementById('username');
    if (input.value.trim() !== "") {
        pilotName = input.value.toUpperCase();
        document.getElementById('display-name').innerText = pilotName;
        document.getElementById('login-sector').style.display = "none";
        document.getElementById('mission-sector').style.display = "block";
        fetchLeaderboard();
        startAutomatedCycle(); // THE AUTOMATION TRIGGER
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

function createStars() {
    const container = document.getElementById('star-container');
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = '2px'; star.style.height = '2px';
        star.style.background = Math.random() > 0.8 ? '#ffcc33' : '#ffffff';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        container.appendChild(star);
    }
}
window.onload = createStars;
// Add this inside your existing script.js fetchLeaderboard function:

async function fetchLeaderboard() {
    try {
        const response = await fetch(`${SUPABASE_URL}/rest/v1/leaderboard?select=*&order=distance.desc&limit=5`, {
            headers: { "apikey": SUPABASE_KEY, "Authorization": `Bearer ${SUPABASE_KEY}` }
        });
        const data = await response.json();
        
        // Update the Chase Visuals
        const topDistance = data[0]?.distance || 1000; // Use the leader as the scale
        
        data.slice(0, 3).forEach((entry, index) => {
            const ship = document.getElementById(`ship-${index + 1}`);
            const progress = (entry.distance / (topDistance * 1.2)) * 100;
            ship.style.left = `${Math.min(progress, 90)}%`;
        });

        // Update User Ship
        const userProgress = (totalLY / (topDistance * 1.2)) * 100;
        document.getElementById('user-ship').style.left = `${Math.min(userProgress, 90)}%`;
        
        // ... rest of your leaderboard list rendering ...
    } catch(e) {}
}