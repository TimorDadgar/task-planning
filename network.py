import paho.mqtt.client as mqtt

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
    if msg.topic == "motion_planning":
        if str(msg.payload) == "fail":
            print("inside motion_planning topic handler")
            # create new plan
        else:
            print("not inside motion_planning topic handler")
            # send next part of plan
    elif msg.topic == "mission_control":
        print("inside mission_control topic handler")
        # handle msg.payload
    elif msg.topic == "perception":
        print("inside perception topic handler")
        # handle msg.payload
    elif msg.topic == "simulation":
        print("inside simulation topic handler")
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
        for i in topics:
            self.client.subscribe(i, QOS_level)


        self.client.will_set("dodsruna", "task_planning client is gone")

        self.client.loop_start()

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

net = Network()