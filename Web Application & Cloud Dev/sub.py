import paho.mqtt.client as mqtt
import os
from cryptography.fernet import Fernet

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"

cipher_key = b'CRBrxyF-tesWKVVc4QThoXSA--NmKMs4YYd_SIvjODE='
cipher = Fernet(cipher_key)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)
    
def on_message(client, userdata, msg):
    print("Message received ",str(msg.payload))
    
    print("Decrypting")
    
    decrypted_message = cipher.decrypt(msg.payload)
    
    print(decrypted_message)
    
    if decrypted_message == b'Vuln':
        os.system('echo Device Vulnerable > vuln_results.txt')
        
    elif decrypted_message == b'NotVuln':
        os.system('echo Device not vulnerable > vuln_results.txt')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
try:
    client.loop_forever()
except:
    print("error")
    