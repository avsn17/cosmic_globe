#!/usr/bin/env python3
"""
SOVEREIGN APEX - Enhanced Focus Timer & Progress Tracker
Version 2.0 | 2026-02-17
"""

import time
import os
import json
import webbrowser
import random
import sys
import glob
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# === CONFIGURATION ===
DATA_DIR = Path("sovereign_data")
DATA_DIR.mkdir(exist_ok=True)

# === THEME & COLORS ===
class Colors:
    PINK = "\033[1;95m"
    YELLOW = "\033[1;93m"
    BLUE = "\033[1;94m"
    GREEN = "\033[1;32m"
    CYAN = "\033[1;36m"
    WHITE = "\033[1;97m"
    RED = "\033[1;91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

C = Colors()

# === STREAM LIBRARY ===
STREAMS = {
    "1": {
        "artist": "Lana Del Rey",
        "url": "https://www.youtube.com/watch?v=OlXWoEvLig0",
        "name": "NEBULA",
        "color": C.PINK
    },
    "2": {
        "artist": "Cigarettes After Sex",
        "url": "https://www.youtube.com/watch?v=3DhndiNT_4s",
        "name": "VOID",
        "color": C.CYAN
    },
    "3": {
        "artist": "Bee Gees",
        "url": "https://www.youtube.com/watch?v=F2jY0GZrds",
        "name": "SPIRAL",
        "color": C.YELLOW
    },
    "4": {
        "artist": "Lofi Hip Hop",
        "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk",
        "name": "DRIFT",
        "color": C.BLUE
    },
    "5": {
        "artist": "Ambient Space",
        "url": "https://www.youtube.com/watch?v=1-RW3nUDTTc",
        "name": "COSMOS",
        "color": C.GREEN
    }
}

# === WISDOM QUOTES ===
WISDOM = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "Good tea is its own reward.",
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Sometimes the best way to solve your own problems is to help someone else.",
    "It is important to draw wisdom from many different places. If we take it from only one place, it becomes rigid and stale.",
    "Pride is not the opposite of shame, but its source. True humility is the only antidote to shame.",
    "Failure is only the opportunity to begin again. Only this time, more wisely."
]

