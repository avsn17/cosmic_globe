import time
import os
import json
import random
import sys
import webbrowser
from datetime import datetime

# --- CONFIGURATION ---
DATA_FILE = "pilot_data.json"
STREAMS = {
    "1": ("Nightride FM", "https://stream.nightride.fm/nightride.mp3"),
    "2": ("Lana Del Rey Mix", "https://www.youtube.com/results?search_query=lana+del+rey+playlist"),
    "3": ("Cigarettes After Sex", "https://www.youtube.com/results?search_query=cigarettes+after+sex+playlist"),
    "4": ("Bee Gees / Disco", "https://www.youtube.com/results?search_query=bee+gees+essentials")
}

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

def draw_header(data):
    clear()
    print("\033[1;32m" + "="*65)
    print(f" CHRONOS_CLI v36.1 | PILOT: AVI | SESSIONS: {data.get('sessions', 0)}")
    print("="*65 + "\033[0m")

def start_music():
    print("\n\033[1;35m--- SELECT NEURAL STREAM ---")
    for key, val in STREAMS.items():
        print(f" {key}. {val[0]}")
    print(" 5. Back to HQ")
    
    choice = input("\nSTREAM_ID > ")
    if choice in STREAMS:
        print(f"\033[1;34m[SYSTEM] Linking to {STREAMS[choice][0]}...\033[0m")
        webbrowser.open(STREAMS[choice][1])
    elif choice == "5":
        return

def start_timer(data):
    duration = 25 * 60
    try:
        while duration > 0:
            draw_header(data)
            m, s = divmod(duration, 60)
            print(f"\n\n          \033[1;33m[ MISSION_ACTIVE ]\033[0m")
            print(f"\n             \033[1;97m{m:02d}:{s:02d}\033[0m")
            print(f"\n\n" + "-"*65)
            log_preview = data.get('log', '')[-50:].replace('\n', ' ')
            print(f" NEURAL_LOG: ...{log_preview}")
            print("-" * 65)
            print("\n \033[2m(Ctrl+C to PAUSE MISSION)\033[0m")
            time.sleep(1)
            duration -= 1
        
        data['sessions'] = data.get('sessions', 0) + 1
        data['minutes'] = data.get('minutes', 0) + 25
        save_data(data)
        print("\n\n\033[1;32m 🔔 MISSION COMPLETE. \033[0m")
        input("Press Enter...")
    except KeyboardInterrupt:
        pass

def main():
    data = load_data()
    while True:
        draw_header(data)
        print("\n 1. [ ENGAGE ]   - 25m Focus Warp")
        print(" 2. [ LOGBOOK ]  - Manual Logs")
        print(" 3. [ MUSIC ]    - Select Neural Stream")
        print(" 4. [ OBJECTS ]  - Manage Tasks")
        print(" 5. [ SHUTDOWN ] - Terminate Session")
        
        choice = input("\nSELECT_PROTOCOL > ")

        if choice == "1":
            start_timer(data)
        elif choice == "2":
            clear()
            print("--- LOGBOOK ---")
            print(data.get('log', ''))
            new = input("\nAdd Log (or Enter to go back): ")
            if new:
                ts = datetime.now().strftime('%Y-%m-%d %H:%M')
                data['log'] = data.get('log', '') + f"\n[{ts}] {new}"
                save_data(data)
        elif choice == "3":
            start_music()
        elif choice == "4":
            while True:
                clear()
                print("--- OBJECTIVES ---")
                for i, t in enumerate(data.get('tasks', [])):
                    print(f" {i+1}. [ ] {t}")
                cmd = input("\n(+) Add, (r) Remove, (b) Back: ")
                if cmd == "+":
                    t = input("Task: "); data.get('tasks', []).append(t); save_data(data)
                elif cmd == "r":
                    idx = int(input("Index: ")) - 1; data.get('tasks', []).pop(idx); save_data(data)
                elif cmd == "b": break
        elif choice == "5":
            break

if __name__ == "__main__":
    main()
