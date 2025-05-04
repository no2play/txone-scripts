import argparse
import snap7
from snap7.util import *
from snap7 import client

# Define area constants as required
PE = 0x81  # Inputs (PE)
PA = 0x82  # Outputs (PA)
MK = 0x83  # Flags (MK)

def connect(ip, rack, slot):
    print(f"[+] Connecting to {ip} (Rack={rack}, Slot={slot})...")
    plc_client = snap7.client.Client()
    plc_client.connect(ip, rack, slot)
    if plc_client.get_connected():
        print("[+] Connected successfully!")
        return plc_client
    else:
        print("[-] Connection failed.")
        return None

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
    data = client.read_area(PE, 0, 0, size)
    print(f"[+] Input bytes: {data.hex()}")

def read_outputs(client, size=1):
    print(f"[*] Reading Outputs (size: {size})")
    data = client.read_area(PA, 0, 0, size)
    print(f"[+] Output bytes: {data.hex()}")

def read_flags(client, size=1):
    print(f"[*] Reading Flags (size: {size})")
    data = client.read_area(MK, 0, 0, size)
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
    parser.add_argument("-m", "--mode", choices=['db-read', 'db-write', 'inputs', 'outputs', 'flags', 'all'], default='all', help="Test mode to run")
    parser.add_argument("--db", type=int, default=1, help="DB number for read/write")
    parser.add_argument("--start", type=int, default=0, help="Start byte address")
    parser.add_argument("--size", type=int, default=4, help="Size of data to read")
    parser.add_argument("--value", type=int, help="Value to write (for db-write mode)")

    args = parser.parse_args()
    plc_client = connect(args.target, args.rack, args.slot)
    if not plc_client:
        exit(1)

    try:
        if args.mode == 'db-read':
            read_db(plc_client, args.db, args.start, args.size)
        elif args.mode == 'db-write':
            if args.value is None:
                print("[-] Please specify --value for db-write mode")
            else:
                write_db(plc_client, args.db, args.start, args.value)
        elif args.mode == 'inputs':
            read_inputs(plc_client, args.size)
        elif args.mode == 'outputs':
            read_outputs(plc_client, args.size)
        elif args.mode == 'flags':
            read_flags(plc_client, args.size)
        elif args.mode == 'all':
            test_all(plc_client)
    finally:
        disconnect(plc_client)
