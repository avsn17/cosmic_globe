import time, os, json, webbrowser, random, sys, glob
from datetime import datetime

# --- CONFIGURATION & COLORS ---
C_PINK, C_YELLOW, C_BLUE, C_GREEN, C_RESET = "\033[1;95m", "\033[1;93m", "\033[1;94m", "\033[1;32m", "\033[0m"

STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/watch?v=OlXWoEvLig0", "NEBULA", "\033[1;35m"),
    "2": ("Cigarettes After Sex", "https://www.youtube.com/watch?v=3DhndiNT_4s", "VOID", "\033[1;36m"),
    "3": ("Bee Gees", "https://www.youtube.com/watch?v=F2jTY0GZrds", "SPIRAL", "\033[1;33m")
}

IROH_QUOTES = ["Hope is something you give yourself.", "Destiny is a funny thing.", "Sharing tea with a stranger is a delight."]

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    defaults = {"xp": 0, "level": 1, "history": [], "total_min": 0}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try: return {**defaults, **json.load(f)}
            except: return defaults
    return defaults

def save_data(pilot_id, data):
    with open(f"pilot_{pilot_id}.json", 'w') as f: json.dump(data, f, indent=4)

def get_leaderboard():
    """Scans all pilot JSONs and ranks them by level and XP"""
    files = glob.glob("pilot_*.json")
    ranks = []
    for f in files:
        try:
            with open(f, 'r') as file:
                d = json.load(file)
                p_id = f.replace("pilot_", "").replace(".json", "")
                ranks.append({"id": p_id, "lvl": d.get("level", 1), "xp": d.get("xp", 0)})
        except: continue
    return sorted(ranks, key=lambda x: (x['lvl'], x['xp']), reverse=True)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def get_dynamic_galaxy(setting):
    width, center = 100, 50
    stars = [C_PINK+"✦"+C_RESET, C_PINK+"✧"+C_RESET, C_YELLOW+"✦"+C_RESET, C_YELLOW+"★"+C_RESET, C_BLUE+"●"+C_RESET, C_BLUE+"◌"+C_RESET]
    line = []
    for i in range(width):
        dist = abs(i - center)
        prob = 0.12 * (1.8 - (dist / center))
        if random.random() < prob: line.append(random.choice(stars))
        else: line.append(" ")
    return "".join(line)

def main():
    clear()
    print(f"{C_GREEN}  SOVEREIGN HIGH COMMAND v54.0 | SYNC: 2026-02-17{C_RESET}")
    pilot_id = input(f"\n{C_GREEN}[ IDENTITY ]{C_RESET} LOGIN ID: ").strip().upper() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print(f"{C_BLUE}[ ATMOSPHERE ]{C_RESET} SELECT NEURAL SETTING:")
    for k, v in STREAMS.items(): print(f" {v[3]}[{k}]{C_RESET} > {v[0]}")
    choice = input("\n>> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    webbrowser.open(stream_data[1]) 
    
    clear()
    goal = input(f"{C_YELLOW}[ MISSION ]{C_RESET} GOAL FOR {pilot_id}: ")

    while True:
        clear()
        lvl, xp, req = data['level'], data['xp'], data['level'] * 300
        bar = f"{C_GREEN}█{C_RESET}" * int(((xp % req) / req) * 30) + "░" * (30 - int(((xp % req) / req) * 30))
        print(f"{C_GREEN}╔═ CAPTAIN: {pilot_id} {'═'*65}╗\n║ LVL: {lvl} | {bar} {xp%req}/{req} XP ║\n╚═{'═'*83}╝{C_RESET}")
        print(f"\n [1] WARP [2] HISTORY [3] LEADERBOARD [4] IROH [5] EXIT")
        
        cmd = input("\n>> ")
        
        if cmd == "1":
            duration = 25 * 60
            field = [get_dynamic_galaxy(stream_data[2]) for _ in range(20)]
            try:
                while duration > 0:
                    m, s = divmod(int(duration), 60)
                    clear()
                    print(f"{C_RESET}{'═'*35} TRAVERSING {stream_data[2]} {'═'*35}")
                    field.pop(0); field.append(get_dynamic_galaxy(stream_data[2]))
                    for line in field[:9]: print(f"   {line}")
                    print(f"\n{' '*45}{C_RESET}{m:02d}:{s:02d}"); print(f"{' '*45}{C_YELLOW}{goal[:15]}{C_RESET}\n")
                    for line in field[10:]: print(f"   {line}")
                    time.sleep(0.4); duration -= 0.4
                data['xp'] += 100; data['total_min'] += 25
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append({"ts": datetime.now().strftime('%y-%m-%d %H:%M'), "task": goal})
                save_data(pilot_id, data); webbrowser.open(stream_data[1])
            except KeyboardInterrupt: pass

        elif cmd == "3":
            clear()
            print(f"{C_YELLOW}--- GALAXY LEADERBOARD ---{C_RESET}")
            for r, p in enumerate(get_leaderboard()[:10], 1):
                color = C_GREEN if p['id'] == pilot_id else ""
                print(f" {r}. {color}{p['id']:<10}{C_RESET} | LVL: {p['lvl']} | XP: {p['xp']}")
            input("\n[ENTER]")
        elif cmd == "2":
            clear(); print(f"--- {pilot_id} LOGS ---")
            for h in data['history'][-10:]: print(f" [{h['ts']}] {h['task']}")
            input("\n[ENTER]")
        elif cmd == "4":
            clear(); print(f"\n{C_BLUE}Iroh: \"{random.choice(IROH_QUOTES)}\"{C_RESET}"); input("\n[BACK]")
        elif cmd == "5": save_data(pilot_id, data); break

if __name__ == "__main__": main()
