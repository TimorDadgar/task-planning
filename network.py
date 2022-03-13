import paho.mqtt.client as mqtt
import json
from htn_planner import *

username = "task-planning"
password = "regalia risk sulfite corporal"
ip = "tharsis.oru.se"
port = 8883
topics = ["motion_planning", "mission_control", "perception", "simulation"]
QOS_level = 0


def on_connect(client, userdata, flags, rc):
    print("on_connect callback: " + str(rc))


def on_message(client, obj, msg):
    print("msg from topic " + msg.topic + ": " + str(msg.payload))
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    data = json.loads(m_decode)

    if msg.topic == "motion_planning":
        if str(msg.payload) == "fail":
            print("inside motion_planning topic handler")

        else:
            print("inside else statement in motion_planning topic handler")

    elif msg.topic == "mission_control":
        print("inside mission_control topic handler")
        print("printing received data", data)
        set_info_from_mission_control(data)

    elif msg.topic == "perception":
        print("inside perception topic handler")
        set_info_from_perception(data)

    elif msg.topic == "simulation/robot/position":
        print("inside simulation topic handler")
        set_info_from_simulation(data)

    elif msg.topic == "simulation/sensor/status/":
        print("inside simulation topic handler")
        set_info_from_simulation(data)
        # handle msg.payload


def on_publish(client, obj, mid):
    print("on_publish callback: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


class Network:
    def __init__(self):
        self.client = mqtt.Client()

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe

        self.client.username_pw_set(username, password)
        self.client.tls_set()
        self.client.connect(ip, port)

        self.client.will_set("dodsruna", "task_planning client is gone")
        for i in topics:
            self.client.subscribe(i, QOS_level)

        self.client.loop_forever()

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()
