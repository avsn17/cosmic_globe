import time, os, json, webbrowser, random, sys
from datetime import datetime

# --- CAPTAIN'S REFINED PLAYLIST ---
STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/watch?v=OlXWoEvLig0", "NOIR", "\033[1;35m"),
    "2": ("Cigarettes After Sex", "https://www.youtube.com/watch?v=3DhndiNT_4s", "ETHEREAL", "\033[1;36m"),
    "3": ("Bee Gees", "https://www.youtube.com/watch?v=F2jTY0GZrds", "DISCO", "\033[1;33m")
}

IROH_QUOTES = [
    "Hope is something you give yourself.",
    "Destiny is a funny thing.",
    "A little help from others can be a great blessing."
]

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    defaults = {"sessions": 0, "xp": 0, "level": 1, "history": []}
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

def get_flight_frame(vibe_type, color):
    width = 65
    chars = ["★", "✧", "»", "·", "°"] if vibe_type == "DISCO" else ["·", " ", "°", "✧"]
    line = "".join(random.choice(chars) if random.random() > 0.93 else " " for _ in range(width))
    return f"{color}{line}\033[0m"

def main():
    clear()
    # SOVEREIGN LOGO
    print("\033[1;32m   _____ ____  _    _ ______ _____  ______ _____ _____ _   _ ")
    print("  / ____/ __ \| |  | |  ____|  __ \|  ____|_   _/ ____| \ | |")
    print(" | (___| |  | | |  | | |__  | |__) | |__    | || |  __|  \| |")
    print("  \___ \ |  | | |  | |  __| |  _  /|  __|   | || | |_ | |\  |")
    print("  ____) | |__| \ \__/ / |____| | \ \| |____ | || |__| | | \ |")
    print(" |_____/ \____/ \____/|______|_|  \_\______|_____\____|_|  \_|\033[0m")
    
    pilot_id = input("\n\033[1;32m[ LOGIN ]\033[0m CAPTAIN ID: ").strip() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print("\033[1;36m[ ATMOSPHERE ]\033[0m SELECT NEURAL STREAM:")
    for k, v in STREAMS.items(): 
        print(f" {v[3]}[{k}]\033[0m > {v[0]}")
    
    # --- INSTANT AUTOPLAY TRIGGER ---
    choice = input("\n>> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    print(f"\n\033[1;34m[SYSTEM] Initializing {stream_data[0]} stream...\033[0m")
    webbrowser.open(stream_data[1])
    
    time.sleep(1) # Brief pause for browser launch
    
    clear()
    print(f"\033[1;33m[ MISSION ]\033[0m SET GOAL FOR THIS SESSION:")
    goal = input(">> ")

    while True:
        clear()
        lvl = data['level']
        req = lvl * 300
        prog = int(((data['xp'] % req) / req) * 20)
        bar = "\033[1;32m█\033[0m" * prog + "░" * (20 - prog)
        
        print(f"\033[1;32m╔═ CAPTAIN: {pilot_id} {'═'*35}╗")
        print(f"║ LVL: {lvl} | {bar} {data['xp']%req}/{req} XP ║")
        print(f"╚═{'═'*53}╝\033[0m")
        print(f"\n \033[1;37mGOAL:\033[0m \033[1;33m{goal}\033[0m | \033[1;37mVIBE:\033[0m {stream_data[3]}{stream_data[0]}\033[0m")
        print("\n \033[1;32m[1] ENGAGE_WARP\033[0m  |  \033[1;36m[2] IROH\033[0m  |  \033[1;31m[3] EXIT\033[0m")
        
        cmd = input("\n>> ")
        
        if cmd == "1":
            duration = 25 * 60
            try:
                while duration > 0:
                    m, s = divmod(duration, 60)
                    clear()
                    print(f"{stream_data[3]}{'═'*20} {stream_data[2]}_WARP_ACTIVE {'═'*20}\033[0m")
                    for _ in range(5): print(f"   {get_flight_frame(stream_data[2], stream_data[3])}")
                    print(f"\n{' '*23}\033[1;97m{m:02d}:{s:02d}\033[0m")
                    print(f"{' '*23}\033[1;33m{goal}\033[0m\n")
                    for _ in range(5): print(f"   {get_flight_frame(stream_data[2], stream_data[3])}")
                    time.sleep(1)
                    duration -= 1
                
                data['xp'] += 100
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {goal}")
                save_data(pilot_id, data)
                print("\n\n\033[1;32m✔ SUCCESS. DATA LOGGED.\033[0m")
                time.sleep(2)
            except KeyboardInterrupt: pass
        elif cmd == "2":
            clear()
            print(f"\n\033[1;36mUncle Iroh: \"{random.choice(IROH_QUOTES)}\"\033[0m")
            input("\n[Back]")
        elif cmd == "3":
            save_data(pilot_id, data)
            break

if __name__ == "__main__": main()
