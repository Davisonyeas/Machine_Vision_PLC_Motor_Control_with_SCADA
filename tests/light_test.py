from pymodbus.client import ModbusTcpClient
import time

PLC_IP = "192.168.0.1"  
client = ModbusTcpClient(host=PLC_IP, port=502)
client.connect()
print("Connected to PLC at", PLC_IP)

# hex y5  = 8196
COIL_ADDR = 8193

# Turn ON (trying simulate Start)
client.write_coil(address=COIL_ADDR, value=True)
print("Sent ON to C100 Green light should come ON")

time.sleep(10)

# Turn OFF again
client.write_coil(address=COIL_ADDR, value=False)
print("Sent OFF to C100 Green light should go OFF, please go off")

client.close()
