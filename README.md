from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.factory import ServerDecoder
from pymodbus.pdu import ModbusRequest
import logging

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s - %(message)s',
    level=logging.INFO
)
log = logging.getLogger()

# ─────────────────────────────────────
# Custom context to log read/write
class LoggingSlaveContext(ModbusSlaveContext):
    def getValues(self, fx, address, count=1):
        log.info(f"[READ] Function={fx}, Address={address}, Count={count}")
        return super().getValues(fx, address, count)

    def setValues(self, fx, address, values):
        log.info(f"[WRITE] Function={fx}, Address={address}, Values={values}")
        return super().setValues(fx, address, values)

# ─────────────────────────────────────
# Setup slave data store
store = LoggingSlaveContext(
    di=None,
    co={0: False, 1: False},  # Coils
    hr={0: 123, 1: 50},       # Holding Registers
    ir=None
)
context = ModbusServerContext(slaves=store, single=True)

# ─────────────────────────────────────
# Identity info
identity = ModbusDeviceIdentification()
identity.VendorName = 'RaspberryPi'
identity.ProductCode = 'RPIMB'
identity.VendorUrl = 'http://raspberrypi.org/'
identity.ProductName = 'Modbus RTU Slave'
identity.ModelName = 'RPI RTU'
identity.MajorMinorRevision = '1.0'

# ─────────────────────────────────────
# Start Serial Server with custom handler
def request_logger(request: ModbusRequest):
    log.info(f"[REQUEST] {request}")
    return request

decoder = ServerDecoder()
decoder.register(request_logger)  # Register the logger

StartSerialServer(
    context=context,
    identity=identity,
    port='/dev/ttyUSB0',    # Adjust if needed
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N',
    framer=ModbusRtuFramer
)
