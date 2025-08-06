from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusAsciiFramer

import logging
import random
import threading
import time

# Enable logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

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

# Update register 40003 (address=2) with random value every second
def update_register():
    while True:
        value = random.randint(0, 9999)
        log.info(f"Writing {value} to register 40003 (address=2)")
        context[0x00].setValues(3, 2, [value])
        time.sleep(1)

thread = threading.Thread(target=update_register, daemon=True)
thread.start()

# Start server with updated parameters
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