# === DATA MANAGEMENT ===
class PilotData:
    """Handles pilot data persistence and operations"""
    
    def __init__(self, pilot_id: str):
        self.pilot_id = pilot_id
        self.filepath = DATA_DIR / f"pilot_{pilot_id}.json"
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load pilot data from file"""
        defaults = {
            "xp": 0,
            "level": 1,
            "history": [],
            "total_minutes": 0,
            "total_sessions": 0,
            "streak_days": 0,
            "last_session": None,
            "achievements": [],
            "preferred_duration": 25
        }
        
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r') as f:
                    loaded = json.load(f)
                    return {**defaults, **loaded}
            except json.JSONDecodeError:
                print(f"{C.RED}⚠ Corrupted data file. Creating backup...{C.RESET}")
                self._backup()
                return defaults
        return defaults
    
    def _backup(self):
        """Create backup of corrupted file"""
        if self.filepath.exists():
            backup_path = DATA_DIR / f"pilot_{self.pilot_id}_backup_{int(time.time())}.json"
            self.filepath.rename(backup_path)
    
    def save(self):
        """Save pilot data to file"""
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def add_xp(self, amount: int):
        """Add XP and handle level ups"""
        self.data['xp'] += amount
        xp_needed = self.data['level'] * 300
        
        if self.data['xp'] >= xp_needed:
            self.data['level'] += 1
            return True  # Leveled up
        return False
    
    def complete_session(self, duration_min: int, goal: str, rank: int):
        """Record completed session"""
        session_id = str(uuid.uuid4())[:8]
        
        entry = {
            "id": session_id,
            "timestamp": datetime.now().isoformat(),
            "duration": duration_min,
            "goal": goal,
            "rank": rank
        }
        
        self.data['history'].append(entry)
        self.data['total_minutes'] += duration_min
        self.data['total_sessions'] += 1
        self.data['last_session'] = datetime.now().isoformat()
        
        # Update streak
        self._update_streak()
        
        # Check achievements
        self._check_achievements()
        
        self.save()
        return session_id
    
    def _update_streak(self):
        """Update daily streak counter"""
        if self.data['last_session']:
            last = datetime.fromisoformat(self.data['last_session'])
            now = datetime.now()
            days_diff = (now.date() - last.date()).days
            
            if days_diff == 0:
                pass  # Same day
            elif days_diff == 1:
                self.data['streak_days'] += 1
            else:
                self.data['streak_days'] = 1
        else:
            self.data['streak_days'] = 1
    
    def _check_achievements(self):
        """Check and unlock achievements"""
        achievements = []
        
        if self.data['total_sessions'] == 1:
            achievements.append("First Mission")
        if self.data['total_sessions'] == 10:
            achievements.append("Veteran Pilot")
        if self.data['total_sessions'] == 50:
            achievements.append("Mission Master")
        if self.data['total_minutes'] >= 1000:
            achievements.append("Millennium Flight")
        if self.data['streak_days'] >= 7:
            achievements.append("Week Warrior")
        if self.data['level'] >= 10:
            achievements.append("Elite Captain")
        
        for ach in achievements:
            if ach not in self.data['achievements']:
                self.data['achievements'].append(ach)
                print(f"\n{C.YELLOW}★ ACHIEVEMENT UNLOCKED: {ach}!{C.RESET}")
                time.sleep(2)

# === LEADERBOARD ===
class Leaderboard:
    """Manages fleet-wide rankings"""
    
    @staticmethod
    def get_rankings() -> List[Dict]:
        """Get sorted leaderboard"""
        files = glob.glob(str(DATA_DIR / "pilot_*.json"))
        ranks = []
        
        for filepath in files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    pilot_id = Path(filepath).stem.replace("pilot_", "")
                    
                    ranks.append({
                        "id": pilot_id,
                        "level": data.get("level", 1),
                        "xp": data.get("xp", 0),
                        "total_minutes": data.get("total_minutes", 0),
                        "sessions": data.get("total_sessions", 0),
                        "streak": data.get("streak_days", 0)
                    })
            except (json.JSONDecodeError, KeyError):
                continue
        
        return sorted(ranks, key=lambda x: (x['level'], x['xp']), reverse=True)
    
    @staticmethod
    def get_rank(pilot_id: str) -> int:
        """Get pilot's current rank"""
        rankings = Leaderboard.get_rankings()
        for i, pilot in enumerate(rankings, 1):
            if pilot['id'] == pilot_id:
                return i
        return 0

