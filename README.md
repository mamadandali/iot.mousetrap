import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

def write_coil(client, address, value, slave_id=1):
    rq = client.write_coil(address, value, unit=slave_id)
    if rq.isError():
        print(f"Error writing coil at address {address}")
        return False
    else:
        print(f"Coil at address {address} set to {value}")
        return True

if __name__ == "__main__":
    client = ModbusClient(
        method='ascii',        # or 'rtu'
        port='/dev/ttyUSB0',
        baudrate=9600,
        timeout=1
    )
    if not client.connect():
        print("Failed to connect to PLC")
        exit(1)

    coil_address = 1
    try:
        while True:
            write_coil(client, coil_address, True)   # Turn ON
            time.sleep(1)
            write_coil(client, coil_address, False)  # Turn OFF
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        client.close()
