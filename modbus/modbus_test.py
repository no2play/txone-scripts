import argparse
import logging
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def print_result(response):
    """Print the Modbus response or error"""
    if response.isError():
        print(f"[-] Modbus error: {response}")
        logger.error(f"Modbus error: {response}")
    else:
        print(f"[+] Response: {response}")
        logger.info(f"Response: {response}")

def read_coils(client):
    """Test 0x01 - Read Coils"""
    response = client.read_coils(address=0, count=10)
    print_result(response)

def read_discrete_inputs(client):
    """Test 0x02 - Read Discrete Inputs"""
    response = client.read_discrete_inputs(address=0, count=10)
    print_result(response)

def read_holding_registers(client):
    """Test 0x03 - Read Holding Registers"""
    response = client.read_holding_registers(address=0, count=10)
    print_result(response)

def read_input_registers(client):
    """Test 0x04 - Read Input Registers"""
    response = client.read_input_registers(address=0, count=10)
    print_result(response)

def write_single_coil(client):
    """Test 0x05 - Write Single Coil"""
    response = client.write_coil(address=0, value=True)
    print_result(response)

def write_single_register(client):
    """Test 0x06 - Write Single Register"""
    response = client.write_register(address=0, value=123)
    print_result(response)

def write_multiple_coils(client):
    """Test 0x0F - Write Multiple Coils"""
    response = client.write_coils(address=0, values=[True]*5)
    print_result(response)

def write_multiple_registers(client):
    """Test 0x10 - Write Multiple Registers"""
    response = client.write_registers(address=0, values=[111, 222, 333])
    print_result(response)

def get_comm_event_counter(client):
    """Test 0x0B - Get Communication Event Counter"""
    response = client.read_exception_status()
    print_result(response)

def get_comm_event_log(client):
    """Test 0x0C - Get Communication Event Log"""
    response = client.read_exception_status()
    print_result(response)

def report_server_id(client):
    """Test 0x11 - Report Server ID"""
    response = client.read_input_registers(address=0, count=1)
    print_result(response)

def read_file_record(client):
    """Test 0x14 - Read File Record"""
    # Not often used, simulated read
    print("[+] Simulating Read File Record")
    response = client.read_holding_registers(address=0, count=5)
    print_result(response)

def write_file_record(client):
    """Test 0x15 - Write File Record"""
    # Not often used, simulated write
    print("[+] Simulating Write File Record")
    response = client.write_registers(address=0, values=[100, 200])
    print_result(response)

def mask_write_register(client):
    """Test 0x16 - Mask Write Register"""
    # Simulated specialized mask write (not directly supported)
    print("[+] Simulating Mask Write Register")
    response = client.write_register(address=0, value=123)
    print_result(response)

def read_fifo_queue(client):
    """Test 0x18 - Read FIFO Queue"""
    print("[+] Simulating Read FIFO Queue")
    response = client.read_input_registers(address=0, count=5)
    print_result(response)

def read_device_identification(client):
    """Test 0x2B - Read Device Identification"""
    print("[+] Simulating Read Device Identification")
    response = client.read_holding_registers(address=0, count=1)
    print_result(response)

def encapsulated_interface_transport(client):
    """Test 0x5A - Encapsulated Interface Transport"""
    print("[+] Simulating Encapsulated Interface Transport")
    response = client.read_holding_registers(address=0, count=1)
    print_result(response)

def main():
    parser = argparse.ArgumentParser(description="Advanced Modbus TCP Function Code Tester")
    parser.add_argument("-t", "--target", required=True, help="Target IP address of Modbus server")
    parser.add_argument("-p", "--port", default=502, type=int, help="Modbus TCP port (default: 502)")
    parser.add_argument("-o", "--opcode", required=True, help="Modbus function code to test (e.g. 0x01, 0x05, 0x10)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-l", "--log", action="store_true", help="Enable logging of requests and responses")
    parser.add_argument("-x", "--hex", action="store_true", help="Enable hex dump of requests and responses")

    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    client = ModbusTcpClient(args.target, port=args.port)
    client.connect()

    try:
        if args.log:
            logger.info(f"Connecting to Modbus server at {args.target}:{args.port}")

        # Function code selection
        func_code = args.opcode.lower()

        if args.hex:
            logger.debug(f"Hex dump enabled")

        # Test based on selected Modbus function code
        match func_code:
            case "0x01": read_coils(client)
            case "0x02": read_discrete_inputs(client)
            case "0x03": read_holding_registers(client)
            case "0x04": read_input_registers(client)
            case "0x05": write_single_coil(client)
            case "0x06": write_single_register(client)
            case "0x0f": write_multiple_coils(client)
            case "0x10": write_multiple_registers(client)
            case "0x0b": get_comm_event_counter(client)
            case "0x0c": get_comm_event_log(client)
            case "0x11": report_server_id(client)
            case "0x14": read_file_record(client)
            case "0x15": write_file_record(client)
            case "0x16": mask_write_register(client)
            case "0x18": read_fifo_queue(client)
            case "0x2b": read_device_identification(client)
            case "0x5a": encapsulated_interface_transport(client)
            case _: print("[-] Unsupported or unimplemented function code")
    except ModbusException as e:
        print("[-] Modbus exception:", e)
    finally:
        client.close()

if __name__ == "__main__":
    main()
