# SOVEREIGN APEX v2.1 GALAXY EDITION
## Enhanced Focus Timer & Progress Tracker

A beautiful terminal-based Pomodoro timer with gamification, progress tracking, ambient music integration, and a **full animated galaxy visualization**!

---

## 🌌 Galaxy Visualization Features (NEW in v2.1!)

Experience a living, breathing galaxy during your focus sessions:

### Multi-Layer Star System
- **Background Stars** (80+) - Slow-moving, dim stars creating depth
- **Mid-Layer Stars** (40+) - Various star types (✦, ★, ◌, ●, +, ✧, ⋆) in multiple colors
- **Foreground Stars** (25+) - Fast-moving bright stars with twinkling effects
- **Dynamic Star Generation** - New stars continuously spawn

### Cosmic Elements
- **Nebula Clouds** (8+) - Colorful gas clouds (░, ▒, ▓) drifting through space
- **Shooting Stars/Comets** (3+) - Streaking across the screen with tails
- **Parallax Scrolling** - Multiple speed layers create 3D depth effect
- **Twinkling Effects** - Stars pulse and shimmer realistically

### Color Palette
- Yellow, Pink, Cyan, Blue, Green, White stars
- Color-coded nebulae matching your stream theme
- Cosmic progress bar with gradient effects

---

## ✨ What's New in v2.1

### Major Improvements

1. **Better Code Structure**
   - Object-oriented design with clear class separation
   - PilotData, Leaderboard, ActivityLog, VisualEffects classes
   - Type hints for better code clarity
   - Improved error handling throughout

2. **Enhanced Features**
   - Multiple session duration options (15/25/45/60 min)
   - Achievement system with milestone unlocks
   - Daily streak tracking
   - Comprehensive statistics dashboard
   - Data export functionality
   - Settings menu for customization

3. **Improved Data Management**
   - Automatic data backup on corruption
   - Centralized data directory (`sovereign_data/`)
   - Better JSON error handling
   - Safe file operations with Path objects

4. **Better UX**
   - More intuitive menu system
   - Real-time progress percentage display
   - Welcome back messages
   - Achievement notifications
   - Improved visual formatting

5. **New Audio Options**
   - Added 2 new stream options (Lofi, Ambient Space)
   - Total of 5 curated music streams
   - Easy stream switching mid-session

6. **Extended Wisdom Library**
   - More Uncle Iroh quotes
   - Better quote display formatting

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download the script
chmod +x sovereign_apex_improved.py

