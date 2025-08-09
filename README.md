import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

def write_coil(client, address, value=True, slave_id=1):
    rq = client.write_coil(address, value, unit=slave_id)
    if rq.isError():
        print(f"Error writing coil at address {address}")
        return False
    else:
        print(f"Coil {address} set to {value}")
        return True

if __name__ == "__main__":
    client = ModbusClient(
        method='ascii',          # or 'rtu' if your PLC uses RTU
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=7,
        parity='E',
        stopbits=1,
        timeout=1
    )

    if not client.connect():
        print("Failed to connect to PLC")
        exit(1)

    address = 1

    try:
        while True:
            write_coil(client, address, True)
            address += 1
            time.sleep(0.05)  # 50 milliseconds
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        client.close()
