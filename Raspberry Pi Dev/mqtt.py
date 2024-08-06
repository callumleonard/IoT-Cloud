import paho.mqtt.client as mqtt
import os

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    print("Message received ",str(msg.payload))
    message = str(msg.payload)
    topic = str(msg.topic)

    print(message)
    if message == "StartScan":
	os.system('python vulnerability_scanner.py')
	os.system('python vuln_checker.py')
    if message == "exploit":
        os.system('sudo python3 ss.py')
    elif message == "off":
        os.system('touch new.txt')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
try:
    client.loop_forever()
except:
    print("error")
