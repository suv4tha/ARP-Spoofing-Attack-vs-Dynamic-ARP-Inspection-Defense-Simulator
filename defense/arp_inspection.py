# Dynamic ARP Inspection (DAI) Defense Simulator
import colorama
from colorama import Fore, Style
colorama.init()

# Trusted ARP table: IP -> legitimate MAC (simulates DHCP snooping binding table)
TRUSTED_ARP_TABLE = {
    "192.168.1.1":  "aa:11:bb:22:cc:33",   # Gateway
    "192.168.1.10": "aa:bb:cc:dd:ee:ff",   # Host A
    "192.168.1.20": "ff:ee:dd:cc:bb:aa",   # Host B
}

def inspect_arp_packet(src_ip, src_mac):
    print(Fore.CYAN + f"\n[DAI] Inspecting ARP packet: {src_ip} claims MAC {src_mac}" + Style.RESET_ALL)
    expected_mac = TRUSTED_ARP_TABLE.get(src_ip)
    if expected_mac is None:
        print(Fore.YELLOW + f"  [WARNING] Unknown IP {src_ip} — packet dropped." + Style.RESET_ALL)
        return False
    if src_mac != expected_mac:
        print(Fore.RED + f"  [BLOCKED] ARP Spoofing detected! Expected {expected_mac}, got {src_mac}. Packet dropped." + Style.RESET_ALL)
        return False
    print(Fore.GREEN + f"  [ALLOWED] ARP packet is legitimate. Forwarded." + Style.RESET_ALL)
    return True

if __name__ == "__main__":
    # Simulate packets coming in
    test_packets = [
        ("192.168.1.1",  "aa:11:bb:22:cc:33"),   # Legitimate gateway
        ("192.168.1.1",  "11:22:33:44:55:66"),   # ATTACK: wrong MAC for gateway
        ("192.168.1.10", "aa:bb:cc:dd:ee:ff"),   # Legitimate host
        ("192.168.1.99", "de:ad:be:ef:00:01"),   # Unknown IP
    ]
    results = [inspect_arp_packet(ip, mac) for ip, mac in test_packets]
    blocked = results.count(False)
    allowed = results.count(True)
    print(f"\n[SUMMARY] {allowed} packets allowed, {blocked} packets blocked by DAI.")