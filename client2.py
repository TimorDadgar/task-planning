import paho.mqtt.client as mqtt
import time
import os

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("on_connect callback: " + str(rc))


def on_message(client, obj, msg):
    print("msg from topic " + msg.topic + ": " + str(msg.payload))


def on_publish(client, obj, mid):
    print("on_publish callback: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
topic = 'test'
topic2 = 'dodsruna'
topic3 = 'dogo'

# Connect
#mqttc.username_pw_set("admin", "1997")
mqttc.connect("92.34.73.176", 1234)

# Start subscribe, with QoS level 0
mqttc.subscribe(topic, 0)
mqttc.subscribe(topic2, 0)
mqttc.subscribe(topic3, 0)

##### OPTION 2 #####
# loop forever, implement the callbacks to do something
mqttc.loop_forever()