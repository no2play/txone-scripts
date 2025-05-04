#!/usr/bin/env python3

import argparse
import socket
import time

# Default function codes
DEFAULT_JOB_FUNCTIONS = [0x00, 0x04, 0x05, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x28, 0x29, 0xF0]
DEFAULT_USER_GROUPS = list(range(0x0, 0x8))
DEFAULT_USER_SUBFUNC_GROUP0 = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x09, 0x0B, 0x0C]

def connect_and_send(ip, port, mode, job_funcs=None, user_groups=None, user_subfuncs=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    try:
        sock.connect((ip, port))
        print(f"[+] Connected to {ip}:{port}")

        # Send ISO-on-TCP + COTP connection request
        iso = b"\x03\x00\x00\x16\x11\xe0\x00\x00\x00\x01\x00\xc1\x02\x01\x00\xc2\x02\x01\x02\xc0\x01\x09"
        sock.sendall(iso)
        resp = sock.recv(1024)

        for code in (job_funcs if mode == "job" else user_groups):
            if mode == "job":
                s7 = build_s7_job_request(code)
                print(f"[>] Sending Job Function Code: 0x{code:02X}")
                sock.sendall(build_tpkt(s7))
                time.sleep(0.2)
            else:
                if code == 0x00:
                    for sub in user_subfuncs or DEFAULT_USER_SUBFUNC_GROUP0:
                        s7 = build_s7_userdata_request(code, sub)
                        print(f"[>] Sending UserData FG:0x{code:02X} SF:0x{sub:02X}")
                        sock.sendall(build_tpkt(s7))
                        time.sleep(0.2)
                else:
                    s7 = build_s7_userdata_request(code, 0x00)
                    print(f"[>] Sending UserData FG:0x{code:02X} SF:0x00")
                    sock.sendall(build_tpkt(s7))
                    time.sleep(0.2)

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        sock.close()


def build_s7_job_request(func_code):
    """Build minimal S7 Job Request with given function code."""
    return bytes([
        0x32,       # Protocol ID
        0x01,       # ROSCTR: Job (0x01)
        0x00, 0x00, # Redundancy identification
        0x00, 0x01, # PDU reference
        0x00, 0x08, # Parameter length
        0x00, 0x00, # Data length
        func_code,  # Function code (varies)
        0x00,       # Reserved
        0x00, 0x00, # Additional param (if any)
    ])


def build_s7_userdata_request(func_group, subfunction):
    """Build minimal S7 UserData request."""
    return bytes([
        0x32,       # Protocol ID
        0x07,       # ROSCTR: UserData (0x07)
        0x00, 0x00, # Redundancy identification
        0x00, 0x01, # PDU reference
        0x00, 0x08, # Parameter length
        0x00, 0x00, # Data length
        0x00,       # Type
        0x00,       # Function group
        func_group, # Function group
        subfunction,# Subfunction
        0x00,       # Sequence number or reserved
        0x00, 0x00  # Other reserved fields
    ])


def build_tpkt(payload):
    """Wrap S7Comm payload in ISO-on-TCP + COTP + TPKT headers."""
    cotp = b'\x02\xf0\x80'
    tpkt_len = len(payload) + len(cotp) + 4
    tpkt = b'\x03\x00' + tpkt_len.to_bytes(2, 'big')
    return tpkt + cotp + payload


def parse_args():
    parser = argparse.ArgumentParser(description="Minimal S7 Scanner (No scapy.contrib)")
    parser.add_argument("target", help="Target IP address of the S7 device")
    parser.add_argument("--port", type=int, default=102, help="Target port (default: 102)")
    parser.add_argument("--mode", choices=["job", "userdata"], required=True, help="Scan mode")
    parser.add_argument("--job-funcs", help="Custom job function codes (e.g. 0x04,0xF0)")
    parser.add_argument("--user-groups", help="Custom user data function groups (e.g. 0x0,0x3)")
    parser.add_argument("--user-subfuncs", help="Subfunctions for FG 0x0 (e.g. 0x01,0x03)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    job_funcs = [int(x, 16) for x in args.job_funcs.split(',')] if args.job_funcs else DEFAULT_JOB_FUNCTIONS
    user_groups = [int(x, 16) for x in args.user_groups.split(',')] if args.user_groups else DEFAULT_USER_GROUPS
    user_subfuncs = [int(x, 16) for x in args.user_subfuncs.split(',')] if args.user_subfuncs else DEFAULT_USER_SUBFUNC_GROUP0

    connect_and_send(
        ip=args.target,
        port=args.port,
        mode=args.mode,
        job_funcs=job_funcs,
        user_groups=user_groups,
        user_subfuncs=user_subfuncs
    )
