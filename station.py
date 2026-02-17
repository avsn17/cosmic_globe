import time, os, json, webbrowser, random, sys
from datetime import datetime

# --- ASSETS ---
STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/watch?v=OlXWoEvLig0", "NOIR", "\033[1;35m"),
    "2": ("Cigarettes After Sex", "https://www.youtube.com/watch?v=3DhndiNT_4s", "ETHEREAL", "\033[1;36m"),
    "3": ("Bee Gees", "https://www.youtube.com/watch?v=F2jTY0GZrds", "DISCO", "\033[1;33m")
}

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    defaults = {"xp": 0, "level": 1, "history": [], "total_min": 0}
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
    with open(f"pilot_{pilot_id}.json", 'w') as f: json.dump(data, f, indent=4)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def get_galaxy_frame(vibe, color):
    width = 75
    center = width // 2
    chars = ["●", "✦", "█", "»", "⚡"] if vibe == "DISCO" else ["◌", "○", "✧", "·", "°"]
    line = []
    for i in range(width):
        dist_from_center = abs(i - center)
        prob = 0.15 * (1 - (dist_from_center / center))
        if random.random() < (prob + 0.02): line.append(random.choice(chars))
        else: line.append(" ")
    return f"{color}{''.join(line)}\033[0m"

def main():
    clear()
    print("\033[1;32m  SOVEREIGN STATION v48.0 | ETERNAL_ORBIT_OS\033[0m")
    pilot_id = input("\n\033[1;32m[ LOGIN ]\033[0m IDENTIFY CAPTAIN: ").strip().upper() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print("\033[1;36m[ ATMOSPHERE ]\033[0m SELECT NEURAL STREAM:")
    for k, v in STREAMS.items(): print(f" {v[3]}[{k}]\033[0m > {v[0]}")
    choice = input("\n>> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    webbrowser.open(stream_data[1]) 
    
    clear()
    print(f"\033[1;33m[ MISSION ]\033[0m OBJECTIVE FOR {pilot_id}:")
    goal = input(">> ")

    while True:
        clear()
        lvl, xp = data['level'], data['xp']
        req = lvl * 300
        bar = "\033[1;32m█\033[0m" * int(((xp % req) / req) * 20) + "░" * (20 - int(((xp % req) / req) * 20))
        
        print(f"\033[1;32m╔═ CAPTAIN: {pilot_id} {'═'*35}╗")
        print(f"║ LVL: {lvl} | {bar} {xp%req}/{req} XP ║")
        print(f"╚═{'═'*53}╝\033[0m")
        print(f"\n STATUS: \033[1;33m{goal}\033[0m | VIBE: {stream_data[3]}{stream_data[0]}\033[0m")
        print("\n [1] ENGAGE_WARP [2] HISTORY_LOG [3] EXIT")
        
        cmd = input("\n>> ")
        
        if cmd == "1":
            duration = 25 * 60
            field = [get_galaxy_frame(stream_data[2], stream_data[3]) for _ in range(14)]
            try:
                while duration > 0:
                    m, s = divmod(int(duration), 60)
                    clear()
                    print(f"{stream_data[3]}{'═'*22} GALACTIC_WARP_ACTIVE {'═'*22}\033[0m")
                    field.pop(0); field.append(get_galaxy_frame(stream_data[2], stream_data[3]))
                    for line in field[:6]: print(f"   {line}")
                    print(f"\n{' '*28}\033[1;97m{m:02d}:{s:02d}\033[0m\n")
                    for line in field[7:]: print(f"   {line}")
                    time.sleep(0.4); duration -= 0.4
                
                # --- AUTO-LOG & POST-FLIGHT AUTOPLAY ---
                data['xp'] += 100; data['total_min'] += 25
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append({"ts": datetime.now().strftime('%Y-%m-%d %H:%M'), "task": goal, "vibe": stream_data[0]})
                save_data(pilot_id, data)
                
                print("\n\033[1;32m✔ MISSION COMPLETE. DATA SYNCED. REFRESHING STREAM...\033[0m")
                webbrowser.open(stream_data[1]) # AUTOPLAY AFTER SESSION
                time.sleep(3)
            except KeyboardInterrupt: pass

        elif cmd == "2":
            clear()
            print(f"\033[1;35m--- {pilot_id} CAREER HISTORY ---\033[0m")
            print(f"PILOT UUID: {pilot_id}_OS_2026")
            print(f"TOTAL FOCUS: {data['total_min']} MIN")
            for h in data['history'][-10:]: print(f" [{h['ts']}] {h['task']} ({h['vibe']})")
            input("\n[ENTER TO RETURN]")
        elif cmd == "3": break

if __name__ == "__main__": main()
