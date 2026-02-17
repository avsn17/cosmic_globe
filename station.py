import time, os, json, webbrowser, random, sys, glob, uuid
from datetime import datetime

# --- SYSTEM THEME ---
P, Y, B, G, C, W, R = "\033[1;95m", "\033[1;93m", "\033[1;94m", "\033[1;32m", "\033[1;36m", "\033[1;97m", "\033[0m"

STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/watch?v=OlXWoEvLig0", "NEBULA", P),
    "2": ("Cigarettes After Sex", "https://www.youtube.com/watch?v=3DhndiNT_4s", "VOID", C),
    "3": ("Bee Gees", "https://www.youtube.com/watch?v=F2jTY0GZrds", "SPIRAL", Y)
}

IROH = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "Good tea is its own reward.",
    "While it is always best to believe in oneself, a little help from others can be a great blessing."
]

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
    files = glob.glob("pilot_*.json")
    ranks = []
    for f in files:
        try:
            with open(f, 'r') as file:
                d = json.load(file); p_id = f.replace("pilot_", "").replace(".json", "")
                ranks.append({"id": p_id, "lvl": d.get("level", 1), "xp": d.get("xp", 0)})
        except: continue
    return sorted(ranks, key=lambda x: (x['lvl'], x['xp']), reverse=True)

def write_global_log(entry):
    with open("fleet_activity.log", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {entry}\n")

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def generate_parallax_line(width=110):
    line = [" "] * width
    if random.random() < 0.08: line[random.randint(0, width-1)] = f"{W}·{R}" 
    if random.random() < 0.05: line[random.randint(0, width-1)] = random.choice([f"{Y}★{R}", f"{B}◌{R}"]) 
    if random.random() < 0.03: line[random.randint(0, width-1)] = random.choice([f"{P}✦{R}", f"{B}●{R}"]) 
    return "".join(line)

def main():
    clear()
    print(f"{G}  SOVEREIGN APEX v61.0 | LOGGED: 2026-02-17{R}")
    pilot_id = input(f"\n{G}[ IDENTITY ]{R} LOGIN ID: ").strip().upper() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print(f"{C}[ ATMOSPHERE ]{R} SELECT STREAM (AUTOPLAY ACTIVE):")
    for k, v in STREAMS.items(): print(f" {v[3]}[{k}]{R} > {v[0]}")
    choice = input("\n>> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    webbrowser.open(stream_data[1]) # Initial Autoplay
    
    clear()
    goal = input(f"{Y}[ MISSION ]{R} SET TARGET FOR {pilot_id}: ")

    while True:
        clear()
        lvl, xp, req = data['level'], data['xp'], data['level'] * 300
        prog = int(((xp % req) / req) * 45)
        bar = f"{G}█{R}" * prog + f"{W}░{R}" * (45 - prog)
        
        print(f"{G}╔═ CAPTAIN: {pilot_id} {'═'*75}╗")
        print(f"║ LVL: {lvl} | {bar} {xp%req}/{req} XP ║")
        print(f"╚═{'═'*93}╝{R}")
        print(f"\n [1] WARP [2] FULL_LOGS [3] LEADERBOARD [4] IROH [5] EXIT")
        
        cmd = input("\n>> ")
        
        if cmd == "1":
            sid = str(uuid.uuid4())[:8]
            duration = 25 * 60
            field = [generate_parallax_line() for _ in range(25)]
            try:
                while duration > 0:
                    m, s = divmod(int(duration), 60)
                    clear()
                    print(f"{W}{'═'*35} MISSION_ID: {sid} | {stream_data[2]} {'═'*35}{R}")
                    field.pop(0); field.append(generate_parallax_line())
                    for i, line in enumerate(field):
                        if i == 11: print(f"  {line[:45]}  {W}{m:02d}:{s:02d}{R}  {line[55:]}")
                        elif i == 12: print(f"  {line[:45]}  {Y}{goal[:12]}{R}  {line[55:]}")
                        else: print(f"  {line}")
                    time.sleep(0.3); duration -= 0.3
                
                # --- DATA PROCESSING ---
                data['xp'] += 100; data['total_min'] += 25
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                
                lb = get_leaderboard()
                rank = next((i + 1 for i, p in enumerate(lb) if p['id'] == pilot_id), "?")
                
                entry = {"id": sid, "ts": datetime.now().strftime('%Y-%m-%d %H:%M'), "goal": goal, "rank": rank}
                data['history'].append(entry)
                save_data(pilot_id, data)
                write_global_log(f"PILOT {pilot_id} COMPLETED {sid} | RANK: {rank}")
                
                print(f"\n{G}✔ MISSION LOGGED. RE-TRIGGERING MUSIC...{R}")
                webbrowser.open(stream_data[1]) # Continuous Autoplay
                time.sleep(4)
            except KeyboardInterrupt: pass

        elif cmd == "2":
            clear()
            print(f"{P}═══ {pilot_id} MISSION CHRONICLES ═══{R}")
            for h in data['history'][-8:]:
                print(f" > {h['ts']} | ID:{h['id']} | RANK:{h.get('rank','?')} | {Y}{h['goal'][:20]}{R}")
            input("\n[ENTER]")
            
        elif cmd == "3":
            clear()
            print(f"{Y}═══ FLEET LEADERBOARD (LIVE) ═══{R}")
            for r, p in enumerate(get_leaderboard()[:10], 1):
                marker = f"{G}>>{R}" if p['id'] == pilot_id else "  "
                print(f" {marker} {r}. {p['id']:<12} | LVL: {p['lvl']} | XP: {p['xp']}")
            input("\n[ENTER]")

        elif cmd == "4":
            clear(); print(f"\n{C}Uncle Iroh: \"{random.choice(IROH)}\"{R}"); input("\n[BACK]")
        elif cmd == "5": save_data(pilot_id, data); break

if __name__ == "__main__": main()
