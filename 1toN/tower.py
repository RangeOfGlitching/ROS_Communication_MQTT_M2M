import paho.mqtt.client as mqtt
import time


def on_connect(self, userdata, flags, rc):
    global connect_flag
    print("Connected with result code " + str(rc))
    connect_flag = True


# def on_message(self, userdata, msg):
# print(f"Receive UAV_Z550 {msg.payload.decode('utf-8')}")
# print(f"Receive UAV_H380 {msg.payload.decode('utf-8')}")
# print("command: ", end="")


def initialise_clients(clientName):
    # callback assignment
    initialise_client = mqtt.Client(clientName, True)
    initialise_client.topic_ack = []
    return initialise_client


# publish a message
def publish(topics, message, waitForAck=False):
    mid = client.publish(topics, message, 1)[1]
    print(f"just published {message} to topic")
    if waitForAck:
        while mid not in client.topic_ack:
            print("wait for ack")
            time.sleep(0.25)
        client.topic_ack.remove(mid)


def on_publish(self, userdata, mid):
    client.topic_ack.append(mid)


connect_flag = False
mqtt_config = {"host": "192.168.50.81", "port": 1883, "topic": "cmd/broadcast", "name": "Tower"}
client = initialise_clients(mqtt_config["name"])
client.on_publish = on_publish
client.on_connect = on_connect
# client.on_message = on_message

client.connect(mqtt_config["host"], mqtt_config["port"], 60)
client.loop_start()

# publish(topicBroadcast, "Connect", True)
while True:
    if connect_flag:
        break
        
while True:
    command = input("command: ")
    publish(mqtt_config["topic"], command)
