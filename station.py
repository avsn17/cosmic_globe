import time, os, json, webbrowser, random, sys
from datetime import datetime

# --- ASSETS: IROH & THE TRIDENT PLAYLIST ---
IROH_QUOTES = [
    "Hope is something you give yourself. That is the meaning of inner strength.",
    "Destiny is a funny thing. You never know how things are going to work out.",
    "While it is always best to believe in oneself, a little help from others can be a great blessing."
]

STREAMS = {
    "1": ("Lana Del Rey", "https://www.youtube.com/results?search_query=lana+del+rey+playlist", "NOIR", "\033[1;35m"), # Purple/Pink
    "2": ("Cigarettes After Sex", "https://www.youtube.com/results?search_query=cigarettes+after+sex+playlist", "ETHEREAL", "\033[1;36m"), # Cyan
    "3": ("Bee Gees", "https://www.youtube.com/results?search_query=bee+gees+disco+playlist", "DISCO", "\033[1;33m") # Gold/Yellow
}

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

def print_banner(text, color_code):
    """Prints stylized ASCII-style titles."""
    print(f"{color_code}--- {text.upper()} --- \033[0m")

def get_flight_frame(vibe_type, color):
    width = 65
    if vibe_type == "NOIR": chars = ["·", " ", " ", "°", "✧"]
    elif vibe_type == "ETHEREAL": chars = ["◌", " ", " ", " ", "▫"]
    else: chars = ["★", "✧", " ", " ", "»", ">", "⚡"]
    line = "".join(random.choice(chars) if random.random() > 0.93 else " " for _ in range(width))
    return f"{color}{line}\033[0m"

def main():
    clear()
    # INITIAL BOOT FONT
    print("\033[1;32m")
    print("  ____  _______      ________ _____  ______ _____ _____ _   _ ")
    print(" / ___||  _ \ \    / /  ____|  __ \|  ____|_   _/ ____| \ | |")
    print(" \___ \| | | \ \  / /| |__  | |__) | |__    | || |  __|  \| |")
    print("  ___) | |_| |\ \/ / |  __| |  _  /|  __|   | || | |_ | |\  |")
    print(" |____/|____/  \__/  |____||_| \_\|____|  |_____\____|_| \_|")
    print("\033[0m")
    
    pilot_id = input("\033[1;32m[ IDENTITY ]\033[0m ENTER CAPTAIN ID: ").strip() or "AVI"
    data = load_data(pilot_id)
    
    clear()
    print_banner("ATMOSPHERE_SELECT", "\033[1;36m")
    for k, v in STREAMS.items(): 
        print(f" {v[3]}[{k}]\033[0m > {v[0]}")
    choice = input("\n>> ")
    stream_data = STREAMS.get(choice, STREAMS["1"])
    webbrowser.open(stream_data[1])
    
    clear()
    print_banner("MISSION_GOAL", "\033[1;33m")
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
        
        print(f"\n \033[1;37mGOAL:\033[0m \033[1;33m{goal}\033[0m")
        print(f" \033[1;37mVIBE:\033[0m {stream_data[3]}{stream_data[0]}\033[0m")
        
        print("\n \033[1;32m[1]\033[0m ENGAGE_WARP  \033[1;36m[2]\033[0m IROH_QUOTE  \033[1;31m[3]\033[0m EXIT")
        
        cmd = input("\n>> ")
        
        if cmd == "1":
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
                
                data['xp'] += 100
                if data['xp'] >= (data['level'] * 300): data['level'] += 1
                data['history'].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {goal}")
                save_data(pilot_id, data)
                print("\n\n\033[1;32m✔ MISSION SUCCESS. XP SYNCED.\033[0m")
                time.sleep(3)
            except KeyboardInterrupt: pass
        elif cmd == "2":
            clear()
            print(f"\n\033[1;36mUncle Iroh: \"{random.choice(IROH_QUOTES)}\"\033[0m")
            input("\n[Back]")
        elif cmd == "3":
            save_data(pilot_id, data)
            break

if __name__ == "__main__": main()
