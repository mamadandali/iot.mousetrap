from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusAsciiFramer

import logging
import random
import threading
import time

# تنظیم لاگر اصلی و pymodbus
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

modbus_logger = logging.getLogger("pymodbus")
modbus_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

modbus_logger.addHandler(console_handler)

# Modbus data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

# Device identity
identity = ModbusDeviceIdentification()
identity.VendorName = 'RaspberryPi'
identity.ProductName = 'Modbus ASCII Slave'

# Update register 40003 (address=2) with random value every second, with error handling
def update_register():
    while True:
        value = random.randint(0, 9999)
        try:
            # سعی می‌کنیم مقدار را بنویسیم
            context[0x00].setValues(3, 2, [value])
        except Exception as e:
            log.error(f"Error writing value {value} to register 40003 (address=2): {e}")
        time.sleep(1)

thread = threading.Thread(target=update_register, daemon=True)
thread.start()

# Start server
StartSerialServer(
    context=context,
    identity=identity,
    port='/dev/serial0',       # Adjust to your serial port
    baudrate=9600,
    stopbits=1,
    bytesize=7,                # 7 data bits as per your HMI
    parity='E',                # Even parity
    framer=ModbusAsciiFramer,
    slave_id=1                 # Set Raspberry Pi slave station number to 1
)
