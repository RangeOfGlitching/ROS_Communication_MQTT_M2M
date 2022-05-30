#! /usr/bin/env python3
#coding:utf-8

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
    rate.sleep()
    # print(f"publish data {data}")

# MQTT
def on_connect(self, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("cmd/broadcast")


def on_message(self, userdata, msg):
    #msg = msg.payload.decode('utf-8')
    print(f"msg.topic {msg}")
    ros_pub(msg.payload.decode('utf-8'))


def initialise_clients(clientName):
    # callback assignment
    initialise_client = mqtt.Client(clientName, False)
    initialise_client.topic_ack = []
    return initialise_client


if __name__ == '__main__':
    # Mqtt
    mqtt_config = {"host": "192.168.50.109", "port": 1883, "topic": "cmd/broadcast"}
    client = initialise_clients("receiver")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_config["host"], mqtt_config["port"], 60)

    # Ros
    Mqtt_Node = 'publisher_py'
    rospy.init_node("cmd_receiver")
    # initialize Ros node
    topicName = 'cmd_receiver'
    publisher = rospy.Publisher(topicName,String,queue_size=10)
    rate = rospy.Rate(10)

    client.loop_forever()
