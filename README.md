from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusRtuFramer
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

initial_coils = [False, False]
initial_hr = [123, 50]

store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, []),
    co=ModbusSequentialDataBlock(0, initial_coils),
    hr=ModbusSequentialDataBlock(0, initial_hr),
    ir=ModbusSequentialDataBlock(0, [])
)

context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = 'RaspberryPi'
identity.ProductCode = 'RPIMB'
identity.VendorUrl = 'http://raspberrypi.org/'
identity.ProductName = 'Modbus RTU Slave'
identity.ModelName = 'RPI RTU'
identity.MajorMinorRevision = '1.0'

StartSerialServer(
    context=context,
    identity=identity,
    port='/dev/ttyUSB0',   # Change if needed
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N',
    framer=ModbusRtuFramer
)
