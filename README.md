import time
from pymodbus.server.async_io import StartSerialServer
from pymodbus.datastore import ModbusSequentialDataStore
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

# Configure logging to see state changes
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Initialize data store
store = ModbusSequentialDataStore(
    coils=[False, False] * 50,  # Coils 00001, 00002, etc.
    holding_registers=[50, 0] * 50  # 40001=50 (gauge), 40002=0 (setpoint)
)
context = ModbusServerContext(slaves={1: store}, single=True)

# Function to log changes
def update_callback(args):
    address = args[0]
    value = args[1]
    if address == 0:  # Coil 00001
        log.info(f"Coil 00001 changed to {value}")
    elif address == 1:  # Coil 00002
        log.info(f"Coil 00002 changed to {value}")
    elif address == 0:  # Holding Register 40001 (gauge)
        log.info(f"Gauge (40001) updated to {value}")
    elif address == 1:  # Holding Register 40002 (setpoint)
        log.info(f"Setpoint (40002) updated to {value}")

# Start Modbus RTU server with callback for state changes
StartSerialServer(
    context,
    port='/dev/serial0',  # Adjust to your Pi's UART port (e.g., /dev/ttyS0)
    baudrate=9600,
    callback=update_callback
)
