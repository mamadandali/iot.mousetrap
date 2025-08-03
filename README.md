from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Initialize coils (discrete outputs)
# coils indexed from 0, set coil 0 and 1 to False
initial_coils = [False, False]

# Initialize holding registers with your values
# hr[0] = 123, hr[1] = 50
initial_hr = [123, 50]

# Create the data blocks with initial values
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, []),              # No discrete inputs
    co=ModbusSequentialDataBlock(0, initial_coils),   # Coils B1 and B2 buttons
    hr=ModbusSequentialDataBlock(0, initial_hr),      # Holding registers W40001=123, W40002=50
    ir=ModbusSequentialDataBlock(0, [])               # No input registers
)

context = ModbusServerContext(slaves=store, single=True)

def run_modbus_rtu_server():
    StartSerialServer(
        context,
        port='/dev/serial0',     # Change if needed (e.g. '/dev/ttyUSB0')
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1,
        framer=None
    )

if __name__ == "__main__":
    print("Starting Modbus RTU slave with preset coils and registers...")
    run_modbus_rtu_server()
