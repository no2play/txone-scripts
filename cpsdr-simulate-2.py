#!/usr/bin/env python3

import argparse
import subprocess
import base64
import requests
import sys

rule_descriptions = {
    1: "BabyShark Agent Pattern",
    2: "Cobalt Strike Malleable Profile",
    3: "WannaCry Killswitch Domain",
    4: "Possible Lateral Tool Transfer via SMB",
    5: "Remote System Discovery Via RPC",
    6: "Execution Via WMI",
    7: "Scheduled Task/Job Via At",
    8: "File Dir Discovery Via RPC",
    9: "Account Discovery Via RPC",
    10: "Network Share Discovery Via RPC",
    11: "Execution Via System Services",
    12: "Remote Schedule Task Lateral Movement via ITaskSchedulerService",
    13: "CobaltStrike Malleable OCSP Profile",
    14: "PwnDrp Access",
    15: "Spoolss Named Pipe Access via SMB",
    16: "Possible PsExec Execution",
    17: "Possible Windows Scheduled Task",
    18: "Possible Sensitive File Access",
    19: "Raw Paste Service Access",
    20: "Telegram API Access",
    21: "Crypto Miner User Agent",
    22: "Source Code Enumeration Detection by Keyword",
    23: "Cobalt Strike Command and Control Beacon",
    24: "Suspicious User Agent",
    25: "Suspicious Base64 Encoded User-Agent",
    26: "Communication To Ngrok Tunneling Service",
    27: "Suspicious Cobalt Strike DNS Beaconing",
    28: "DNS TXT Answer with Possible Execution Strings",
    29: "Potential Network Sweep Detected",
    30: "Potential Port Scan Detected",
    31: "Scheduled Task/Job Via Scheduled Task",
    32: "Detect Modbus Diagnostic - Force Listen Only Mode",
    33: "Detect Siemens SIMATIC S7 PLC STOP Command",
}

description_text = "CPSDR Simulation Script (Kali - Attacker)\n\nSupported Rules:\n"
for number, desc in rule_descriptions.items():
    description_text += f"  {number}: {desc}\n"

