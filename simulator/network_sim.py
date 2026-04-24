# Full ARP Spoofing vs DAI Simulation
import time, colorama
from colorama import Fore, Style
colorama.init()

TRUSTED_TABLE = {
    "192.168.1.1":  "aa:11:bb:22:cc:33",
    "192.168.1.10": "aa:bb:cc:dd:ee:ff",
}

ARP_CACHE = {}  # Simulates victim's ARP cache

def update_arp_cache(ip, mac, use_dai=False):
    if use_dai:
        expected = TRUSTED_TABLE.get(ip)
        if expected and expected != mac:
            print(Fore.RED + f"  [DAI BLOCKED] Spoofed ARP for {ip} rejected!" + Style.RESET_ALL)
            return
    ARP_CACHE[ip] = mac
    print(Fore.GREEN + f"  [ARP CACHE] {ip} → {mac}" + Style.RESET_ALL)

def run_simulation(use_dai=False):
    mode = "WITH Dynamic ARP Inspection" if use_dai else "WITHOUT Defense (Vulnerable)"
    print(Fore.CYAN + f"\n{'='*50}\nSimulation: {mode}\n{'='*50}" + Style.RESET_ALL)

    print("\n[Phase 1] Normal ARP traffic:")
    update_arp_cache("192.168.1.1", "aa:11:bb:22:cc:33", use_dai)
    update_arp_cache("192.168.1.10", "aa:bb:cc:dd:ee:ff", use_dai)
    time.sleep(1)

    print("\n[Phase 2] Attacker sends spoofed ARP reply:")
    print(Fore.YELLOW + "  [ATTACK] Sending fake ARP: 192.168.1.1 is at 11:22:33:44:55:66" + Style.RESET_ALL)
    update_arp_cache("192.168.1.1", "11:22:33:44:55:66", use_dai)
    time.sleep(1)

    print(f"\n[Result] Victim ARP Cache: {ARP_CACHE}")
    if ARP_CACHE.get("192.168.1.1") == "11:22:33:44:55:66":
        print(Fore.RED + "  ❌ ATTACK SUCCEEDED — Traffic redirected to attacker!" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "  ✅ ATTACK BLOCKED — ARP cache is clean." + Style.RESET_ALL)
    ARP_CACHE.clear()

if __name__ == "__main__":
    run_simulation(use_dai=False)  # Show attack succeeding
    time.sleep(2)
    run_simulation(use_dai=True)   # Show defense blocking it