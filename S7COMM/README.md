# Advanced S7 Protocol Scanner

A Python-based scanner for Siemens S7 devices over ISO-on-TCP (port 102), designed for penetration testing and network diagnostics. This tool mimics certain Snap7 behaviors and explores supported job functions and user data subfunctions.

---

## ⚠️ Disclaimer

This tool is intended **solely for authorized testing and educational purposes**. Unauthorized scanning of industrial control systems (ICS) is illegal and dangerous. Always obtain proper permission before use.

---

## Features

- Scans Siemens S7 PLCs over port 102
- Supports two scan modes:
  - `job`: Sends S7 job function codes (e.g., Setup Communication, Read Var, etc.)
  - `userdata`: Sends S7 UserData function group and subfunction codes
- Customizable scan parameters (function codes, groups, and subfunctions)
- Built using raw socket and Scapy (without `scapy.contrib.s7comm`)

---

## Requirements

- Python 3.6+
- [Scapy](https://scapy.readthedocs.io/en/latest/)

Install Scapy via pip:

```bash
pip install scapy
```

## Usage

```bash
python3 s7_scan.py <target-ip> --mode <job|userdata> [options]
```
## Arguments

| Argument | Description |
|----------|-------------|
| `target` | Target IP address of the S7 device |
| `--port`	| TCP port to use (default: `102`) |
| `--mode` | Scan mode: job for S7 `job` functions or `userdata` for UserData functions |
| `--job-funcs` |	Comma-separated list of job function codes (e.g., `0x04,0xF0`) |
| `--user-groups` |	Comma-separated list of user data function groups (e.g., `0x0,0x3`) |
| `--user-subfuncs` |	Comma-separated list of subfunction codes (used only for FG 0x0) |

## Example Scans

**Default Job Scan**
```bash
python3 s7_scan_advanced.py 192.168.1.100 --mode job
```
**Custom Job Codes**
```bash
python3 s7_scan_advanced.py 192.168.1.100 --mode job --job-funcs 0x04,0x05
```
**Default UserData Scan**
```bash
python3 s7_scan_advanced.py 192.168.1.100 --mode userdata
```
**Specific UserData Group and Subfunctions**
```bash
python3 s7_scan_advanced.py 192.168.1.100 --mode userdata --user-groups 0x0 --user-subfuncs 0x00,0x03,0x09
```

## Output

The script prints each function or subfunction it sends, and whether the connection is successful. Responses are not deeply parsed unless implemented with further protocol logic.

## TODO

- Implement response parsing for known S7 function codes
- Add logging and PCAP output
- Add support for TLS (if applicable in newer S7 firmware)

# Snap7 S7Comm Test Tool

This script is designed to interact with Siemens S7 PLCs using the Snap7 library. It can perform various tasks, such as reading and writing data blocks (DB), reading PLC inputs and outputs, and detecting specific job and user data function codes in the communication protocol.

## Features

- **Connect to PLC**: Establish a connection to a Siemens PLC by providing the IP address, rack, and slot.
- **Read Data Blocks (DB)**: Read specific data blocks from the PLC.
- **Write to Data Blocks (DB)**: Write values (such as integers) to specific data blocks.
- **Read Inputs, Outputs, and Flags**: Read the state of inputs, outputs, and flags in the PLC.
- **Advanced Protocol Detection**: Detect job function codes and user data function groups and sub-functions.


## Requirements

- Python 3.x
- `snap7` library
- A Siemens S7 PLC with an accessible IP address

## Installation

1. Install Python 3 (if not already installed).
2. Install the `snap7` library:
```bash
pip install python-snap7
```

## Usage
**General Syntax*
```bash
python3 snap7_advanced_test.py -t <PLC_IP> -r <RACK> -s <SLOT> -m <MODE> [OPTIONS]
```
**Available Modes**
- `db-read`: Read data from a specified data block (DB).
- `db-write`: Write data to a specified data block (DB).
- `inputs`: Read PLC inputs.
- `outputs`: Read PLC outputs.
- `flags`: Read PLC flags.
- `all`: Perform all of the above actions (read inputs, outputs, flags, and DB).
- `job`: Detect job function codes.
- `userdata`: Detect user data function group and sub-function codes.

**Example Commands**
1. Read a Data Block (DB)
```bash
python3 snap7_advanced_test.py -t 192.168.0.100 -r 0 -s 1 -m db-read --db 1 --start 0 --size 4
```
- This will read 4 bytes from DB1 starting from address 0.

2. Write to a Data Block (DB)
```bash
python3 snap7_advanced_test.py -t 192.168.0.100 -r 0 -s 1 -m db-write --db 1 --start 0 --value 1234
```
- This will write the integer value 1234 to DB1 starting from address 0.

3. Read PLC Inputs
```bash
python3 snap7_advanced_test.py -t 192.168.0.100 -r 0 -s 1 -m inputs --size 2
```
- This will read 2 bytes from the input area.

4. Detect Job Function Code
```bash
python3 snap7_advanced_test.py -t 192.168.0.100 -r 0 -s 1 -m job --job-code 0x1A
```
- This will detect the job function 0x1A.

5. Detect User Data Function Group and Sub-function
```bash
python3 snap7_advanced_test.py -t 192.168.0.100 -r 0 -s 1 -m userdata --group-code 0x0 --sub-function 0x03
```
- This will detect the user data function group 0x0 and sub-function 0x03.


**Arguments**

`-t, --target`: The target PLC IP address (required).

`-r, --rack`: The PLC rack number (default: 0).

`-s, --slot`: The PLC slot number (default: 1).

`-m, --mode`: The mode to run (e.g., db-read, db-write, inputs, outputs, flags, all, job, userdata).

`--db`: The DB number for read/write (default: 1).

`--start`: The start byte address for read/write operations (default: 0).

`--size`: The size (in bytes) to read (default: 4).

`--value`: The value to write (used for db-write mode).

`--job-code`: The job function code (for job mode).

`--group-code`: The user data function group code (for userdata mode).

`--sub-function`: The sub-function code (for userdata mode).


## Example Output

**For Job Function Code Detection**
```bash
[+] Connecting to 192.168.0.100 (Rack=0, Slot=1)...
[+] Connected successfully!
[+] Detected Job Function: 0x1A
[*] Disconnected.
```
**For User Data Function Group Detection**
```bash
[+] Connecting to 192.168.0.100 (Rack=0, Slot=1)...
[+] Connected successfully!
[+] Detected User Data Function Group: 0x0
[*] Disconnected.
```

## Notes

Ensure that the PLC is accessible and that the IP, rack, and slot settings match your setup.
The script can handle various PLC areas (inputs, outputs, flags, data blocks) and provides useful diagnostic output for each operation.

## License

This project is licensed under the MIT License.

