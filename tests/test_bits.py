from pymodbus.client import ModbusTcpClient
import time
# fast pulse test sync btw plc and pi
# todo - check latency and if syc works, real-time sync between all device **remember**

ip = "192.168.0.1"
c  = ModbusTcpClient(ip, port=502)
c.connect()

def pulse(addr, name):
    print(f"\nPulsing coil addr {addr} ({name})")
    c.write_coil(address=addr, value=True)
    time.sleep(0.2)
    rb = c.read_coils(address=addr, count=1)
    print("Readback:", rb.bits if not rb.isError() else rb)
    c.write_coil(address=addr, value=False)
    time.sleep(0.1)


for a,n in [(0,"C1"), (1,"C2"), (2,"C3"), (3,"C4"), (4,"C5"), (99,"C100"), (100,"C101")]:
    pulse(a,n)

c.close()
