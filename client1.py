import paho.mqtt.client as mqtt
import time
import os

username = "task-planning"
password = "regalia risk sulfite corporal"
ip = ""
port = ""


def on_connect(client, userdata, flags, rc):
    print("on_connect callback: " + str(rc))

def on_message(client, obj, msg):
    print("msg from topic " + msg.topic + ": " + str(msg.payload))

def on_publish(client, obj, mid):
    print("on_publish callback: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

topic = 'test'

mqttc.will_set("dodsruna", "task_planning client is gone")

mqttc.tls_set()
mqttc.username_pw_set(username, password)
mqttc.connect(ip, port)

mqttc.loop_start()

mqttc.publish(topic, "hope this is working")
mqttc.subscribe(topic, 0)

mqttc.loop_forever()

