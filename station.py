import time, os, json, webbrowser
from datetime import datetime

def load_data(pilot_id):
    filename = f"pilot_{pilot_id}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f: return json.load(f)
    return {"sessions": 0, "history": []}

def save_data(pilot_id, data):
    with open(f"pilot_{pilot_id}.json", 'w') as f: json.dump(data, f, indent=4)

def main():
    os.system('clear')
    print("\033[1;32m=== CHRONOS IDENTITY TERMINAL ===\033[0m")
    pilot_id = input("ENTER_PILOT_ID > ").strip() or "AVI"
    data = load_data(pilot_id)
    
    # Music Autoplay in background
    webbrowser.open("https://stream.nightride.fm/nightride.mp3")

    while True:
        print(f"\n[PILOT: {pilot_id}] | Sessions: {data['sessions']}")
        print("1. [ENGAGE] 2. [HISTORY] 3. [EXIT]")
        choice = input("SELECT > ")
        
        if choice == "1":
            print("Warp engaged (25m)...")
            time.sleep(2) # Simulating timer for brevity
            data['sessions'] += 1
            data['history'].append(datetime.now().strftime('%Y-%m-%d %H:%M'))
            save_data(pilot_id, data)
            print("AUTO-SAVED. Mission Logged.")
        elif choice == "2":
            print(data['history'])
        elif choice == "3": break

if __name__ == "__main__":
    main()
