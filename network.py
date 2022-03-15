import paho.mqtt.client as mqtt
import json
from htn_planner import *

username = "task-planning"
password = "regalia risk sulfite corporal"
ip = "tharsis.oru.se"
port = 8883
topics = ["tp/status", "mission_control", "perception", "simulation/robot/position"]
QOS_level = 0


def on_connect(client, userdata, flags, rc):
    print("on_connect callback: " + str(rc))


def on_message(client, obj, msg):
    print("msg from topic " + msg.topic + ": " + str(msg.payload))
    m_decode = str(msg.payload.decode("utf-8", "ignore"))   # decode json message
    data = json.loads(m_decode)     # insert json message to data variable

    if msg.topic == "tp/status":
        print("inside status topic handler")
        if data[1]['status'] == "ok":
            final_plan.current_plan_list_pos += 1   # if plan step had success, add 1 to list pos in plan object
            send_final_plan_1_by_1()
        else:
            print("plan failed, we cant handle that right now")
            # call function which handles fail case

    elif msg.topic == "mission_control":
        print("inside mission_control topic handler")
        set_info_from_mission_control(data)

    elif msg.topic == "perception":
        print("inside perception topic handler")
        set_info_from_perception(data)

    elif msg.topic == "simulation/robot/position":
        print("inside simulation/robot/position topic handler")
        set_info_from_simulation(data)

    #elif "simulation/sensor/status/" in msg.topic:
        #print("inside simulation/sensor/status topic handler")
        #set_info_from_simulation(data)

    else:
        print("can't handle that topic/message")


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
        self.client.disconnect()
