# 🌌 COSMIC GLOBE
### Galaxy Edition Focus Timer — v2.1

> A beautiful terminal-based Pomodoro timer with animated galaxy visualization, gamification, and ambient music integration. Live at [avsn17.github.io/cosmic_globe](https://avsn17.github.io/cosmic_globe/)

![Version](https://img.shields.io/badge/version-2.1-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Stars](https://img.shields.io/github/stars/avsn17/cosmic_globe?style=social)

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/avsn17/cosmic_globe.git
cd cosmic_globe

# Run
python3 cosmic_globe.py
```

**Or install the `apex` command globally:**

```bash
chmod +x install.sh && ./install.sh
# Then from anywhere:
apex
```

---

## 🌌 Galaxy Visualization

Every focus session takes place inside a living, breathing galaxy:

```
·  ★  ░▒░  *  ✶  ·  ★  *  ·  +  ·  ⭐︎  ·
 ·  *  ░▒▓▒░  ·  *  ·  ★  ·  *  ·  ★
★  ·  ░▒░  ☄*······  ·  ✶  ★  ·  *  ·
  ·  ★  ·  *  ·  ★  ·  *  ·  ★  ·

           25:00 — Deep Work
```

**3 parallax layers:**
- `·` Background stars — slow, dim, 80+ objects
- `* ✶ ★` Mid-layer stars — varied types, multiple colors, 40+ objects
- `★ ✶ * ⭐︎` Foreground stars — bright, fast, twinkling, 25+ objects

**Cosmic elements:**
- Nebula clouds (`░▒▓`) drifting through space
- Shooting stars with glowing tails
- Animated boot sequence on startup
- Station select screen with galaxy background

---

## 📁 Project Structure

```
cosmic_globe/
├── cosmic_globe.py        # Main focus timer application
├── station.py             # Music station manager
├── index.html             # GitHub Pages landing page
├── style.css              # Web styles
├── manifest.json          # Web app manifest
├── install.sh             # Global installer script
├── pilot_data.json        # Pilot progress data
└── mission_log.txt        # Session activity log
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎮 Gamification | XP, levels, achievements |
| 🏆 Leaderboard | Compete with other pilots |
| 🎵 Music Stations | 5 curated ambient streams |
| ⏱ Session Durations | 15 / 25 / 45 / 60 min + custom |
| 📊 Statistics | Sessions, time, streaks, averages |
| 🔥 Streaks | Daily consistency tracking |
| 💾 Data Export | Backup your progress |
| ⚙️ Settings | Customize your experience |
| 🌐 Web App | Live at GitHub Pages |

---

## 🎵 Music Stations

| # | Station | Artist | Vibe |
|---|---|---|---|
| 1 | NEBULA | Lana Del Rey | Dreamy |
| 2 | VOID | Cigarettes After Sex | Ambient |
| 3 | SPIRAL | Bee Gees | Classic |
| 4 | DRIFT | Lofi Hip Hop | Focus |
| 5 | COSMOS | Ambient Space | Deep |

---

## 🎮 Gamification

**XP System**
- Earn 4 XP per minute of focus time
- Level up every `level × 300` XP

**Achievements**

| Achievement | Requirement |
|---|---|
| First Mission | Complete 1 session |
| Veteran Pilot | Complete 10 sessions |
| Mission Master | Complete 50 sessions |
| Millennium Flight | 1000 total minutes |
| Week Warrior | 7-day streak |
| Elite Captain | Reach level 10 |

---

## 📖 Commands

```
[1]  Launch Mission    — Start a focus session
[2]  View Statistics   — See your progress
[3]  Mission History   — Past sessions
[4]  Leaderboard       — Fleet rankings
[5]  Wisdom           — Uncle Iroh quotes
[6]  Settings         — Customize
[7]  Change Stream    — Switch music
[0]  Exit             — Save and quit
```

---

## 💾 Data

All data stored locally:

```
cosmic_globe/
├── pilot_data.json        # Your XP, level, achievements
├── mission_log.txt        # Session activity log
└── sovereign_data/        # Extended pilot profiles
    └── pilot_<ID>.json
```

No cloud sync. Your data stays on your machine.

---

## ⚙️ Requirements

- Python 3.6+
- Terminal with ANSI color support
- Web browser (for music streams)

No external dependencies required.

---

## 🔧 Troubleshooting

**`apex: command not found`**
```bash
source ~/.zshrc
```

**Permission denied**
```bash
chmod +x cosmic_globe.py
```

**Python not found**
```bash
brew install python3
```

**Colors look wrong**

Use a modern terminal — iTerm2, macOS Terminal, GNOME Terminal.

---

## 📝 Changelog

**v2.1 — Galaxy Edition**
- Full galaxy with 3 parallax layers
- Nebulae, shooting stars, comet tails
- Animated boot sequence
- Station select with galaxy background
- `station.py` module added

**v2.0**
- Complete OOP rewrite
- Achievements and daily streaks
- Multiple session durations
- Statistics dashboard, settings, data export

**v1.0**
- Basic Pomodoro timer
- XP/leveling, leaderboard, mission history

---

## 🌐 Web App

Visit the live site:
**[avsn17.github.io/cosmic_globe](https://avsn17.github.io/cosmic_globe/)**

---

## 🙏 Credits

- Music via YouTube
- Wisdom: *Avatar: The Last Airbender* (Uncle Iroh)
- Design: Retro terminal aesthetics

---

## 📄 License

Free to use, modify, and share.

---

**Fly through the galaxy. Focus. Level up. 🚀✨**

*Made by [avsn17](https://github.com/avsn17)*

