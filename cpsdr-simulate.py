#!/usr/bin/env python3

import argparse
import subprocess
import base64
import requests
import sys

rule_descriptions = {
    5: "Possible Lateral Tool Transfer via SMB",
    6: "Remote System Discovery Via RPC",
    7: "Execution Via WMI",
    8: "Scheduled Task/Job Via At",
    9: "File/Directory Discovery Via RPC",
    10: "Account Discovery Via RPC",
    11: "Network Share Discovery Via RPC",
    12: "Execution Via System Services",
    13: "Remote Schedule Task Lateral Movement via ITaskSchedulerService",
    16: "Spoolss Named Pipe Access via SMB",
    17: "Possible PsExec Execution",
    18: "Possible Windows Scheduled Task",
    19: "Possible Sensitive File Access",
    23: "Source Code Enumeration Detection by Keyword",
    24: "Cobalt Strike Command and Control Beacon",
    25: "Suspicious User Agent",
    26: "Suspicious Base64 Encoded User-Agent",
    27: "Communication to Ngrok Tunneling Service",
    28: "Suspicious Cobalt Strike DNS Beaconing",
    29: "DNS TXT Answer with Possible Execution Strings",
    30: "Potential Network Sweep Detected",
    31: "Potential Port Scan Detected",
    32: "Scheduled Task/Job Via Scheduled Task",
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

def simulate_7(target):  # WMI Exec
    print(f"[+] Simulating WMI Execution on {target}...")
    subprocess.run(["wmiexec.py", f"{args.username}:{args.password}@{target}", "ipconfig"], check=False)

def simulate_16(target):  # Spoolss Named Pipe
    print(f"[+] Simulating Spoolss Named Pipe Access on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "netshareenumall"])

def simulate_17(target):  # PsExec Execution
    print(f"[+] Simulating PsExec Execution on {target}...")
    subprocess.run(["psexec.py", f"{args.username}:{args.password}@{target}", "cmd.exe"], check=False)

def simulate_25(target):  # Suspicious User-Agent
    print(f"[+] Sending Suspicious User-Agent to {target}...")
    headers = {"User-Agent": "python-requests/evil-miner"}
    requests.get(f"http://{target}", headers=headers)

def simulate_26(target):  # Base64 User-Agent
    print(f"[+] Sending Base64 User-Agent to {target}...")
    b64_agent = base64.b64encode(b"malicious-agent").decode()
    headers = {"User-Agent": b64_agent}
    requests.get(f"http://{target}", headers=headers)

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
