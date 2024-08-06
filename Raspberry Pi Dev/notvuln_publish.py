import paho.mqtt.publish as publish

mqtt_broker_address = "192.168.1.137"
mqtt_channel = "test_channel"

message = "NotVuln"

publish.single(mqtt_channel, message, hostname=mqtt_broker_address)