# Run
python3 sovereign_apex_improved.py
```

### Requirements
- Python 3.6+
- Terminal with ANSI color support
- Web browser for music streaming

No external dependencies required!

---

## 📖 How to Use

### First Time Setup

1. **Login**: Enter your pilot ID (username)
2. **Select Stream**: Choose ambient music (1-5)
3. **Set Goal**: Define what you'll work on
4. **Launch Mission**: Start your focus session!

### Main Menu Commands

```
[1] 🚀 LAUNCH MISSION - Start a focus session
[2] 📊 VIEW STATISTICS - See your progress stats
[3] 📜 MISSION HISTORY - Review past sessions
[4] 🏆 LEADERBOARD - Compare with other pilots
[5] 💭 WISDOM - Get inspired by Uncle Iroh
[6] ⚙️  SETTINGS - Customize your experience
[7] 🔊 CHANGE STREAM - Switch music
[0] 🚪 EXIT - Save and quit
```

### Focus Session

During a session:
- Watch the animated starfield
- See your timer countdown
- View your goal at the center
- Progress bar shows completion percentage
- Press Ctrl+C to abort (no XP earned)

---

## 🎮 Gamification System

### XP & Leveling
- Earn **4 XP per minute** of focus time
- Level up every **300 XP × current level**
- Higher levels = higher leaderboard rank

### Achievements

Unlock special achievements:
- **First Mission** - Complete your first session
- **Veteran Pilot** - Complete 10 sessions
- **Mission Master** - Complete 50 sessions
- **Millennium Flight** - Reach 1000 total minutes
- **Week Warrior** - Maintain a 7-day streak
- **Elite Captain** - Reach level 10

### Leaderboard

Compete with other pilots on your system:
- Rankings based on level and XP
- See total sessions and minutes
- Track your rank over time

---

## 🎵 Music Streams

1. **NEBULA** - Lana Del Rey (Dreamy, Melancholic)
2. **VOID** - Cigarettes After Sex (Ambient, Chill)
3. **SPIRAL** - Bee Gees (Classic, Upbeat)
4. **DRIFT** - Lofi Hip Hop (Focus, Beats)
5. **COSMOS** - Ambient Space (Atmospheric, Deep)

Music auto-opens in your browser and re-triggers after each session.

---

## 📊 Data & Privacy

### Data Storage

All data is stored locally in `sovereign_data/`:
```
sovereign_data/
├── pilot_<ID>.json      # Individual pilot data
├── fleet_activity.log   # Global activity log
└── export_*.json        # Data exports (if created)
```

### Data Backup

- Corrupted files are automatically backed up
- Use Settings → Export Data to create manual backups
- No cloud sync - your data stays on your machine

### Reset Progress

Settings → Reset Progress → Type "RESET" to confirm
⚠️ This permanently deletes your data!

---

## 🎨 Customization

### Session Durations

Built-in options:
- Quick Sprint: 15 minutes
- Standard: 25 minutes (classic Pomodoro)
- Deep Dive: 45 minutes
- Ultra Focus: 60 minutes
- Custom: Any duration you want

### Default Duration

Set in Settings menu to skip selection each time.

---

## 💡 Tips for Maximum Productivity

1. **Set Specific Goals**: Instead of "work", try "finish chapter 3" or "debug login function"

2. **Use Appropriate Durations**:
   - 15 min for quick tasks
   - 25 min for focused work (standard)
   - 45-60 min for deep, complex work

3. **Build Your Streak**: Daily consistency unlocks achievements and builds habits

4. **Check Stats Regularly**: Track your progress to stay motivated

5. **Compete on Leaderboard**: Friendly competition with roommates/colleagues

6. **Match Music to Task**:
   - Creative work → Nebula, Drift
   - Technical work → Void, Cosmos
   - Energizing → Spiral

---

## 🔧 Troubleshooting

### Music Doesn't Open

**Issue**: Browser doesn't launch
**Solution**: Check that your system can run `webbrowser` module. Try manually opening URLs.

### Colors Look Wrong

**Issue**: Terminal doesn't support ANSI colors
**Solution**: Use a modern terminal (iTerm2, Windows Terminal, GNOME Terminal)

### Data Corrupted

**Issue**: JSON error on startup
**Solution**: The script auto-creates backups. Check `sovereign_data/` for backup files.

### Permission Error

**Issue**: Can't write to directory
**Solution**: Run with proper permissions or change DATA_DIR in code

---

## 📝 Changelog

### v2.1 GALAXY EDITION (Current)
- 🌌 Full galaxy visualization system
- 150+ animated stars across 3 parallax layers
- Nebula clouds with colorful gas effects
- Shooting stars and comets with tails
- Dynamic star spawning and twinkling
- Cosmic-themed progress bar
- Enhanced mission display with live stats
- Better visual depth and immersion

### v2.0
- Complete rewrite with OOP structure
- Added achievements and streaks
- Multiple session durations
- Enhanced statistics
- Better error handling
- Data export feature
- Settings menu
- 2 new music streams
- Expanded wisdom quotes

### v1.0 (Original)
- Basic Pomodoro timer
- XP and leveling system
- 3 music streams
- Simple leaderboard
- Mission history


![Version](https://img.shields.io/badge/version-2.1-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Stars](https://img.shields.io/github/stars/avsn17/sovereign-apex?style=social)
---

## 🙏 Credits

- **Music Streams**: YouTube (links in code)
- **Wisdom**: Avatar: The Last Airbender (Uncle Iroh)
- **Design Inspiration**: Retro terminal aesthetics

---

## 📄 License

Free to use, modify, and share. No warranty provided.

---

## 🤝 Contributing

Feel free to fork and improve! Some ideas:

- Add sound effects (requires external library)
- Desktop notifications
- Custom music playlist support
- Break reminders between sessions
- Task list integration
- Statistics charts (requires matplotlib)
- Mobile app version
- Multi-language support

---

## ❓ FAQ

**Q: Can I use this without internet?**
A: Yes, but music links won't work. The timer functions fully offline.

**Q: Does this sync between computers?**
A: No, data is local only. Use the export feature to transfer manually.

**Q: Can I compete with friends?**
A: Yes! If you share the same `sovereign_data/` folder (e.g., on a network drive).

**Q: Why "Sovereign Apex"?**
A: It sounds cool and space-themed. Feel free to rename!

**Q: Can I modify the XP formula?**
A: Yes! Edit the `add_xp()` method and `complete_mission()` calculations.

---

**Enjoy your focus sessions, Captain! 🚀**