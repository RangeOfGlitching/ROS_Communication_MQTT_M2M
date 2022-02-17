#!/usr/bin/env python
#coding:utf-8
# license removed for brevity
import ssl
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json


# Ros
def ros_pub(dataJson):
    global publisher, rate
    # data = json.loads(dataJson)
    publisher.publish(dataJson)     #將date字串發布到topic
    rate.sleep();
    # print(f"publish data {data}")


# MQTT
def initialise_clients(cname):
    # callback assignment
    initialise_client = mqtt.Client(clientname, False) 
    initialise_client.topic_ack = []
    return initialise_client

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    # print(f"got {msg.payload.decode('utf-8')}")
    ros_pub(msg.payload.decode('utf-8'))

if __name__ == '__main__':
    # Mqtt
    mqtt_config = {"host": "192.168.50.180", "port": 1883, "topic": "data/pub"}"
    client = initialise_clients("client1")
    client.on_publish = on_publish
    client.on_connect = on_connec
    client.connect(mqtt_config["host"], mqtt_config["port"], 60)
    client.loop_start()

    # Ros
    Mqtt_Node = 'publisher_py'
    rospy.init_node(Mqtt_Node)
    # initialize Ros node
    topicName = 'phone_msg'
    publisher = rospy.Publisher(topicName,String,queue_size=10)
    rate = rospy.Rate(10)

    client.loop_forever()

# mqtt connect code list
# 0: Connection successful
# 1: Connection refused – incorrect protocol version
# 2: Connection refused – invalid client identifier
# 3: Connection refused – server unavailable
# 4: Connection refused – bad username or password
# 5: Connection refused – not authorised
# 6-255: Currently unused.
