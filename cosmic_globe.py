import time, os, sys, json, argparse
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.spacey2_stats.json")
LOG_FILE = os.path.expanduser("~/.cosmic_globe/mission_log.txt")

def log_mission(mins, meters):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] MISSION: {mins}m | DISTANCE: {meters:.2f}m | STATUS: SUCCESS\n")

def start_warp(mins):
    print(f"\033[1;32mBOLD: COMMENCING {mins} MINUTE WARP...\033[0m")
    time.sleep(1) # Orbital sync delay
    meters = mins * 0.5
    log_mission(mins, meters)
    print(f"\033[1;32mBOLD: MISSION SUCCESS. {meters} METERS LOGGED.\033[0m")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mins", type=float, nargs='?', default=25.0)
    parser.add_argument("--stats", action="store_true")
    args = parser.parse_args()
    if args.stats:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f: print(f.read())
        else:
            print("BOLD: NO LOGS FOUND. START A MISSION.")
    else:
        start_warp(args.mins)
