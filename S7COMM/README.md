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
python3 s7_test.py -t <PLC_IP> -r <RACK> -s <SLOT> -m <MODE> [OPTIONS]
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
python3 s7_test.py -t 192.168.0.100 -r 0 -s 1 -m db-read --db 1 --start 0 --size 4
```
- This will read 4 bytes from DB1 starting from address 0.

2. Write to a Data Block (DB)
```bash
python3 s7_test.py -t 192.168.0.100 -r 0 -s 1 -m db-write --db 1 --start 0 --value 1234
```
- This will write the integer value 1234 to DB1 starting from address 0.

3. Read PLC Inputs
```bash
python3 s7_test.py -t 192.168.0.100 -r 0 -s 1 -m inputs --size 2
```
- This will read 2 bytes from the input area.

4. Detect Job Function Code
```bash
python3 s7_test.py -t 192.168.0.100 -r 0 -s 1 -m job --job-code 0x1A
```
- This will detect the job function 0x1A.

5. Detect User Data Function Group and Sub-function
```bash
python3 s7_test.py -t 192.168.0.100 -r 0 -s 1 -m userdata --group-code 0x0 --sub-function 0x03
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

