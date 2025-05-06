#!/usr/bin/env python3

import argparse
import subprocess
import base64
import requests
import sys

# Enable Impacket logging
logger.init()

rule_descriptions = {
    1: "BabyShark Agent Pattern",
    2: "Cobalt Strike Malleable Profile",
    3: "WannaCry Killswitch Domain",
    4: "Possible Lateral Tool Transfer via SMB",
    5: "Remote System Discovery Via RPC",
    6: "Execution Via WMI (Impacket)",
    15: "Spoolss Named Pipe Access via SMB",
    16: "Possible PsExec Execution (Impacket)",
    24: "Suspicious User Agent",
    25: "Suspicious Base64 Encoded User-Agent",
    29: "Potential Network Sweep Detected",
    30: "Potential Port Scan Detected",
}

description_text = "CPSDR Simulation Script (Kali - Attacker)\n\nSupported Rules:\n"
for number, desc in rule_descriptions.items():
    description_text += f"  {number}: {desc}\n"

parser = argparse.ArgumentParser(
    description=description_text,
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-o", "--option", required=True, type=int, help="Rule number to simulate (e.g., 5, 17, 30)")
parser.add_argument("-t", "--target", help="Target IP or hostname")
parser.add_argument("-u", "--username", help="Username for authentication (if required)")
parser.add_argument("-p", "--password", help="Password for authentication (if required)")

args = parser.parse_args()

def target_required(rule_id):
    return rule_id in [1, 2, 4, 5, 6, 15, 16, 24, 25, 29, 30]

def auth_required(rule_id):
    return rule_id in [4, 5, 6, 15, 16]

def get_cred_str():
    return f"{args.username}%{args.password}"

# Simulations
def simulate_1(target):  # BabyShark Agent Pattern
    print(f"[+] Simulating BabyShark Agent Pattern against {target}...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:11.0) Gecko BabyShark",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "param=" + base64.b64encode(b"ThisIsASimulatedBeacon").decode()

    try:
        response = requests.post(f"http://{target}/smart/stream.php", headers=headers, data=data, timeout=5)
        print(f"[+] HTTP status: {response.status_code}")
    except Exception as e:
        print(f"[!] Failed to connect to {target}: {e}")

def simulate_2(target):
    print(f"[+] Simulating Cobalt Strike Malleable Profile against {target}...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CobaltStrike",
        "Host": f"{target}",
        "Accept": "*/*",
        "Connection": "close"
    }
    data = base64.b64encode(b"GET /favicon.ico HTTP/1.1\r\nHost: beacon\r\n\r\n").decode()

    try:
        response = requests.post(f"http://{target}/submit", headers=headers, data=data, timeout=5)
        print(f"[+] HTTP status: {response.status_code}")
    except Exception as e:
        print(f"[!] Failed to connect to {target}: {e}")

def simulate_3(target=None):
    print("[+] Simulating WannaCry Killswitch Domain check...")

    # Simulate random killswitch domain (e.g., iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com)
    killswitch_domain = "iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com"

    try:
        response = requests.get(f"http://{killswitch_domain}", timeout=5)
        print(f"[+] HTTP status from killswitch domain: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Expected failure or blocked domain (simulated): {e}")

def simulate_4(target):  # SMB File Transfer
    print(f"[+] Simulating SMB File Transfer to {target}...")
    subprocess.run(["smbclient", f"//{target}/share", "-U", get_cred_str(), "-c", "put /etc/passwd"])

def simulate_5(target):  # RPC Discovery
    print(f"[+] Simulating RPC Discovery on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "enumdomusers"])

def simulate_6(target):  # WMI Exec (alternative)
    print(f"[+] Simulating WMI Execution on {target}...")
    # Use an alternative method like WinRM or PsExec here
    try:
        subprocess.run(["psexec.py", f"{args.username}:{args.password}@{target}", "ipconfig"], check=False)
    except Exception as e:
        print(f"[!] WMI execution failed: {e}")

def simulate_15(target):  # Spoolss Named Pipe
    print(f"[+] Simulating Spoolss Named Pipe Access on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "netshareenumall"])

def simulate_16(target):  # PsExec (alternative method)
    print(f"[+] Simulating PsExec Execution on {target}...")
    try:
        subprocess.run(["psexec.py", f"{args.username}:{args.password}@{target}", "cmd.exe"], check=False)
    except Exception as e:
        print(f"[!] PsExec execution failed: {e}")

def simulate_24(target):  # Suspicious User-Agent
    print(f"[+] Sending Suspicious User-Agent to {target}...")
    headers = {"User-Agent": "python-requests/evil-miner"}
    try:
        requests.get(f"http://{target}", headers=headers, timeout=5)
    except Exception as e:
        print(f"[!] HTTP request failed: {e}")

def simulate_25(target):  # Base64 User-Agent
    print(f"[+] Sending Base64 User-Agent to {target}...")
    b64_agent = base64.b64encode(b"malicious-agent").decode()
    headers = {"User-Agent": b64_agent}
    try:
        requests.get(f"http://{target}", headers=headers, timeout=5)
    except Exception as e:
        print(f"[!] HTTP request failed: {e}")

def simulate_29(target):  # Nmap Sweep
    print(f"[+] Running Nmap Sweep on {target}...")
    subprocess.run(["nmap", "-sn", target])

def simulate_30(target):  # Full Port Scan
    print(f"[+] Running Full Port Scan on {target}...")
    subprocess.run(["nmap", "-p-", target])

rule_map = {
    1: simulate_1,
    2: simulate_2,
    3: simulate_3,
    4: simulate_4,
    5: simulate_5,
    6: simulate_6,
    15: simulate_15,
    16: simulate_16,
    24: simulate_24,
    25: simulate_25,
    29: simulate_29,
    30: simulate_30
}

# Validation
if args.option not in rule_map:
    print(f"[!] Rule ID {args.option} is not supported in this script.")
    sys.exit(1)

if target_required(args.option) and not args.target:
    print(f"[!] Rule ID {args.option} requires a -t <target> argument.")
    sys.exit(1)

if auth_required(args.option) and (not args.username or not args.password):
    print("[!] This simulation requires -u <username> and -p <password>")
    sys.exit(1)

# Run
if args.target:
    rule_map[args.option](args.target)
else:
    rule_map[args.option]("")
