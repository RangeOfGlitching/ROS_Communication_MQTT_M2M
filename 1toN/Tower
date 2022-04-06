import paho.mqtt.client as mqtt
import time
import numpy as np


def on_connect(self, userdata, flags, rc):
    # print("Connected with result code " + str(rc))
    client.subscribe(topicAck)
    pass


def on_message(self, userdata, msg):
    print(f"msg.topic {msg.payload.decode('utf-8')}")


def initialise_clients(clientName):
    # callback assignment
    initialise_client = mqtt.Client(clientName, False)
    initialise_client.topic_ack = []
    return initialise_client


# publish a message
def publish(topics, message, waitForAck=False):
    mid = client.publish(topics, message, 2)[1]
    print(f"just published {message} to topic")
    if waitForAck:
        while mid not in client.topic_ack:
            print("wait for ack")
            time.sleep(0.25)
        client.topic_ack.remove(mid)


def on_publish(self, userdata, mid):
    print("ack")
    client.topic_ack.append(mid)


host = "192.168.50.149"
port = 1883

topicBroadcast = "mqtt/startUp3to1"

topicAck = "mqtt/topicAck3to1"

client = initialise_clients("client1")

client.on_connect = on_connect

client.connect(host, port, 60)

client.on_publish = on_publish

client.on_message = on_message

client.loop_start()
#
# publish(topicBroadcast, "Connect", True)
count = 0
while True:
    command = input("command: ")
    publish(topicBroadcast, command)
