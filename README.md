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
        method='rtu',            # اکثر PLCهای دلتا RTU استفاده می‌کنند
        port='/dev/ttyUSB0',     # پورت سریال USB روی رزبری پای
        baudrate=9600,
        bytesize=7,              # تنظیمات دیتابیت و پاریتی طبق PLC
        parity='E',              # Even parity
        stopbits=1,
        timeout=1
    )

    if not client.connect():
        print("Failed to connect to PLC")
        exit(1)

    # آدرس واقعی کویل Y0 طبق جدول - 1281 منهای 1280 = 1
    coil_address = 1

    try:
        while True:
            write_coil(client, coil_address, True)   # روشن کردن کویل
            time.sleep(1)
            write_coil(client, coil_address, False)  # خاموش کردن کویل
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        client.close()
