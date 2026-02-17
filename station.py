import time, os, json, webbrowser, random, sys
from datetime import datetime

# --- CAPTAIN'S REFINED PLAYLIST ---
STREAMS = {
    "1": ("Lana Del Rey (Noir Hits)", "https://www.youtube.com/watch?v=OlXWoEvLig0"),
    "2": ("Cigarettes After Sex (Ethereal Focus)", "https://www.youtube.com/watch?v=3DhndiNT_4s"),
    "3": ("Bee Gees (Space Disco)", "https://www.youtube.com/watch?v=F2jTY0GZrds")
}

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    defaults = {"sessions": 0, "xp": 0, "level": 1, "history": []}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for k, v in defaults.items():
                if k not in data: data[k] = v
            return data
    return defaults

def save_data(pilot_id, data):
    with open(f"pilot_{pilot_id}.json", 'w') as f: json.dump(data, f, indent=4)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def star_warp(m, s, goal, lvl):
    """Dynamic Starfield Warp Experience"""
    # Color changes based on Level
    color = "\033[1;32m" if lvl < 5 else "\033[1;35m" 
    stars = ["+", "*", "°", "•", "✧", "★"]
    clear()
    print(f"{color}{' '*10}─── WARP DRIVE ENGAGED ───\033[0m")
    for _ in range(5):
        line = "".join(random.choice(stars) if random.random() > 0.96 else " " for _ in range(60))
        print(f"    {line}")
    print(f"\n\033[1;97m{' '*20}TIME: {m:02d}:{s:02d}\033[0m")
    print(f"\033[1;33m{' '*20}MISSION: {goal}\033[0m\n")
    for _ in range(5):
        line = "".join(random.choice(stars) if random.random() > 0.96 else " " for _ in range(60))
        print(f"    {line}")

def main():
    clear()
    print("\033[1;32m[ IDENTITY ]\033[0m Enter Captain ID:")
    pilot_id = input(">> ").strip() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print("\033[1;36m[ VIBE ]\033[0m Select Neural Atmosphere:")
    for k, v in STREAMS.items(): print(f" {k} > {v[0]}")
    m_choice = input(">> ")
    stream = STREAMS.get(m_choice, STREAMS["1"])
    webbrowser.open(stream[1])
    
    clear()
    print("\033[1;33m[ MISSION ]\033[0m Objective:")
    goal = input(">> ")

    while True:
        clear()
        lvl = data['level']
        req = lvl * 300
        prog = int(((data['xp'] % req) / req) * 20)
        bar = "█" * prog + "░" * (20 - prog)
        
        print(f"\033[1;32m╔═ CAPTAIN: {pilot_id} {'═'*30}╗")
        print(f"║ LVL: {lvl} | {bar} {data['xp']%req}/{req} XP ║")
        print(f"╚═{'═'*48}╝\033[0m")
        print(f"\n CURRENT MISSION: {goal}")
        print(f" ACTIVE ATMOSPHERE: {stream[0]}")
        print("\n COMMANDS: [1] START WARP | [2] NEW VIBE | [3] EXIT")
        
        cmd = input("\n>> ")
        if cmd == "1":
            duration = 25 * 60
            try:
                while duration > 0:
                    m, s = divmod(duration, 60)
                    star_warp(m, s, goal, lvl)
                    time.sleep(1)
                    duration -= 1
                data['xp'] += 100
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append(f"{datetime.now().strftime('%Y-%m-%d')} - {goal}")
                save_data(pilot_id, data)
                print("\n\033[1;32m✔ MISSION COMPLETE. 100 XP AWARDED.\033[0m")
                time.sleep(3)
            except KeyboardInterrupt: pass
        elif cmd == "2":
            clear()
            for k, v in STREAMS.items(): print(f" {k} > {v[0]}")
            m_choice = input("NEW VIBE >> ")
            if m_choice in STREAMS:
                stream = STREAMS[m_choice]
                webbrowser.open(stream[1])
        elif cmd == "3":
            save_data(pilot_id, data)
            break

if __name__ == "__main__": main()
