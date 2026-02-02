import os
import time
import json
import sys
import random
import requests
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
MAX_THREADS = 25
BATCH_TIMEOUT = 10

# --- HACKER PALETTE ---
os.system('color')
G = "\033[32m"  # Terminal Green
R = "\033[31m"  # Error Red
W = "\033[0m"   # White
B = "\033[1m"   # Bold
C = "\033[36m"  # Cyan
Y = "\033[33m"  # Warning Yellow
P = "\033[35m"  # Purple

def type_writer(text, speed=0.005, color=G):
    """Simulates a retro terminal typing effect."""
    sys.stdout.write(color + B)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        # Randomize speed slightly for realism
        time.sleep(random.uniform(speed * 0.5, speed * 1.5))
    sys.stdout.write(W + "\n")

def fake_loading_screen():
    """Displays a fake initialization sequence."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Random Hex Dump Effect
    print(f"{G}")
    for _ in range(15):
        hex_str = " ".join([f"{random.randint(0, 255):02X}" for _ in range(16)])
        print(f"0x{random.randint(1000, 9999)}: {hex_str}")
        time.sleep(0.02)
    
    print(f"\n{W}[*] DECRYPTING KERNEL...", end="")
    time.sleep(0.5)
    print(f"{G} [OK]")
    
    modules = ["NET_SPOOF", "GHOST_PROTOCOL", "PACKET_SNIFFER", "DOM_INJECTOR", "API_BREAKER"]
    for mod in modules:
        sys.stdout.write(f"\r{W}[*] LOADING MODULE: {C}{mod:<15}")
        time.sleep(0.2)
        sys.stdout.write(f"{G} [LOADED]\n")
    
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{G}{B}
  .oooooo.           .o8                        
 d8P'  `Y8b         "888                        
888           .oooo.  888  .ooooo.   .oooo.o 
888          `P  )88b 888 d88' `88b d88(  "8 
888           .oP"888 888 888   888 `"Y88b.  
`88b    ooo  d8(  888 888 888   888 o.  )88b 
 `Y8bood8P'  `Y888""8o888 `Y8bod8P' 8""888P' 
{W}
    {C}[ SYSTEM: ROOT_ACCESS ]   [ TARGET: DOJ_MAINFRAME ]{W}
    {R}----------------------------------------------------------{W}
    """)

# --- EXECUTION FLOW ---
fake_loading_screen()
banner()

# --- 1. TARGET ACQUISITION ---
type_writer("[?] INITIATING TARGET ACQUISITION PROTOCOL...", 0.02, C)
print(f"{G}    [1] BATCH_LOAD: 'names.txt'{W}")
print(f"{G}    [2] MANUAL_INJECT: Direct Input{W}")

choice = input(f"{B}>> COMMAND: {W}")

names = []
if choice == '1':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "names.txt")
    if not os.path.exists(file_path):
        type_writer("[!] CRITICAL ERROR: TARGET LIST NOT FOUND. ABORTING.", 0.05, R)
        exit()
    with open(file_path, "r", encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]
    type_writer(f"[*] UPLOAD COMPLETE. {len(names)} TARGETS QUEUED.", 0.02, G)

elif choice == '2':
    raw = input(f"{B}>> ENTER PAYLOADS: {W}")
    names = [n.strip() for n in raw.split(',') if n.strip()]
else:
    exit()

# --- 2. SESSION HIJACKING ---
type_writer("\n[*] INITIALIZING GHOST_BROWSER FOR SESSION HIJACK...", 0.03, Y)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

TARGET_URL = "https://www.justice.gov/epstein"
driver.get(TARGET_URL)

print(f"\n{R}" + "="*60)
print(f"{B} [!] SECURITY CHECKPOINT DETECTED [!] {W}")
print(f"{C} 1. BYPASS CAPTCHA MANUALLY.")
print(f"{C} 2. AWAIT SEARCH INTERFACE.")
print(f"{R}" + "="*60)
input(f"\n{G}>> PRESS ENTER TO INJECT SESSION TOKEN...{W}")

# Steal Cookies
selenium_cookies = driver.get_cookies()
user_agent = driver.execute_script("return navigator.userAgent")
driver.quit()

type_writer("[+] SESSION TOKEN EXFILTRATED.", 0.02, G)
type_writer(f"[+] SPOOFING USER AGENT: {user_agent[:25]}...", 0.005, C)
type_writer("[+] ESTABLISHING ENCRYPTED TUNNEL TO API...", 0.02, G)

# --- 3. CONFIGURE ASSAULT ---
session = requests.Session()
session.headers.update({
    "User-Agent": user_agent,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.justice.gov/epstein"
})
for cookie in selenium_cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# --- 4. SCANNER LOGIC ---
API_URL = "https://www.justice.gov/multimedia-search"

def check_target(name):
    try:
        params = {"keys": f'"{name}"'} 
        response = session.get(API_URL, params=params, timeout=BATCH_TIMEOUT)
        
        links = []
        status = "CLEAN"
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('hits', {}).get('total', {}).get('value', 0) > 0:
                    status = "HIT"
                    hits_list = data.get('hits', {}).get('hits', [])
                    links = [h['_source']['ORIGIN_FILE_URI'] for h in hits_list if '_source' in h]
            except json.JSONDecodeError:
                pass
        return name, status, links
    except:
        return name, "ERROR", []

# --- 5. LIVE ATTACK MONITOR ---
print(f"\n{W}" + "-"*60)
print(f"{B}TARGET_ID                       STATUS_INDICATOR")
print(f"{W}" + "-"*60)

total_hits = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    future_to_name = {executor.submit(check_target, name): name for name in names}
    
    for future in concurrent.futures.as_completed(future_to_name):
        name, status, links = future.result()
        
        if status == "HIT":
            total_hits += 1
            # Dramatic HIT Effect
            print(f"{R}{B}{name:<30} [!] MATCH CONFIRMED [!]{W}")
            time.sleep(0.1) # Brief pause for effect
            print(f"{Y}    >>> EXFILTRATING {len(links)} FILES...{W}")
            for link in links:
                print(f"{C}    > {link}{W}")
            print(f"{R}" + "-"*60 + f"{W}")
            
        elif status == "CLEAN":
            # Fast, scrolling clean status
            print(f"{G}{name:<30} [ ] CLEAN{W}")
        else:
            print(f"{P}{name:<30} [?] CONNECTION_RESET{W}")

# --- SUMMARY ---
print(f"{W}" + "="*60)
if total_hits > 0:
     type_writer(f"[!] WARNING: {total_hits} POSITIVE MATCHES LOGGED.", 0.05, R)
     type_writer("[!] DATA DUMP COMPLETE.", 0.05, R)
else:
     type_writer("[+] SYSTEM CLEAN. NO EVIDENCE FOUND.", 0.05, G)

print(f"\n{C}Credit: Ys6a // Fsociety Protocol v3.1{W}")
input(f"{B}Press Enter to terminate connection...{W}")