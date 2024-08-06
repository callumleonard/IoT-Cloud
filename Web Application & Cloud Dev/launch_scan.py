import paho.mqtt.publish as publish
from cryptography.fernet import Fernet

mqtt_broker_address = "192.168.1.132"
mqtt_channel = "test_channel"

cipher_key = b'CRBrxyF-tesWKVVc4QThoXSA--NmKMs4YYd_SIvjODE='
cipher = Fernet(cipher_key)

message = b'StartScan'
encrypted_message = cipher.encrypt(message)
out_message = encrypted_message.decode() #turn encrypted msg into a string to send

publish.single(mqtt_channel, out_message, hostname=mqtt_broker_address)