import time, os, json, webbrowser, random, sys
from datetime import datetime

# --- NEURAL ATMOSPHERES (The Trident Playlist) ---
STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/watch?v=OlXWoEvLig0", "NOIR", "\033[1;35m"),
    "2": ("Cigarettes After Sex", "https://www.youtube.com/watch?v=3DhndiNT_4s", "ETHEREAL", "\033[1;36m"),
    "3": ("Bee Gees", "https://www.youtube.com/watch?v=F2jTY0GZrds", "DISCO", "\033[1;33m")
}

IROH_QUOTES = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "While it is always best to believe in oneself, a little help from others can be a great blessing.",
    "Sharing tea with a stranger is a delight."
]

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    defaults = {"sessions": 0, "xp": 0, "level": 1, "history": [], "total_min": 0}
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

def get_flight_frame(vibe_type, color):
    width = 65
    chars = ["★", "✧", "»", "⚡", ">"] if vibe_type == "DISCO" else ["·", "°", "◌", "✧", " "]
    line = "".join(random.choice(chars) if random.random() > 0.93 else " " for _ in range(width))
    return f"{color}{line}\033[0m"

def main():
    clear()
    # SOVEREIGN LOGO & IDENTITY
    print("\033[1;32m")
    print("  ██████  ██████  ██    ██ ███████ ██████  ███████ ██  ██████  ███    ██ ")
    print(" ██      ██    ██ ██    ██ ██      ██   ██ ██      ██ ██       ████   ██ ")
    print("  █████  ██    ██ ██    ██ █████   ██████  █████   ██ ██   ███ ██ ██  ██ ")
    print("      ██ ██    ██  ██  ██  ██      ██   ██ ██      ██ ██    ██ ██  ██ ██ ")
    print(" ██████   ██████    ████   ███████ ██   ██ ███████ ██  ██████  ██   ████ ")
    print("\033[0m")
    
    pilot_id = input("\033[1;32m[ IDENTITY ]\033[0m ENTER CAPTAIN ID: ").strip().upper() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print("\033[1;36m[ ATMOSPHERE ]\033[0m SELECT NEURAL STREAM (AUTO-PLAYING):")
    for k, v in STREAMS.items(): 
        print(f" {v[3]}[{k}]\033[0m > {v[0]}")
    
    choice = input("\n>> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    webbrowser.open(stream_data[1]) # INSTANT MUSIC START
    
    clear()
    print(f"\033[1;33m[ MISSION ]\033[0m DEFINE OBJECTIVE FOR {pilot_id}:")
    goal = input(">> ")

    while True:
        clear()
        lvl, xp = data['level'], data['xp']
        req = lvl * 300
        bar_len = int(((xp % req) / req) * 20)
        bar = "\033[1;32m█\033[0m" * bar_len + "░" * (20 - bar_len)
        
        print(f"\033[1;32m╔═ CAPTAIN: {pilot_id} {'═'*35}╗")
        print(f"║ LVL: {lvl} | {bar} {xp%req}/{req} XP ║")
        print(f"╚═{'═'*53}╝\033[0m")
        print(f"\n MISSION: \033[1;33m{goal}\033[0m | VIBE: {stream_data[3]}{stream_data[0]}\033[0m")
        
        print("\n [1] ENGAGE_WARP  [2] CAREER_LOGS  [3] IROH_WISDOM  [4] EXIT")
        
        cmd = input("\n>> ")
        
        if cmd == "1": # THE ANIMATED EXPERIENCE
            duration = 25 * 60
            try:
                while duration > 0:
                    m, s = divmod(duration, 60)
                    clear()
                    print(f"{stream_data[3]}{'═'*20} {stream_data[2]}_FLIGHT_ACTIVE {'═'*20}\033[0m")
                    for _ in range(5): print(f"   {get_flight_frame(stream_data[2], stream_data[3])}")
                    print(f"\n{' '*23}\033[1;97mTIME: {m:02d}:{s:02d}\033[0m")
                    print(f"{' '*23}\033[1;33m{goal}\033[0m\n")
                    for _ in range(5): print(f"   {get_flight_frame(stream_data[2], stream_data[3])}")
                    time.sleep(1)
                    duration -= 1
                
                # REWARDS & LOGGING
                data['xp'] += 100
                data['total_min'] += 25
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append({"time": datetime.now().strftime('%Y-%m-%d %H:%M'), "task": goal})
                save_data(pilot_id, data)
                print("\n\033[1;32m✔ MISSION COMPLETE. DATA SYNCED TO LOG.\033[0m")
                time.sleep(3)
            except KeyboardInterrupt: pass

        elif cmd == "2": # HISTORY LOGS
            clear()
            print(f"\033[1;35m--- {pilot_id} CAREER HISTORY ---\033[0m")
            print(f"TOTAL FOCUS: {data['total_min']} MINS | RANK: LEVEL {data['level']}")
            for entry in data['history'][-10:]: print(f" [+] {entry['time']} - {entry['task']}")
            input("\n[ENTER TO RETURN]")

        elif cmd == "3": # IROH
            clear()
            print(f"\n\033[1;36mUncle Iroh: \"{random.choice(IROH_QUOTES)}\"\033[0m")
            input("\n[ENTER TO RETURN]")

        elif cmd == "4":
            save_data(pilot_id, data)
            break

if __name__ == "__main__": main()
