# TXOne Edge IPS DoS Protection Test Suite

This repository contains a collection of test scripts designed to validate DoS protection capabilities in TXOne Edge IPS.

## DoS Protection Tests

This suite includes tests for various types of DoS attacks, leveraging the following attack types:
- TCP SYN Flood
- UDP Flood
- ICMP Flood
- TCP SYN Scan
- TCP NULL Scan
- TCP Xmas Scan
- Ping Sweep

## Prerequisites

- **TXOne Edge IPS** is deployed inline or in bridge mode between the attacker and target OT device.
- At least one OT asset (e.g., PLC or HMI) is accessible on the network.
- The IPS rule set includes default or custom DoS protection rules.
- **Test Workstation**: Kali Linux or another system with `hping3`, `nmap`, or similar tools installed.

## Available Tests

This test suite includes the following attack types:

- **TCP SYN Flood**
- **UDP Flood**
- **ICMP Flood**
- **TCP SYN Scan**
- **TCP NULL Scan**
- **TCP Xmas Scan**
- **Ping Sweep**

## Usage

To run a DoS attack test, use the following command structure:

```bash
python3 test-dos-attack.py <attack_type> <target_ip> <duration>
