from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusRtuFramer
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Data blocks: 2 Holding registers, 2 Coils
store = ModbusSlaveContext(
    di=None,
    co={0: False, 1: False},        # Coils (B1 and B2 buttons)
    hr={0: 123, 1: 50},             # Holding registers (W40001, W40002)
    ir=None
)
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = 'RaspberryPi'
identity.ProductCode = 'RPIMB'
identity.VendorUrl = 'http://raspberrypi.org/'
identity.ProductName = 'Modbus RTU Slave'
identity.ModelName = 'RPI RTU'
identity.MajorMinorRevision = '1.0'

# Start RTU Slave on /dev/ttyUSB0 (adjust if needed)
StartSerialServer(
    context=context,
    identity=identity,
    port='/dev/ttyUSB0',     # Change this if needed
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N',
    framer=ModbusRtuFramer
)
