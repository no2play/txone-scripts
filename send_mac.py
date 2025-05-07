#!/usr/bin/env python3

import argparse
from scapy.all import Ether, sendp, conf

def main():
    parser = argparse.ArgumentParser(description="Send raw Ethernet frames from source MAC to target MAC.")
    parser.add_argument("-t", "--target", required=True, help="Target MAC address")
    parser.add_argument("-s", "--source", required=True, help="Source MAC address")
    parser.add_argument("-i", "--interface", default=conf.iface, help="Network interface (default: Scapy default)")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of frames to send (default: 1)")
    parser.add_argument("-p", "--payload", default="HelloMAC", help="Custom payload string (default: 'HelloMAC')")

    args = parser.parse_args()

    # Build the Ethernet frame
    frame = Ether(dst=args.target, src=args.source, type=0x1234) / args.payload.encode()

    # Send the frame
    print(f"Sending {args.count} Ethernet frame(s) from {args.source} to {args.target} on {args.interface}")
    sendp(frame, iface=args.interface, count=args.count, verbose=True)

if __name__ == "__main__":
    main()
