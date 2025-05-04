#!/usr/bin/env python3

import argparse
import snap7
from snap7.util import *

# Function to parse hexadecimal input
def parse_hex(value):
    return int(value, 16)

def connect(ip, rack, slot):
    print(f"[+] Connecting to {ip} (Rack={rack}, Slot={slot})...")
    client = snap7.client.Client()
    client.connect(ip, rack, slot)
    if client.get_connected():
        print("[+] Connected successfully!")
        return client
    else:
        print("[-] Connection failed.")
        return None

def detect_job_function(job_code):
    job_list = [0x00, 0x04, 0x05, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x28, 0x29, 0xF0]
    if job_code in job_list:
        print(f"[+] Detected Job Function: 0x{job_code:02X}")
    else:
        print(f"[-] Unknown Job Function: 0x{job_code:02X}")

def detect_user_data_function_group(group_code):
    group_list = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7]
    if group_code in group_list:
        print(f"[+] Detected User Data Function Group: 0x{group_code:02X}")
    else:
        print(f"[-] Unknown Function Group: 0x{group_code:02X}")

def detect_sub_function_for_group(group_code, sub_function_code):
    sub_functions = {
        0x0: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x09, 0x0B, 0x0C],
        0x1: [0x00, 0x01, 0x02],
        0x2: [0x00, 0x01],
        # Add other group/sub-function mappings as necessary
    }
    
    if group_code in sub_functions:
        if sub_function_code in sub_functions[group_code]:
            print(f"[+] Detected Sub-function: Group 0x{group_code:02X}, Sub-function 0x{sub_function_code:02X}")
        else:
            print(f"[-] Unknown Sub-function for Group 0x{group_code:02X}: 0x{sub_function_code:02X}")
    else:
        print(f"[-] Unknown Function Group: 0x{group_code:02X}")

def read_db(client, db_num, start, size):
    print(f"[*] Reading DB{db_num}, Start: {start}, Size: {size}")
    data = client.db_read(db_num, start, size)
    print(f"[+] Raw DB Data: {data.hex()}")
    return data

def write_db(client, db_num, start, value):
    print(f"[*] Writing INT {value} to DB{db_num}, Start: {start}")
    data = bytearray(2)
    set_int(data, 0, value)
    client.db_write(db_num, start, data)
    print("[+] Write successful.")

def read_inputs(client, size=1):
    print(f"[*] Reading Inputs (size: {size})")
    data = client.read_area(0x81, 0, 0, size)  # Using area code 0x81 for inputs
    print(f"[+] Input bytes: {data.hex()}")

def read_outputs(client, size=1):
    print(f"[*] Reading Outputs (size: {size})")
    data = client.read_area(0x82, 0, 0, size)  # Using area code 0x82 for outputs
    print(f"[+] Output bytes: {data.hex()}")

def read_flags(client, size=1):
    print(f"[*] Reading Flags (size: {size})")
    data = client.read_area(0x83, 0, 0, size)  # Using area code 0x83 for flags
    print(f"[+] Flags: {data.hex()}")

def test_all(client):
    # Perform a sweep of various operations that simulate the kinds of S7COMM behaviors
    read_inputs(client)
    read_outputs(client)
    read_flags(client)
    read_db(client, db_num=1, start=0, size=4)
    write_db(client, db_num=1, start=0, value=1234)

def disconnect(client):
    client.disconnect()
    print("[*] Disconnected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Snap7 S7Comm Test Tool")
    parser.add_argument("-t", "--target", required=True, help="Target PLC IP address")
    parser.add_argument("-r", "--rack", type=int, default=0, help="PLC Rack number (default=0)")
    parser.add_argument("-s", "--slot", type=int, default=1, help="PLC Slot number (default=1)")
    parser.add_argument("-m", "--mode", choices=['db-read', 'db-write', 'inputs', 'outputs', 'flags', 'all', 'job', 'userdata'], default='all', help="Test mode to run")
    parser.add_argument("--db", type=int, default=1, help="DB number for read/write")
    parser.add_argument("--start", type=int, default=0, help="Start byte address")
    parser.add_argument("--size", type=int, default=4, help="Size of data to read")
    parser.add_argument("--value", type=int, help="Value to write (for db-write mode)")
    parser.add_argument("--job-code", type=parse_hex, help="Job function code to detect (for job mode)")
    parser.add_argument("--group-code", type=parse_hex, help="User data function group code to detect (for userdata mode)")
    parser.add_argument("--sub-function", type=parse_hex, help="Sub-function code to detect (for userdata mode)")

    args = parser.parse_args()
    client = connect(args.target, args.rack, args.slot)
    if not client:
        exit(1)

    try:
        if args.mode == 'db-read':
            read_db(client, args.db, args.start, args.size)
        elif args.mode == 'db-write':
            if args.value is None:
                print("[-] Please specify --value for db-write mode")
            else:
                write_db(client, args.db, args.start, args.value)
        elif args.mode == 'inputs':
            read_inputs(client, args.size)
        elif args.mode == 'outputs':
            read_outputs(client, args.size)
        elif args.mode == 'flags':
            read_flags(client, args.size)
        elif args.mode == 'all':
            test_all(client)
        elif args.mode == 'job' and args.job_code is not None:
            detect_job_function(args.job_code)
        elif args.mode == 'userdata':
            if args.group_code is not None:
                detect_user_data_function_group(args.group_code)
            if args.group_code is not None and args.sub_function is not None:
                detect_sub_function_for_group(args.group_code, args.sub_function)
    finally:
        disconnect(client)
