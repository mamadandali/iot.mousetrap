from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(
    method='ascii',        # یا 'rtu' اگه متد شما RTU هست
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=7,
    parity='E',
    stopbits=1,
    timeout=1
)

if client.connect():
    # تلاش برای خواندن 1 کویل از آدرس 1
    rr = client.read_coils(1, 1, unit=1)
    if rr.isError():
        print("Error reading coil")
    else:
        print(f"Coil status at address 1: {rr.bits[0]}")
    client.close()
else:
    print("Failed to connect")
