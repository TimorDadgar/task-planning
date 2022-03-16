import paho.mqtt.client as mqtt
import json
from htn_planner import *

username = "task-planning"
password = "regalia risk sulfite corporal"
ip = "tharsis.oru.se"
port = 8883
topics = ["tp/status", "mcpoints", "perception/obsmap", "simulation/robot/position"]
QOS_level = 0


def on_connect(client, userdata, flags, rc):
    print("on_connect callback: " + str(rc))


def on_message(client, obj, msg):
    print("msg from topic " + msg.topic + ": " + str(msg.payload))
    m_decode = str(msg.payload.decode("utf-8", "ignore"))   # decode json message
    data = json.loads(m_decode)     # insert json message to data variable

    if msg.topic == "tp/status":
        print("inside status topic handler")
        if data[0]['status'] == "success":
            final_plan.current_plan_list_pos += 1   # if plan step had success, add 1 to list pos in plan object
            data_out = send_final_plan_1_by_1(False)    # change False to True if mock_data is going to be sent
            if data_out is not None:
                client.publish("tp/instruction", payload=data_out)
            else:
                print("end of plan")
        else:
            print("plan failed, we cant handle that right now")
            # call function which handles fail case

    elif msg.topic == "mcpoints":
        print("inside mission_control topic handler")
        if data[0] is None:
            print("cant handle null mission")
        else:
            set_info_from_mission_control(data)

            # run functions for creating the top_map and plan when we have fixed them
            # generate_top_map()
            # generate_plan()

            mock_data = True    # set mock_data to True if we should send mock data, otherwise set it to False
            data_out = send_final_plan_1_by_1(mock_data)

            # ------------------- REMOVE WHEN DOING REAL TEST -----------------------------
            client.publish("test_channel", payload=data_out)    # publish data to test_channel topic
            # -----------------------------------------------------------------------------

            # ------------------- UNCOMMENT WHEN DOING REAL TEST --------------------------
            # client.publish("tp/instruction", payload=data_out)     # publish data to real topic
            # -----------------------------------------------------------------------------

    elif msg.topic == "perception/obsmap":
        print("inside perception topic handler")
        set_info_from_perception(data)

    elif msg.topic == "simulation/robot/position":
        print("inside simulation/robot/position topic handler")
        set_info_from_simulation(data)

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

mqttc = Network()