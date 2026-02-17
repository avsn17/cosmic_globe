import time, os, json, webbrowser, random, sys
from datetime import datetime

STREAMS = {
    "1": ("Coffee Dreams (2026 Lo-Fi)", "https://www.youtube.com/watch?v=sd2kAWVtOis"),
    "2": ("Lana Del Rey (Noir Hits)", "https://www.youtube.com/watch?v=OlXWoEvLig0"),
    "3": ("Cigarettes After Sex (Deep Focus)", "https://www.youtube.com/watch?v=3DhndiNT_4s"),
    "4": ("Bee Gees (Space Disco)", "https://www.youtube.com/watch?v=F2jTY0GZrds")
}

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f: return json.load(f)
    return {"sessions": 0, "xp": 0, "level": 1, "log": "", "history": []}

def save_data(pilot_id, data):
    with open(f"pilot_{pilot_id}.json", 'w') as f: json.dump(data, f, indent=4)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def get_rank(lvl):
    ranks = ["ROOKIE", "PILOT", "COMMANDER", "ACE", "SOVEREIGN"]
    return ranks[min(lvl-1, 4)]

def main():
    clear()
    print("\033[1;32m" + "═" * 60)
    print(" CHRONOS_SOVEREIGN v39.4 | CAPTAIN'S BRIDGE")
    print("═" * 60 + "\033[0m")
    
    pilot_id = input("\nENTER_CAPTAIN_ID > ").strip() or "AVI"
    data = load_data(pilot_id)
    
    print("\n\033[1;36m[COMMAND] SELECT NEURAL ATMOSPHERE:\033[0m")
    for k, v in STREAMS.items(): print(f"  {k}. {v[0]}")
    
    m_choice = input("\nATMOSPHERE_ID > ")
    selected_stream = STREAMS.get(m_choice, STREAMS["1"])
    webbrowser.open(selected_stream[1])
    
    goal = input("\n[GAMIFICATION] SET MISSION OBJECTIVE: ")

    while True:
        req = data['level'] * 300
        percent = int(((data['xp'] % req) / req) * 20)
        bar = "█" * percent + "░" * (20 - percent)
        
        clear()
        print(f"\033[1;32m═" * 60)
        print(f" CAPTAIN: {pilot_id} | LVL: {data['level']} | {get_rank(data['level'])}")
        print(f" {bar} {data['xp'] % req}/{req} XP")
        print("═" * 60 + "\033[0m")
        print(f"\n CURRENT_OBJECTIVE: \033[1;33m{goal}\033[0m")
        print(f" ATMOSPHERE: \033[1;36m{selected_stream[0]}\033[0m")
        
        print("\n 1. [ ENGAGE ]   2. [ LOGS ]   3. [ SWITCH_MUSIC ]   4. [ EXIT ]")
        
        choice = input("\nACTION > ")
        if choice == "1":
            duration = 25 * 60
            try:
                while duration > 0:
                    m, s = divmod(duration, 60)
                    sys.stdout.write(f"\r    \033[1;35mWARP ACTIVE: {m:02d}:{s:02d} | TASK: {goal}\033[0m")
                    sys.stdout.flush()
                    time.sleep(1)
                    duration -= 1
                data['xp'] += 100
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {goal}")
                save_data(pilot_id, data)
                print("\n\n\033[1;32m✔ MISSION COMPLETE. XP GAINED.\033[0m")
                input("Press Enter...")
            except KeyboardInterrupt: pass
        elif choice == "4": break
if __name__ == "__main__": main()
