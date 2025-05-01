# TXOne Edge IPS Simulator: CPSDR Events & DoS Attack Toolkit

This repository contains tools to simulate detections for TXOne Edge IPS. It includes:

- 🧠 **CPSDR Event Generator** – Simulates malicious activity patterns using crafted network behavior and tools.
- 💥 **DoS Attack Simulator** – Generates DoS-style traffic using `hping3` and `nmap`.

---

## 📂 Files

- `cpsdr_simulator.py`: Simulates CPSDR event patterns (e.g., User-Agent anomalies, RPC discovery, lateral movement).
- `dos_attack_simulator.py`: Simulates common DoS attacks and port scan activity.

---

## 🔧 Requirements

This toolkit is designed for Kali Linux (or any Debian-based pentesting distro).

Install required tools:

```bash
sudo apt update
sudo apt install hping3 nmap curl -y
```

Make both Python scripts executable:
```bash
chmod +x cpsdr_simulator.py dos_attack_simulator.py
```

## 🚨 CPSDR Event Generator

Simulate a wide range of malicious patterns that map to MITRE ATT&CK tactics and techniques.

📌 Usage
python3 cpsdr_simulator.py -h
🧪 Example
Run a simulated attack for a Cobalt Strike Malleable Profile:

```bash
python3 cpsdr_simulator.py -o 2 -t 192.168.1.10
```

List of options (-o) supported:
Option	Pattern Description
- 1	BabyShark Agent Pattern
- 2	Cobalt Strike Malleable Profile
- 3	WannaCry Killswitch Domain
- 4	Possible Lateral Tool Transfer via SMB
- 6	Execution Via WMI
- 13	CobaltStrike Malleable OCSP Profile
- 14	PwnDrp Access
- 19	Raw Paste Service Access
- 20	Telegram API Access
- 23	Cobalt Strike Command and Control Beacon
- 24	Suspicious User Agent
- 25	Suspicious Base64 Encoded User-Agent

⚠️ **Note: Some patterns are network-based and require a reachable target IP.**

## 💣 DoS Attack Simulator

Simulate various DoS attacks and TCP/IP scans.

📌 Usage
```bash
python3 dos_attack_simulator.py -h
```

🧪 Examples
SYN Flood (DoS)
```bash
python3 dos_attack_simulator.py syn-flood 192.168.1.10 10
```
UDP Flood
```bash
python3 dos_attack_simulator.py udp-flood 192.168.1.10 10
```
ICMP Flood
```bash
python3 dos_attack_simulator.py icmp-flood 192.168.1.10 10
```

**Port Scans**

TCP SYN Scan:
```bash
python3 dos_attack_simulator.py tcp-scan-syn 192.168.1.10 5
```
TCP NULL Scan:
```bash
python3 dos_attack_simulator.py tcp-scan-null 192.168.1.10 5
```
TCP Xmas Scan:
```bash
python3 dos_attack_simulator.py tcp-scan-xmas 192.168.1.10 5
```
Ping Sweep:
```bash
python3 dos_attack_simulator.py ping-sweep 192.168.1.10 5
```

💡 Available Attack Types
- syn-flood
- udp-flood
- icmp-flood
- tcp-scan-syn
- tcp-scan-null
- tcp-scan-xmas
- ping-sweep

## ⚠️ Warning

This toolkit is for educational and internal testing only. Only use it on systems you own or are explicitly authorized to test. Unauthorized use may be illegal.

## 👨‍💻 Author

Created and maintained by no2play

