from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

initial_coils = [False]*10
initial_hr = [0]*10
initial_hr[0] = 123
initial_hr[1] = 50

store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, []),              
    co=ModbusSequentialDataBlock(0, initial_coils),   
    hr=ModbusSequentialDataBlock(0, initial_hr),      
    ir=ModbusSequentialDataBlock(0, [])               
)

context = ModbusServerContext(slaves=store, single=True)

def run_modbus_rtu_server():
    StartSerialServer(
        context,
        port='/dev/serial0',    
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1,
        framer=None
    )

if __name__ == "__main__":
    print("Starting Modbus RTU slave server...")
    run_modbus_rtu_server()
