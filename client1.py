import paho.mqtt.client as mqtt
import time
import os
import json


username = "task-planning"
password = "regalia risk sulfite corporal"
ip = "tharsis.oru.se"
port = 8883


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

topic = 'mission_control'

points = [{
        "command": "goto",
        "x": 122,
        "y": 78,
        "id": 0
    },
    {
        "command": "sensor-drop",
        "x": 20,
        "y": 10,
        "id": 1
    }]

data_out = json.dumps(points)     # encode object to JSON

mqttc.username_pw_set(username, password)
mqttc.tls_set()
mqttc.connect(ip, port)
mqttc.will_set("dodsruna", "task_planning client is gone")
mqttc.loop_start()
mqttc.publish(topic, payload=data_out)
mqttc.loop_stop()