parser = argparse.ArgumentParser(
    description=description_text,
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-o", "--option", required=True, type=int, help="Rule number to simulate (e.g., 5, 29, 33)")
parser.add_argument("-t", "--target", help="Target IP or hostname")
parser.add_argument("-u", "--username", help="Username for authentication (if required)")
parser.add_argument("-p", "--password", help="Password for authentication (if required)")

args = parser.parse_args()

def target_required(rule_id):
    return rule_id in [1,2,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]

def auth_required(rule_id):
    return rule_id in [4,5,6,15,16]

def get_cred_str():
    return f"{args.username}%{args.password}"

def simulate_1(target):
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
        print(f"[!] Failed to connect: {e}")

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
        print(f"[!] Failed to connect: {e}")

def simulate_3(target=None):
    print("[+] Simulating WannaCry Killswitch Domain check...")
    killswitch_domain = "iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com"
    try:
        response = requests.get(f"http://{killswitch_domain}", timeout=5)
        print(f"[+] HTTP status: {response.status_code}")
    except Exception as e:
        print(f"[!] Expected failure or blocked domain (simulated): {e}")

def simulate_4(target):
    print(f"[+] Simulating SMB File Transfer to {target}...")
    subprocess.run(["smbclient", f"//{target}/share", "-U", get_cred_str(), "-c", "put /etc/passwd"])

def simulate_5(target):
    print(f"[+] Simulating RPC Discovery on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "enumdomusers"])

def simulate_6(target):
    print(f"[+] Simulating WMI Execution on {target}...")
    try:
        subprocess.run(["psexec.py", f"{args.username}:{args.password}@{target}", "ipconfig"], check=False)
    except Exception as e:
        print(f"[!] WMI execution failed: {e}")

def simulate_7(target):
    print(f"[+] Simulating Scheduled Task/Job via at on {target}...")
    subprocess.run(["at", "now + 1 minute", "/interactive", "cmd.exe"], check=False)

def simulate_8(target):
    print(f"[+] Simulating File/Directory Discovery via RPC on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "enumshares"], check=False)

def simulate_9(target):
    print(f"[+] Simulating Account Discovery via RPC on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "enumdomusers"], check=False)

def simulate_10(target):
    print(f"[+] Simulating Network Share Discovery via RPC on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "netshareenumall"], check=False)

def simulate_11(target):
    print(f"[+] Simulating Execution via System Services on {target}...")
    print("[!] Simulation not implemented yet.")

def simulate_15(target):
    print(f"[+] Simulating Spoolss Named Pipe Access on {target}...")
    subprocess.run(["rpcclient", "-U", get_cred_str(), target, "-c", "netshareenumall"])

def simulate_16(target):
    print(f"[+] Simulating Possible PsExec Execution on {target}...")
    try:
        subprocess.run(["psexec.py", f"{args.username}:{args.password}@{target}", "cmd.exe"], check=False)
    except Exception as e:
        print(f"[!] PsExec execution failed: {e}")

def simulate_24(target):
    print(f"[+] Sending Suspicious User-Agent to {target}...")
    headers = {"User-Agent": "python-requests/evil-miner"}
    try:
        requests.get(f"http://{target}", headers=headers, timeout=5)
    except Exception as e:
        print(f"[!] HTTP request failed: {e}")

def simulate_25(target):
    print(f"[+] Sending Base64 User-Agent to {target}...")
    b64_agent = base64.b64encode(b"malicious-agent").decode()
    headers = {"User-Agent": b64_agent}
    try:
        requests.get(f"http://{target}", headers=headers, timeout=5)
    except Exception as e:
        print(f"[!] HTTP request failed: {e}")

def simulate_29(target):
    print(f"[+] Running Nmap Sweep on {target}...")
    subprocess.run(["nmap", "-sn", target])

def simulate_30(target):
    print(f"[+] Running Full Port Scan on {target}...")
    subprocess.run(["nmap", "-p-", target])

def simulate_32(target):

    try:
        from pymodbus.client import ModbusTcpClient
    except ImportError:
        print("[!] pymodbus library is not installed. Please run: pip install pymodbus")
        sys.exit(1)
    
    print(f"[+] Detect Modbus Diagnostic (Force Listen Only Mode) on {target}...")
    client = ModbusTcpClient(target)
    if not client.connect():
        print("[!] Could not connect to Modbus server")
        return
    # Modbus diagnostic function code (function code 8, subfunction 4)
    from pymodbus.pdu import DiagnosticRequest
    rq = DiagnosticRequest(subfunction=4, data=0)
    response = client.execute(rq)
    print("[+] Sent Modbus diagnostic command")
    client.close()

def simulate_33(target):

    try:
        from snap7 import client as snap7_client
    except ImportError:
        print("[!] snap7 library is not installed. Please run: pip install python-snap7")
        sys.exit(1)
    
    print(f"[+] Detect Siemens SIMATIC S7 PLC STOP command on {target}...")
    plc = snap7_client.Client()
    try:
        plc.connect(target, 0, 1)  # rack=0, slot=1 (typical S7-300)
        print("[+] Connected to PLC - simulation complete")
        plc.disconnect()
    except Exception as e:
        print(f"[!] Failed to connect to PLC: {e}")

def main():
    rule_id = args.option
    target = args.target

    if target_required(rule_id) and not target:
        print("[!] Target IP/hostname is required for this rule.")
        sys.exit(1)

    if auth_required(rule_id) and (not args.username or not args.password):
        print("[!] Username and password are required for this rule.")
        sys.exit(1)

    simulate_func = globals().get(f"simulate_{rule_id}")
    if not simulate_func:
        print(f"[!] Simulation for rule {rule_id} is not implemented.")
        sys.exit(1)

    simulate_func(target)

if __name__ == "__main__":
    main()
