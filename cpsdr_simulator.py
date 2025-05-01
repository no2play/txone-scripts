#!/usr/bin/env python3

import argparse
import subprocess
import sys
import time

def simulate(option, target_ip):
    print(f"[+] Selected pattern {option} for target {target_ip}...")

    try:
        if option == 1:
            print("[+] Simulating BabyShark Agent Pattern...")
            subprocess.run(["curl", "-A", "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko", f"http://{target_ip}/index.html"])

        elif option == 2:
            print("[+] Simulating Cobalt Strike Malleable Profile...")
            subprocess.run(["curl", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36", f"http://{target_ip}/update"])

        elif option == 3:
            print("[+] Simulating WannaCry Killswitch Domain...")
            subprocess.run(["curl", "http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com"])

        elif option == 4:
            print("[+] Simulating SMB Lateral Tool Transfer...")
            subprocess.run(["smbclient", f"//{target_ip}/C$", "-U", "guest", "-c", "dir"])

        elif option == 6:
            print("[+] Simulating Execution via WMI...")
            subprocess.run(["wmic", f"/node:{target_ip}", "process", "call", "create", "notepad.exe"])

        elif option == 13:
            print("[+] Simulating Cobalt Strike OCSP Profile...")
            subprocess.run(["curl", "-k", "-H", "Host: ocsp.verisign.com", f"https://{target_ip}/ocsp"])

        elif option == 14:
            print("[+] Simulating PwnDrp Access...")
            subprocess.run(["curl", "-A", "PwnDrp", f"http://{target_ip}/malware.exe"])

        elif option == 19:
            print("[+] Simulating Raw Paste Service Access...")
            subprocess.run(["curl", "https://pastebin.com/raw/abc123"])

        elif option == 20:
            print("[+] Simulating Telegram API Access...")
            subprocess.run(["curl", "https://api.telegram.org/bot<token>/getUpdates"])

        elif option == 23:
            print("[+] Simulating Cobalt Strike Beacon Traffic...")
            subprocess.run(["curl", "-A", "Mozilla/5.0 Beacon", f"http://{target_ip}/submit.php"])

        elif option == 24:
            print("[+] Simulating Suspicious User-Agent...")
            subprocess.run(["curl", "-A", "python-requests/2.27.1", f"http://{target_ip}/test"])

        elif option == 25:
            print("[+] Simulating Suspicious Base64 Encoded User-Agent...")
            b64_agent = "TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEwOyBNT0JJTCBCVUVJRCAzMC4wLjApIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84Ni4wLjQ0MzAvODguMC4zMzI5LjEwMA=="
            subprocess.run(["curl", "-A", b64_agent, f"http://{target_ip}/data"])

        else:
            print("[!] Invalid option. Use -h to see available patterns.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("[!] Interrupted by user.")
    except Exception as e:
        print(f"[!] Error during simulation: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TXOne Edge IPS CPSDR Event Simulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-o", "--option", type=int, required=True,
                        help="Simulation option number (see below)")
    parser.add_argument("-t", "--target", required=True,
                        help="Target IP address or domain")

    args = parser.parse_args()
    simulate(args.option, args.target)
