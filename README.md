from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusAsciiFramer
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

store = ModbusSlaveContext(
    di=None,
    co={0: False, 1: False},
    hr={0: 123, 1: 50},
    ir=None
)
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = 'RaspberryPi'
identity.ProductName = 'Modbus ASCII Slave'

StartSerialServer(
    context=context,
    identity=identity,
    port='/dev/serial0',  # or '/dev/ttyS0' or '/dev/ttyAMA0' depending on your Pi
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N',
    framer=ModbusAsciiFramer
)
