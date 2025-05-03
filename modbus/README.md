# Modbus Function Code Test Script
This script is designed to test a wide range of Modbus TCP function codes against a target server (e.g., ModRSsim2 running on Windows 7). It is compatible with detection systems like TXOne EdgeIPS and can simulate known Modbus behaviors for IPS rule verification.

## 🔧 Requirements
- Python 3.8+
- Install pymodbus:
```bash
pip install pymodbus
```

## 🚀 Usage
```bash
python3 modbus_test.py -t <target_ip> -o <function_code> [options]
```

## 📌 Arguments

| Argument | Description |
|----------|-------------|
| `-t`, `--target` |	Target Modbus server IP (e.g., `192.168.1.10`) [required] |
| `-p`, `--port` |	Modbus TCP port (default: 502) |
| `-o`, `--opcode` |	Modbus function code to test (e.g., `0x01`, `0x10`) [required] |
| `-v`, `--verbose` |	Enable debug-level output |
| `-l`, `--log`	| Log Modbus request/response |
| `-x`, `--hex`	| Print hex dump of communication |

## 🧪 Example Tests
```bash
# Test read coils (0x01)
python3 modbus_test.py -t 192.168.1.100 -o 0x01

# Test write multiple registers (0x10) with logging and hex dump
python3 modbus_test.py -t 192.168.1.100 -o 0x10 -v -l -x
```

## ✅ Supported Function Codes
This tool supports the following Modbus function codes used in industrial protocol security testing:

- `0x01`: Read Coils
- `0x02`: Read Discrete Inputs
- `0x03`: Read Holding Registers
- `0x04`: Read Input Registers
- `0x05`: Write Single Coil
- `0x06`: Write Single Register
- `0x0F`: Write Multiple Coils
- `0x10`: Write Multiple Registers
- `0x0B`: Get Comm Event Counter
- `0x0C`: Get Comm Event Log
- `0x11`: Report Server ID
- `0x14`: Read File Record (simulated)
- `0x15`: Write File Record (simulated)
- `0x16`: Mask Write Register (simulated)
- `0x18`: Read FIFO Queue (simulated)
- `0x2B`: Read Device Identification (simulated)
- `0x5A`: Encapsulated Interface Transport (simulated)


⚠️ Some codes like `0x14`, `0x15`, `0x16`, `0x18`, `0x2B`, and `0x5A` are simulated using generic read/write calls due to limited support in open libraries.

## 🛡 Use Cases

- Simulate known Modbus operations to trigger IPS rules.
- Validate protocol handling on legacy devices (e.g., Windows 7 + ModRSsim2).
- Reproduce OT attack surfaces for lab and demo purposes.
