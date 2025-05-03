from snap7 import client
from snap7.util import get_bool

# Set the IP address and port
PLC_IP = '172.23.32.32'  # The IP of your PLC (S7-PLCSIM1)
PLC_PORT = 102          # Default port for S7COMM

# Create the Snap7 client object
plc = client.Client()

# Connect to the PLC
plc.connect(PLC_IP, 0, 1)

if plc.connected():
    print(f"Connected to PLC at {PLC_IP}")

    # Read 1 byte from memory area M0 (Memory byte 0)
    data = plc.read_area(0x83, 0, 0, 1)  # 0x83 for DB, 0 for DB number, 0 offset, 1 byte size

    # Check the first byte for a boolean value
    first_bit = get_bool(data, 0, 0)  # Checking the first bit in the first byte

    print(f"First bit value: {first_bit}")

    # Disconnect from the PLC
    plc.disconnect()
else:
    print("Failed to connect to PLC.")
