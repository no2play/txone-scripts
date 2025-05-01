# 🛡️ TXOne Edge IPS Test Suite

This repository contains automated test scripts to evaluate and validate the behavior and effectiveness of **TXOne Edge IPS** under various threat scenarios. These tests are designed for use in controlled OT/ICS lab environments to simulate real-world attack conditions and verify IPS detection and response.

## 📚 Test Cases Overview

| Test Case ID | Test Name                     | Description                               |
|--------------|-------------------------------|-------------------------------------------|
| TC-01        | DoS Protection (SYN Flood)     | Simulates a SYN flood attack to verify DoS detection, logging, and mitigation. |
| TC-02        | *(Coming Soon)*                | Example: Protocol Abuse – Modbus Scan     |
| TC-03        | *(Coming Soon)*                | Example: Unauthorized File Transfer       |
| TC-04        | *(Coming Soon)*                | Example: L2 MAC Spoofing Detection        |
| ...          | *(More test cases coming)*     |                                           |

---

## ✅ Prerequisites

- **TXOne Edge IPS** deployed in **inline** or **bridge mode**.
- At least one OT asset (e.g., PLC, HMI) reachable from test host.
- Rulesets enabled for the test case being executed.
- Test machine (e.g., Kali Linux or Linux workstation) with:
  - Python 3.x
  - `hping3`, `nping`, `slowloris`, or other required tools
  - Root access (for raw packet tools)

---

## 🚀 Running a Test

Each test script is a standalone Python file. To run a test:

```bash
sudo python3 <script_name>.py <TARGET-IP> <DURATION/OPTIONS>