# === ACTIVITY LOG ===
class ActivityLog:
    """Global fleet activity logger"""
    
    LOG_FILE = DATA_DIR / "fleet_activity.log"
    
    @staticmethod
    def write(message: str):
        """Write entry to activity log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(ActivityLog.LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")

# === VISUAL EFFECTS ===
class VisualEffects:
    """Terminal visual effects and animations"""
    
    @staticmethod
    def clear():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def generate_parallax_line(width: int = 110) -> str:
        """Generate animated starfield line"""
        line = [" "] * width
        
        # Dots
        if random.random() < 0.08:
            line[random.randint(0, width-1)] = f"{C.WHITE}·{C.RESET}"
        
        # Stars
        if random.random() < 0.05:
            char = random.choice([f"{C.YELLOW}★{C.RESET}", f"{C.BLUE}◌{C.RESET}"])
            line[random.randint(0, width-1)] = char
        
        # Special elements
        if random.random() < 0.03:
            char = random.choice([f"{C.PINK}✦{C.RESET}", f"{C.BLUE}●{C.RESET}"])
            line[random.randint(0, width-1)] = char
        
        return "".join(line)
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 45) -> str:
        """Generate progress bar"""
        progress = int((current / total) * width) if total > 0 else 0
        filled = f"{C.GREEN}█{C.RESET}" * progress
        empty = f"{C.WHITE}░{C.RESET}" * (width - progress)
        return filled + empty

# === MAIN APPLICATION ===
class SovereignApex:
    """Main application controller"""
    
    def __init__(self):
        self.pilot_data = None
        self.current_stream = None
        self.current_goal = ""
    
    def run(self):
        """Main application loop"""
        self.login()
        self.select_stream()
        self.set_goal()
        self.main_menu()
    
    def login(self):
        """Pilot authentication"""
        VisualEffects.clear()
        print(f"{C.GREEN}╔═══════════════════════════════════════════════════════════════╗")
        print(f"║  SOVEREIGN APEX v2.0 | ENHANCED FOCUS SYSTEM                 ║")
        print(f"║  LOGGED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                   ║")
        print(f"╚═══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        pilot_id = input(f"\n{C.GREEN}[ IDENTITY ]{C.RESET} LOGIN ID: ").strip().upper()
        if not pilot_id:
            pilot_id = "AVI"
        
        self.pilot_data = PilotData(pilot_id)
        
        # Welcome back message
        if self.pilot_data.data['total_sessions'] > 0:
            print(f"\n{C.CYAN}Welcome back, Captain {pilot_id}!{C.RESET}")
            print(f"Last session: {self.pilot_data.data.get('last_session', 'Never')[:10]}")
            time.sleep(1.5)
    
    def select_stream(self):
        """Audio stream selection"""
        VisualEffects.clear()
        print(f"{C.CYAN}╔═ ATMOSPHERE SELECTION ═══════════════════════════════════════╗{C.RESET}")
        
        for key, stream in STREAMS.items():
            print(f" {stream['color']}[{key}]{C.RESET} > {stream['artist']:<30} ({stream['name']})")
        
        print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        choice = input("\n>> ").strip()
        self.current_stream = STREAMS.get(choice, STREAMS["1"])
        
        print(f"\n{C.GREEN}▶ Opening {self.current_stream['name']}...{C.RESET}")
        try:
            webbrowser.open(self.current_stream['url'])
        except Exception as e:
            print(f"{C.RED}⚠ Could not open browser: {e}{C.RESET}")
        
        time.sleep(2)
    
    def set_goal(self):
        """Mission goal setting"""
        VisualEffects.clear()
        print(f"{C.YELLOW}╔═ MISSION BRIEFING ═══════════════════════════════════════════╗{C.RESET}")
        self.current_goal = input(f"\n{C.YELLOW}[ OBJECTIVE ]{C.RESET} What will you accomplish? ").strip()
        
        if not self.current_goal:
            self.current_goal = "Deep Work Session"
    
    def main_menu(self):
        """Main command menu"""
        while True:
            VisualEffects.clear()
            
            # Header with stats
            level = self.pilot_data.data['level']
            xp = self.pilot_data.data['xp']
            xp_needed = level * 300
            xp_current = xp % xp_needed
            
            bar = VisualEffects.progress_bar(xp_current, xp_needed)
            
            print(f"{C.GREEN}╔═ CAPTAIN: {self.pilot_data.pilot_id} ═════════════════════════════════════════════════════╗")
            print(f"║ LEVEL: {level:<3} | {bar} {xp_current}/{xp_needed} XP")
            print(f"║ SESSIONS: {self.pilot_data.data['total_sessions']:<4} | TOTAL TIME: {self.pilot_data.data['total_minutes']} min | STREAK: {self.pilot_data.data['streak_days']} days")
            print(f"╚═══════════════════════════════════════════════════════════════════════════════╝{C.RESET}")
            
            # Menu options
            print(f"\n{C.CYAN}COMMANDS:{C.RESET}")
            print(f" [1] 🚀 LAUNCH MISSION (Focus Session)")
            print(f" [2] 📊 VIEW STATISTICS")
            print(f" [3] 📜 MISSION HISTORY")
            print(f" [4] 🏆 LEADERBOARD")
            print(f" [5] 💭 WISDOM")
            print(f" [6] ⚙️  SETTINGS")
            print(f" [7] 🔊 CHANGE STREAM")
            print(f" [0] 🚪 EXIT")
            
            cmd = input(f"\n{C.WHITE}>> {C.RESET}").strip()
            
            if cmd == "1":
                self.launch_mission()
            elif cmd == "2":
                self.view_statistics()
            elif cmd == "3":
                self.view_history()
            elif cmd == "4":
                self.view_leaderboard()
            elif cmd == "5":
                self.show_wisdom()
            elif cmd == "6":
                self.settings()
            elif cmd == "7":
                self.select_stream()
            elif cmd == "0":
                self.exit_app()
                break
            else:
                print(f"{C.RED}Invalid command{C.RESET}")
                time.sleep(1)
    
    def launch_mission(self):
        """Start focus session"""
        VisualEffects.clear()
        
        # Duration selection
        print(f"{C.YELLOW}[ DURATION ]{C.RESET}")
        print(" [1] Quick Sprint (15 min)")
        print(" [2] Standard Mission (25 min)")
        print(" [3] Deep Dive (45 min)")
        print(" [4] Ultra Focus (60 min)")
        print(" [C] Custom")
        
        dur_choice = input("\n>> ").strip().lower()
        
        duration_map = {"1": 15, "2": 25, "3": 45, "4": 60}
        
        if dur_choice == "c":
            try:
                duration = int(input("Custom duration (minutes): "))
            except ValueError:
                duration = 25
        else:
            duration = duration_map.get(dur_choice, 25)
        
        session_id = str(uuid.uuid4())[:8]
        total_seconds = duration * 60
        
        # Initialize starfield
        field = [VisualEffects.generate_parallax_line() for _ in range(25)]
        
        try:
            remaining = total_seconds
            
            while remaining > 0:
                minutes, seconds = divmod(int(remaining), 60)
                
                VisualEffects.clear()
                
                # Header
                print(f"{C.WHITE}{'═'*30} MISSION: {session_id} | {self.current_stream['name']} {'═'*30}{C.RESET}")
                
                # Animated starfield
                field.pop(0)
                field.append(VisualEffects.generate_parallax_line())
                
                for i, line in enumerate(field):
                    if i == 11:
                        print(f"  {line[:45]}  {C.WHITE}{minutes:02d}:{seconds:02d}{C.RESET}  {line[55:]}")
                    elif i == 12:
                        goal_display = self.current_goal[:12].center(12)
                        print(f"  {line[:45]}  {C.YELLOW}{goal_display}{C.RESET}  {line[55:]}")
                    else:
                        print(f"  {line}")
                
                # Progress indicator
                progress_pct = ((total_seconds - remaining) / total_seconds) * 100
                print(f"\n{C.GREEN}{'▓' * int(progress_pct / 2)}{C.RESET}", end="")
                print(f" {progress_pct:.1f}%")
                
                time.sleep(0.3)
                remaining -= 0.3
            
            # Mission complete
            self.complete_mission(duration, session_id)
            
        except KeyboardInterrupt:
            print(f"\n\n{C.RED}Mission aborted.{C.RESET}")
            time.sleep(2)
    
    def complete_mission(self, duration: int, session_id: str):
        """Handle mission completion"""
        rank = Leaderboard.get_rank(self.pilot_data.pilot_id)
        
        # Record session
        self.pilot_data.complete_session(duration, self.current_goal, rank)
        
        # Award XP
        xp_gained = duration * 4  # 4 XP per minute
        leveled_up = self.pilot_data.add_xp(xp_gained)
        
        # Log activity
        ActivityLog.write(f"PILOT {self.pilot_data.pilot_id} completed mission {session_id} | Rank: {rank}")
        
        # Display completion
        VisualEffects.clear()
        print(f"\n{C.GREEN}{'═'*70}")
        print(f"  ✓ MISSION COMPLETE")
        print(f"{'═'*70}{C.RESET}")
        print(f"\n{C.YELLOW}+{xp_gained} XP{C.RESET} | Duration: {duration} min | Rank: #{rank}")
        
        if leveled_up:
            print(f"\n{C.PINK}★★★ LEVEL UP! NOW LEVEL {self.pilot_data.data['level']} ★★★{C.RESET}")
        
        # Re-trigger music
        print(f"\n{C.CYAN}♪ Re-opening stream...{C.RESET}")
        try:
            webbrowser.open(self.current_stream['url'])
        except:
            pass
        
        input(f"\n{C.WHITE}Press ENTER to continue{C.RESET}")
    
    def view_statistics(self):
        """Display pilot statistics"""
        VisualEffects.clear()
        data = self.pilot_data.data
        
        print(f"{C.PINK}╔═ PILOT STATISTICS ═══════════════════════════════════════════╗{C.RESET}")
        print(f"\n  Total Sessions:    {data['total_sessions']}")
        print(f"  Total Time:        {data['total_minutes']} minutes ({data['total_minutes']/60:.1f} hours)")
        print(f"  Current Level:     {data['level']}")
        print(f"  Total XP:          {data['xp']}")
        print(f"  Current Streak:    {data['streak_days']} days")
        
        if data['achievements']:
            print(f"\n  🏆 Achievements:")
            for ach in data['achievements']:
                print(f"     • {ach}")
        
        avg_session = data['total_minutes'] / data['total_sessions'] if data['total_sessions'] > 0 else 0
        print(f"\n  Average Session:   {avg_session:.1f} minutes")
        
        print(f"\n{C.PINK}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        input(f"\n{C.WHITE}Press ENTER to continue{C.RESET}")
    
    def view_history(self):
        """Display mission history"""
        VisualEffects.clear()
        history = self.pilot_data.data['history'][-15:]  # Last 15 sessions
        
        print(f"{C.PINK}╔═ MISSION HISTORY ════════════════════════════════════════════╗{C.RESET}")
        
        if not history:
            print("\n  No missions completed yet.")
        else:
            for entry in reversed(history):
                timestamp = entry['timestamp'][:16].replace('T', ' ')
                print(f"\n  [{timestamp}] ID:{entry['id']} | Rank:#{entry.get('rank', '?')}")
                print(f"  ├─ Duration: {entry.get('duration', 25)} min")
                print(f"  └─ Goal: {C.YELLOW}{entry['goal'][:40]}{C.RESET}")
        
        print(f"\n{C.PINK}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        input(f"\n{C.WHITE}Press ENTER to continue{C.RESET}")
    
    def view_leaderboard(self):
        """Display fleet leaderboard"""
        VisualEffects.clear()
        rankings = Leaderboard.get_rankings()
        
        print(f"{C.YELLOW}╔═ FLEET LEADERBOARD ══════════════════════════════════════════╗{C.RESET}")
        print(f"\n  {'RANK':<6} {'PILOT':<15} {'LEVEL':<8} {'XP':<10} {'SESSIONS':<10}")
        print(f"  {'-'*60}")
        
        for i, pilot in enumerate(rankings[:15], 1):
            marker = f"{C.GREEN}►{C.RESET}" if pilot['id'] == self.pilot_data.pilot_id else " "
            print(f"  {marker} {i:<4} {pilot['id']:<15} {pilot['level']:<8} {pilot['xp']:<10} {pilot['sessions']:<10}")
        
        print(f"\n{C.YELLOW}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        input(f"\n{C.WHITE}Press ENTER to continue{C.RESET}")
    
    def show_wisdom(self):
        """Display random wisdom quote"""
        VisualEffects.clear()
        quote = random.choice(WISDOM)
        
        print(f"\n{C.CYAN}╔═ WISDOM ═════════════════════════════════════════════════════╗")
        print(f"║                                                              ║")
        print(f"║  Uncle Iroh:                                                 ║")
        print(f"║  \"{quote[:56]}\"")
        if len(quote) > 56:
            remaining = quote[56:]
            while remaining:
                print(f"║  \"{remaining[:56]}\"")
                remaining = remaining[56:]
        print(f"║                                                              ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        input(f"\n{C.WHITE}Press ENTER to continue{C.RESET}")
    
    def settings(self):
        """Application settings"""
        VisualEffects.clear()
        print(f"{C.CYAN}╔═ SETTINGS ═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"\n  [1] Set default session duration")
        print(f"  [2] Reset progress (dangerous!)")
        print(f"  [3] Export data")
        print(f"  [0] Back")
        
        choice = input(f"\n>> ").strip()
        
        if choice == "1":
            try:
                duration = int(input("Default duration (minutes): "))
                self.pilot_data.data['preferred_duration'] = duration
                self.pilot_data.save()
                print(f"{C.GREEN}✓ Saved{C.RESET}")
            except ValueError:
                print(f"{C.RED}Invalid input{C.RESET}")
            time.sleep(1)
        
        elif choice == "2":
            confirm = input(f"{C.RED}Type 'RESET' to confirm: {C.RESET}").strip()
            if confirm == "RESET":
                self.pilot_data.filepath.unlink()
                print(f"{C.GREEN}✓ Progress reset{C.RESET}")
                time.sleep(2)
                sys.exit(0)
        
        elif choice == "3":
            export_path = DATA_DIR / f"export_{self.pilot_data.pilot_id}_{int(time.time())}.json"
            with open(export_path, 'w') as f:
                json.dump(self.pilot_data.data, f, indent=4)
            print(f"{C.GREEN}✓ Exported to {export_path}{C.RESET}")
            time.sleep(2)
    
    def exit_app(self):
        """Clean exit"""
        self.pilot_data.save()
        VisualEffects.clear()
        print(f"\n{C.GREEN}Flight systems powered down. Safe travels, Captain.{C.RESET}\n")
        time.sleep(1)

# === ENTRY POINT ===
def main():
    try:
        app = SovereignApex()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}Emergency shutdown initiated.{C.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.RED}Critical error: {e}{C.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()