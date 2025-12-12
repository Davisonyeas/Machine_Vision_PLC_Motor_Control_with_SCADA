from pymodbus.client import ModbusTcpClient
import time
# seting pulse rate to 50ms

PLC_IP = "192.168.0.1"
client = ModbusTcpClient(host=PLC_IP, port=502)
client.connect()

def pulse(addr):
    # FC5 write single coil
    client.write_coil(address=addr, value=True)
    time.sleep(0.05)  
    client.write_coil(address=addr, value=False)

for addr in (99, 100):           
    print(f"Trying C100 at coil addr {addr}")
    pulse(addr)
    rb = client.read_coils(address=addr, count=1)
    print("Readback:", (not rb.isError()) and rb.bits)

client.close()
