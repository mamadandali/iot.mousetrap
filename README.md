from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusAsciiFramer
import logging

# Enable request logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0, 0]),
    hr=ModbusSequentialDataBlock(0, [123, 50]),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

# Device identity (optional)
identity = ModbusDeviceIdentification()
identity.VendorName = 'RaspberryPi'
identity.ProductName = 'Modbus ASCII Slave'

# Start Modbus ASCII server
StartSerialServer(
    context=context,
    identity=identity,
    port='/dev/serial0',     # Adjust if needed
    baudrate=9600,
    stopbits=1,
    bytesize=7,              # ASCII usually requires 7 data bits
    parity='E',              # or 'N' based on your HMI settings
    framer=ModbusAsciiFramer
)
