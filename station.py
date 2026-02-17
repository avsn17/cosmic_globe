import time, os, json, webbrowser, random, sys
from datetime import datetime

# --- CONFIGURATION & ASSETS ---
IROH_QUOTES = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Sharing tea with a stranger is a delight."
]

STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/results?search_query=lana+del+rey+playlist", "NOIR"),
    "2": ("Cigarettes After Sex", "https://www.youtube.com/results?search_query=cigarettes+after+sex+playlist", "ETHEREAL"),
    "3": ("Bee Gees", "https://www.youtube.com/results?search_query=bee+gees+disco+playlist", "DISCO")
}

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    defaults = {"sessions": 0, "xp": 0, "level": 1, "history": [], "log": ""}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
                for k, v in defaults.items():
                    if k not in data: data[k] = v
                return data
            except: return defaults
    return defaults

def save_data(pilot_id, data):
    with open(f"pilot_{pilot_id}.json", 'w') as f:
        json.dump(data, f, indent=4)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def get_flight_frame(vibe):
    width = 60
    if vibe == "NOIR":
        chars, color = ["·", " ", " ", "°"], "\033[1;34m"
    elif vibe == "ETHEREAL":
        chars, color = ["◌", " ", " ", " "], "\033[0;37m"
    else: # DISCO
        chars, color = ["★", "✧", " ", " ", "»", ">"], "\033[1;35m"
    line = "".join(random.choice(chars) if random.random() > 0.94 else " " for _ in range(width))
    return f"{color}{line}\033[0m"

def main():
    clear()
    print("\033[1;32m[ IDENTITY_LINK ]\033[0m Enter Captain ID:")
    pilot_id = input(">> ").strip() or "AVI"
    data = load_data(pilot_id)
    
    # 1. CAPTAIN SELECTS MUSIC (Autoplay)
    clear()
    print("\033[1;36m[ ATMOSPHERE ]\033[0m Select Neural Atmosphere:")
    for k, v in STREAMS.items(): print(f" {k} > {v[0]}")
    choice = input(">> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    webbrowser.open(stream_data[1])
    
    # 2. MISSION OBJECTIVE (Gamification)
    clear()
    print("\033[1;33m[ MISSION_CONTROL ]\033[0m What is the objective for this session?")
    goal = input(">> ")

    while True:
        clear()
        lvl = data['level']
        req = lvl * 300
        prog = int(((data['xp'] % req) / req) * 20)
        bar = "█" * prog + "░" * (20 - prog)
        
        print(f"\033[1;32m╔═ CAPTAIN: {pilot_id} {'═'*31}╗")
        print(f"║ LVL: {lvl} | {bar} {data['xp']%req}/{req} XP ║")
        print(f"╚═{'═'*49}╝\033[0m")
        print(f"\n CURRENT MISSION: {goal}")
        print(f" ACTIVE VIBE: {stream_data[0]}")
        print(f"\n COMMANDS: [1] ENGAGE_WARP | [2] IROH_WISDOM | [3] FLIGHT_LOGS | [4] EXIT")
        
        cmd = input("\n>> ")
        
        if cmd == "1": # THE ANIMATED EXPERIENCE
            duration = 25 * 60
            try:
                while duration > 0:
                    m, s = divmod(duration, 60)
                    clear()
                    print(f"\033[1;32m{'═'*15} FLIGHT_ACTIVE: {stream_data[2]} {'═'*15}\033[0m")
                    for _ in range(4): print(f"    {get_flight_frame(stream_data[2])}")
                    print(f"\n{' '*18}\033[1;97mTIME: {m:02d}:{s:02d}\033[0m")
                    print(f"{' '*18}\033[1;33mGOAL: {goal}\033[0m\n")
                    for _ in range(4): print(f"    {get_flight_frame(stream_data[2])}")
                    time.sleep(1)
                    duration -= 1
                
                # AUTO-SAVE & XP GAIN
                data['xp'] += 100
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {goal}")
                save_data(pilot_id, data)
                print("\n\033[1;32m✔ MISSION COMPLETE. 100 XP RECORDED.\033[0m")
                time.sleep(3)
            except KeyboardInterrupt: pass

        elif cmd == "2": # IROH CHAT
            clear()
            print(f"\n\033[1;36mUncle Iroh: \"{random.choice(IROH_QUOTES)}\"\033[0m")
            input("\nPress Enter to return to bridge...")

        elif cmd == "3": # HISTORY LOGS
            clear()
            print(f"--- {pilot_id} FLIGHT HISTORY ---")
            for entry in data['history'][-10:]: print(f" [+] {entry}")
            input("\nPress Enter...")

        elif cmd == "4":
            save_data(pilot_id, data)
            break

if __name__ == "__main__": main()
