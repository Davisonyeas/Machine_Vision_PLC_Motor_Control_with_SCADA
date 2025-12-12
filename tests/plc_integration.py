import os
import sys
import time
import paho.mqtt.client as mqtt
from pymodbus.client import ModbusTcpClient
# from ..realtime_recogition import recognize_face

IP = "192.168.0.1"
PORT = 502
MOD_ADDR = 0
# MQTT_HOST = "127.0.0.1"
MQTT_HOST = "localhost"
MQTT_PORT = 1883
client_id="sac/face/label"
topic_detect = "sac/face/label"

#pseudo cide for integration
# connect to broker
# subscribe to topic
# callback 
# MQTT succes 

# write to plc based on the message received

# client = mqtt.Client(
#     client_id="sac/face/label",
#     protocol=mqtt.MQTTv311,
#     transport="tcp",
#     callback_api_version=mqtt.CallbackAPIVersion.VERSION2
# )

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc, properties=None):
        print("MQTT Connected" if rc == 0 else f"Failed COnnection, {rc}")

    client = mqtt.Client(
        client_id=client_id, 
        protocol=mqtt.MQTTv311,
        transport="tcp",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT)
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received {msg.payload.decode()} from topic - {msg.topic}")

        message_detect = msg.payload.decode()
        def pulse_plc(message):
            # connect to plc
            mod_client = ModbusTcpClient(IP, port=PORT)
            mod_client.connect()
            print("Connected to Modbus Server")

            if message != "NoFace":
                rb = mod_client.read_coils(MOD_ADDR, count=1)
                print("rb", rb)
                print(f"Current State is = {rb if not rb.isError() else rb}")
                mod_client.write_coil(address=MOD_ADDR, value=True)
                time.sleep(1)
                print(f"After State is = {rb if not rb.isError() else rb}")

            else:
                print("UNKNOWN")

        pulse_plc(message_detect)

    client.subscribe(topic_detect)
    client.on_message = on_message 

def run():
    clien = connect_mqtt()
    subscribe(clien)
    clien.loop_forever()

if __name__ == "__main__":
    run()



print("Done with other file")

