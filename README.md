from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusAsciiFramer
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)
log = logging.getLogger()

class LoggingSlaveContext(ModbusSlaveContext):
    def getValues(self, fx, address, count=1):
        log.info(f"READ → Function={fx}, Address={address}, Count={count}")
        return super().getValues(fx, address, count)

    def setValues(self, fx, address, values):
        log.info(f"WRITE → Function={fx}, Address={address}, Values={values}")
        return super().setValues(fx, address, values)

store = LoggingSlaveContext(
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
    port='/dev/serial0',  # Adjust if needed (e.g. /dev/ttyAMA0 or USB0)
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N',
    framer=ModbusAsciiFramer
)
