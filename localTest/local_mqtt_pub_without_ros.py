import paho.mqtt.client as mqtt
import time
import numpy as np





def on_connect(self, userdata, flags, rc):
    # print("Connected with result code " + str(rc))
    pass


def initialise_clients(clientname):
    # callback assignment
    initialise_client = mqtt.Client(clientname, False) 
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


host = "192.168.1.110"
port = 1883

topic = "mqtt/pub"

client = initialise_clients("client1")

client.on_connect = on_connect

client.connect(host, port, 60)

client.on_publish = on_publish

client.loop_start()
#
publish(topic, "Connect", True)
count = 0
while True:
    randTemp = np.random.uniform(25.0, 35.0)
    publish(topic, randTemp)
    time.sleep(2)
    print(count)
    count += 1
