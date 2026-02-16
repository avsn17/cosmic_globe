import time
import os
import json
import random
import sys
from datetime import datetime

# --- KONFIGURATION ---
DATA_FILE = "pilot_data.json"
IROH_QUOTES = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "It is important to draw wisdom from many different places.",
    "Sharing tea with a fascinating stranger is one of life’s true delights."
]

def play_alarm():
    # Erzeugt einen System-Beep (funktioniert auf den meisten Terminals)
    for _ in range(3):
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(0.5)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"sessions": 0, "minutes": 0, "tasks": [], "log": ""}
    return {"sessions": 0, "minutes": 0, "tasks": [], "log": ""}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header(data):
    clear()
    print("\033[1;32m" + "="*65)
    print(f" CHRONOS_TERMINAL v31.1 | PILOT: AVI | SESSIONS: {data.get('sessions', 0)}")
    print("="*65 + "\033[0m")

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
            print(f" LAST_LOG: ...{log_preview}")
            print("-"*65)
            print("\n \033[2m(Press Ctrl+C to PAUSE/EXIT MISSION)\033[0m")
            time.sleep(1)
            duration -= 1
        
        play_alarm()
        data['sessions'] = data.get('sessions', 0) + 1
        data['minutes'] = data.get('minutes', 0) + 25
        save_data(data)
        print("\n\n\033[1;32m 🔔 MISSION_COMPLETE! Audio Signal Sent. \033[0m")
        input("Press Enter to return to Command...")
    except KeyboardInterrupt:
        print("\n\n\033[1;31m MISSION_PAUSED. Returning to HQ... \033[0m")
        time.sleep(1)

def main():
    data = load_data()
    while True:
        draw_header(data)
        print("\n 1. [ ENGAGE ]   - Start Focus Mission (25m)")
        print(" 2. [ LOGBOOK ]  - Access Manual Pilot Logs")
        print(" 3. [ OBJECTS ]  - Manage Mission Objectives")
        print(" 4. [ NEURAL ]   - Consult Iroh Neural Link")
        print(" 5. [ SHUTDOWN ] - Terminate Terminal Session")
        
        choice = input("\nSELECT_PROTOCOL > ")

        if choice == "1":
            start_timer(data)
        elif choice == "2":
            clear()
            print("\033[1;32m--- MISSION_LOGBOOK ---\033[0m")
            print(data.get('log', 'No entries yet.'))
            print("\n" + "="*40)
            print("Commands: (a) Add Entry, (c) Clear Logs, (b) Back")
            cmd = input("> ")
            if cmd == "a":
                new_log = input("Log Entry: ")
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                data['log'] = data.get('log', '') + f"\n[{timestamp}] {new_log}"
                save_data(data)
            elif cmd == "c":
                if input("Are you sure? (y/n): ") == "y":
                    data['log'] = ""
                    save_data(data)
        elif choice == "3":
            while True:
                clear()
                print("\033[1;32m--- ACTIVE_OBJECTIVES ---\033[0m")
                tasks = data.get('tasks', [])
                for i, t in enumerate(tasks):
                    print(f" {i+1}. [ ] {t}")
                if not tasks: print(" No active objectives.")
                cmd = input("\n(+) Add, (r) Remove, (b) Back: ")
                if cmd == "+":
                    t = input("Objective Name: ")
                    if 'tasks' not in data: data['tasks'] = []
                    data['tasks'].append(t)
                    save_data(data)
                elif cmd == "r" and tasks:
                    try:
                        idx = int(input("Remove Index: ")) - 1
                        data['tasks'].pop(idx)
                        save_data(data)
                    except: pass
                elif cmd == "b":
                    break
        elif choice == "4":
            clear()
            print(f"\n\033[1;36m[ NEURAL_LINK_ESTABLISHED ]\033[0m\n")
            print(f"Uncle Iroh: \"{random.choice(IROH_QUOTES)}\"")
            input("\n\nPress Enter to disconnect...")
        elif choice == "5":
            print("\033[1;31mTerminating Link... Goodbye, Pilot.\033[0m")
            break

if __name__ == "__main__":
    main()
