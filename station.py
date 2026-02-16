import time
import os
import json
import random
import sys
import webbrowser
import threading
from datetime import datetime

# --- CONFIGURATION ---
DATA_FILE = "pilot_data.json"
MUSIC_URL = "https://stream.nightride.fm/nightride.mp3"
IROH_QUOTES = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "Sharing tea with a fascinating stranger is one of life’s true delights.",
    "While it is always best to believe in oneself, a little help from others can be a great blessing."
]

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"sessions": 0, "minutes": 0, "tasks": [], "log": "", "history": []}
    return {"sessions": 0, "minutes": 0, "tasks": [], "log": "", "history": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_sfx():
    sys.stdout.write('\a')
    sys.stdout.flush()

def draw_sparkles():
    # Simulated ASCII Sparkle Field
    chars = [".", "*", " ", "'", "°", "+"]
    return "".join(random.choice(chars) for _ in range(60))

def draw_header(data):
    clear()
    print("\033[1;32m" + "="*65)
    print(f" CHRONOS_CLI v34.0 | NEBULA_X SYSTEM | SESSIONS: {data.get('sessions', 0)}")
    print(draw_sparkles())
    print("="*65 + "\033[0m")

def start_music():
    print("\033[1;34m[SYSTEM] Booting Neural Music Stream...\033[0m")
    # This opens the stream in the background via the default browser or player
    webbrowser.open(MUSIC_URL)

def start_timer(data):
    duration = 25 * 60
    play_sfx()
    try:
        while duration > 0:
            draw_header(data)
            m, s = divmod(duration, 60)
            print(f"\n\n          \033[1;33m[ MISSION_ACTIVE ]\033[0m")
            print(f"\n             \033[1;97m{m:02d}:{s:02d}\033[0m")
            print(f"\n       {draw_sparkles()}")
            print(f"\n\n" + "-"*65)
            log_preview = data.get('log', '')[-50:].replace('\n', ' ')
            print(f" NEURAL_LOG: ...{log_preview}")
            print("-" * 65)
            print("\n \033[2m(Ctrl+C to PAUSE/HOLD POSITION)\033[0m")
            time.sleep(1)
            duration -= 1
        
        play_sfx()
        data['sessions'] = data.get('sessions', 0) + 1
        data['minutes'] = data.get('minutes', 0) + 25
        # Save timestamped history
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        if 'history' not in data: data['history'] = []
        data['history'].append(timestamp)
        save_data(data)
        print("\n\n\033[1;32m 🔔 MISSION COMPLETE. DATA SYNCED. \033[0m")
        input("Press Enter to return...")
    except KeyboardInterrupt:
        print("\n\n\033[1;31m MISSION_PAUSED. Returning to Command. \033[0m")
        time.sleep(1)

def main():
    data = load_data()
    while True:
        draw_header(data)
        print("\n \033[1m1. [ ENGAGE ]\033[0m   - Launch 25m Focus Warp")
        print(" \033[1m2. [ LOGBOOK ]\033[0m  - Write Neural Patterns (Manual Log)")
        print(" \033[1m3. [ OBJECTS ]\033[0m  - Tactical Objectives (Tasks)")
        print(" \033[1m4. [ MUSIC ]\033[0m    - Start Neural Music Stream")
        print(" \033[1m5. [ HISTORY ]\033[0m  - View Mission Flight Logs")
        print(" \033[1m6. [ IROH ]\033[0m     - Consult Neural Link")
        print(" \033[1m7. [ SYNC ]\033[0m     - Manual JSON Export Info")
        print(" \033[1m8. [ EXIT ]\033[0m     - Shutdown Terminal")
        
        choice = input("\nSELECT_PROTOCOL > ")

        if choice == "1":
            start_timer(data)
        elif choice == "2":
            clear()
            print("\033[1;32m--- MANUAL_LOGBOOK ---\033[0m")
            print(data.get('log', 'Empty.'))
            cmd = input("\n(a) Add Entry, (c) Clear, (b) Back: ")
            if cmd == "a":
                entry = input("Log Content: ")
                ts = datetime.now().strftime('%Y-%m-%d %H:%M')
                data['log'] = data.get('log', '') + f"\n[{ts}] {entry}"
                save_data(data)
            elif cmd == "c": data['log'] = ""; save_data(data)
        elif choice == "3":
            while True:
                clear()
                print("\033[1;32m--- OBJECTIVES ---\033[0m")
                for i, t in enumerate(data.get('tasks', [])):
                    print(f" {i+1}. [ ] {t}")
                cmd = input("\n(+) Add, (r) Remove, (b) Back: ")
                if cmd == "+":
                    t = input("Task: "); data.get('tasks', []).append(t); save_data(data)
                elif cmd == "r":
                    idx = int(input("Index: ")) - 1; data.get('tasks', []).pop(idx); save_data(data)
                elif cmd == "b": break
        elif choice == "4":
            start_music()
        elif choice == "5":
            clear()
            print("\033[1;32m--- MISSION_HISTORY ---\033[0m")
            for h in data.get('history', []):
                print(f" [+] COMPLETED: {h}")
            input("\nPress Enter...")
        elif choice == "6":
            clear()
            print(f"\n\033[1;36mIroh: \"{random.choice(IROH_QUOTES)}\"\033[0m")
            input("\nPress Enter...")
        elif choice == "7":
            clear()
            print(f"FILE_LOCATION: {os.path.abspath(DATA_FILE)}")
            print("Use the 'UPLOAD' button on the Website to sync this file.")
            input("\nPress Enter...")
        elif choice == "8":
            break

if __name__ == "__main__":
    main()
# Add these options to your main() loop in station.py

def music_menu():
    print("\n\033[1;35m--- SELECT NEURAL STREAM ---")
    print("1. Nightride FM (Synthwave)")
    print("2. Lana Del Rey (Cozy/Noir)")
    print("3. Cigarettes After Sex (Slowcore)")
    print("4. Bee Gees (Space Disco)")
    print("5. Back to Menu")
    
    choice = input("\nSTREAM_ID > ")
    streams = {
        "1": "https://stream.nightride.fm/nightride.mp3",
        "2": "https://www.youtube.com/results?search_query=lana+del+rey+mix",
        "3": "https://www.youtube.com/results?search_query=cigarettes+after+sex+mix",
        "4": "https://www.youtube.com/results?search_query=bee+gees+mix"
    }
    if choice in streams:
        webbrowser.open(streams[choice])