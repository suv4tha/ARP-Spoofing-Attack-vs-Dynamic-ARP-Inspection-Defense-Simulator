# ARP Spoofing Attack vs Dynamic ARP Inspection Defense Simulator

## Overview
This project simulates an ARP Spoofing (Man-in-the-Middle) attack and demonstrates 
how Dynamic ARP Inspection (DAI) defends against it in a network environment.

## What is ARP Spoofing?
ARP Spoofing is an attack where a malicious actor sends fake ARP replies to 
associate their MAC address with a legitimate IP (e.g., the gateway), 
intercepting all traffic meant for that IP.

## Defense: Dynamic ARP Inspection (DAI)
DAI validates ARP packets against a trusted binding table (built from DHCP snooping). 
Any ARP reply with an IP-MAC mismatch is dropped immediately.

## Project Structure
- `attack/arp_spoof.py` – Simulates the ARP spoofing attack
- `defense/arp_inspection.py` – Simulates DAI packet inspection
- `simulator/network_sim.py` – Full network simulation (attack + defense)

## How to Run
```bash
pip install -r requirements.txt
python simulator/network_sim.py
```

## Demo Output
- Phase 1: Normal ARP traffic is accepted
- Phase 2: Without DAI → attacker poisons the ARP cache ❌
- Phase 3: With DAI → spoofed packet is blocked ✅

## Technologies
- Python 3
- Scapy (packet crafting)
- Colorama (colored terminal output)