import time, os, json, webbrowser, random, sys
from datetime import datetime

# --- CONFIGURATION & COLORS ---
C_PINK, C_YELLOW, C_BLUE, C_RESET = "\033[1;95m", "\033[1;93m", "\033[1;94m", "\033[0m"

STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/watch?v=OlXWoEvLig0", "NEBULA", "\033[1;35m"),
    "2": ("Cigarettes After Sex", "https://www.youtube.com/watch?v=3DhndiNT_4s", "VOID", "\033[1;36m"),
    "3": ("Bee Gees", "https://www.youtube.com/watch?v=F2jTY0GZrds", "SPIRAL", "\033[1;33m")
}

IROH_QUOTES = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "Sharing tea with a stranger is one of life's true delights."
]

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    defaults = {"xp": 0, "level": 1, "history": [], "total_min": 0}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
                return {**defaults, **data}
            except: return defaults
    return defaults

def save_data(pilot_id, data):
    with open(f"pilot_{pilot_id}.json", 'w') as f: json.dump(data, f, indent=4)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def get_dynamic_galaxy(setting):
    """Generates stars forming in different galactic settings"""
    width = 75
    center = width // 2
    
    # Star Palette
    p_stars = [C_PINK + "✦" + C_RESET, C_PINK + "✧" + C_RESET]
    y_stars = [C_YELLOW + "✦" + C_RESET, C_YELLOW + "★" + C_RESET]
    b_stars = [C_BLUE + "●" + C_RESET, C_BLUE + "◌" + C_RESET]
    
    # Adjust density and clustering based on 'setting'
    if setting == "NEBULA":      # Dense, colorful clusters
        base_prob, cluster_factor = 0.15, 1.2
    elif setting == "SPIRAL":    # Streaky, rhythmic patterns
        base_prob, cluster_factor = 0.10, 2.5
    else:                        # VOID: Sparse, distant stars
        base_prob, cluster_factor = 0.04, 0.5

    line = []
    for i in range(width):
        dist = abs(i - center)
        # Formation logic: stars cluster more in certain 'zones'
        zone_influence = 1.0 if (i % 15 < 5 and setting == "SPIRAL") else 0.6
        prob = base_prob * (1.5 - (dist / center)) * zone_influence * cluster_factor
        
        if random.random() < prob:
            line.append(random.choice(p_stars + y_stars + b_stars))
        else:
            line.append(" ")
    return "".join(line)

def main():
    clear()
    print(f"\033[1;95m  SOVEREIGN GALAXY v52.0 | SYSTEM TIME: {datetime.now().strftime('%H:%M')}\033[0m")
    pilot_id = input("\n\033[1;32m[ IDENTITY ]\033[0m LOGIN ID: ").strip().upper() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print("\033[1;36m[ ATMOSPHERE ]\033[0m SELECT NEURAL SETTING:")
    for k, v in STREAMS.items(): print(f" {v[3]}[{k}]\033[0m > {v[0]} ({v[2]})")
    choice = input("\n>> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    webbrowser.open(stream_data[1]) 
    
    clear()
    goal = input(f"\033[1;33m[ MISSION ]\033[0m GOAL FOR {pilot_id}: ")

    while True:
        clear()
        lvl, xp = data['level'], data['xp']
        req = lvl * 300
        bar = "\033[1;32m█\033[0m" * int(((xp % req) / req) * 20) + "░" * (20 - int(((xp % req) / req) * 20))
        
        print(f"\033[1;32m╔═ CAPTAIN: {pilot_id} {'═'*35}╗")
        print(f"║ LVL: {lvl} | {bar} {xp%req}/{req} XP ║")
        print(f"╚═{'═'*53}╝\033[0m")
        print(f"\n SETTING: \033[1;33m{stream_data[2]}\033[0m | VIBE: {stream_data[3]}{stream_data[0]}\033[0m")
        print("\n [1] ENGAGE_WARP [2] HISTORY_LOG [3] IROH_WISDOM [4] EXIT")
        
        cmd = input("\n>> ")
        
        if cmd == "1":
            duration = 25 * 60
            field = [get_dynamic_galaxy(stream_data[2]) for _ in range(14)]
            try:
                while duration > 0:
                    m, s = divmod(int(duration), 60)
                    clear()
                    print(f"\033[1;97m{'═'*20} TRAVERSING {stream_data[2]} {'═'*20}\033[0m")
                    field.pop(0); field.append(get_dynamic_galaxy(stream_data[2]))
                    for line in field[:6]: print(f"   {line}")
                    print(f"\n{' '*28}\033[1;97m{m:02d}:{s:02d}\033[0m\n")
                    for line in field[7:]: print(f"   {line}")
                    time.sleep(0.4); duration -= 0.4
                
                # REWARDS & AUTO-LOG
                data['xp'] += 100; data['total_min'] += 25
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append({"ts": datetime.now().strftime('%Y-%m-%d %H:%M'), "task": goal, "vibe": stream_data[0]})
                save_data(pilot_id, data)
                
                print("\n\033[1;32m✔ SECTOR CLEARED. REFRESHING STREAM...\033[0m")
                webbrowser.open(stream_data[1]) 
                time.sleep(4)
            except KeyboardInterrupt: pass

        elif cmd == "2":
            clear()
            print(f"\033[1;35m--- {pilot_id} CAREER LOGS ---\033[0m")
            for h in data['history'][-10:]: print(f" [{h['ts']}] {h['task']}")
            input("\n[ENTER TO RETURN]")
        elif cmd == "3":
            clear(); print(f"\n\033[1;36mIroh: \"{random.choice(IROH_QUOTES)}\"\033[0m"); input("\n[BACK]")
        elif cmd == "4":
            save_data(pilot_id, data); break

if __name__ == "__main__": main()
