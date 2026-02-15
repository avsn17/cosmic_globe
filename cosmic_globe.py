import time, os, random, sys, json, argparse

DATA_FILE = os.path.expanduser("~/.spacey2_stats.json")
def load_stats():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f: return json.load(f)
        except: pass
    return {"total_meters": 0.0, "xp": 0, "missions": 0}

def save_stats(stats):
    with open(DATA_FILE, 'w') as f: json.dump(stats, f)

G, R, Y, C, W = "\033[1;32m", "\033[1;31m", "\033[1;33m", "\033[1;36m", "\033[0m"

def bold_type(text, color=G):
    for char in text:
        sys.stdout.write(f"{color}{char}{W}"); sys.stdout.flush(); time.sleep(0.02)
    print()

def show_stats():
    s = load_stats()
    print(f"\n{Y}>>> COSMIC_GLOBE CORE_STATS{W}\n{G}METERS: {s['total_meters']:.2f}m\nXP:     {s['xp']}\nMISSIONS: {s['missions']}{W}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mins", type=float, nargs='?', default=25.0)
    parser.add_argument("--stats", action="store_true")
    args = parser.parse_args()
    if args.stats: show_stats()
    else: print(f"{G}BOLD: LOCK IN. MISSION STARTING...{W}")
