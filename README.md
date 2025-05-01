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

This is a Python-based simulation tool designed to trigger specific cybersecurity detection rules in a test environment, primarily for validating TXOne CPSDR (Cyber-Physical Systems Detection & Response) detections. 

The script simulates a variety of attack techniques such as lateral movement, service abuse, suspicious user agents, and port scanning.

---

## 🛠 Requirements

- Python 3
- `nmap`
- `smbclient`
- `rpcclient`
- `impacket` tools (`wmiexec.py`, `psexec.py`)
- `requests` library (`pip install requests`)

Ensure the attacker machine (e.g., Kali Linux) has access to these tools.

---

## 🚀 Usage

```bash
python3 simulate.py -o <rule_id> -t <target_ip> [-u <username> -p <password>]
```

Required Parameters
```bash
-o, --option — Rule number to simulate (see list below)
-t, --target — Target IP or hostname (required for most rules)
-u, --username — Username for authentication (required for certain rules)
-p, --password — Password for authentication (required for certain rules)
```

## 🧪 Supported Rules

| Rule ID | Description                                         | Requires Auth |
|---------|-----------------------------------------------------|---------------|
| 5       | Possible Lateral Tool Transfer via SMB             | ✅             |
| 6       | Remote System Discovery Via RPC                    | ✅             |
| 7       | Execution Via WMI                                  | ✅             |
| 16      | Spoolss Named Pipe Access via SMB                  | ✅             |
| 17      | Possible PsExec Execution                          | ✅             |
| 25      | Suspicious User Agent                              | ❌             |
| 26      | Suspicious Base64 Encoded User-Agent               | ❌             |
| 30      | Potential Network Sweep Detected                   | ❌             |
| 31      | Potential Port Scan Detected                       | ❌             |


## 🧑‍💻 Examples

Simulate PsExec (Rule 17):
```bash
python3 simulate.py -o 17 -t 192.168.1.100 -u admin -p P@ssw0rd!
```
Simulate Base64 User-Agent (Rule 26):
```bash
python3 simulate.py -o 26 -t 192.168.1.100
```

## ⚠️ Notes

- Use only in isolated, controlled environments (test labs).
- Some rules require valid credentials and target services (e.g., SMB, RPC) to be active.
- `impacket` tools must be in your `$PATH`.

---

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

