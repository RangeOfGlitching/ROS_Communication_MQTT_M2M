#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import time
import numpy as np
from paho.mqtt.client import ssl
import sys
  
  
receiveMessanges = []



def initialise_clients(clientname, user, Password):
    # callback assignment
    initialise_client = mqtt.Client(clientname, False)  # don't use clean session
    initialise_client.username_pw_set(user, Password)
    # initialise_client.tls_set(cert_reqs=ssl.CERT_NONE)

    initialise_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                              tls_version=ssl.PROTOCOL_TLS,
                              ciphers=None)
    initialise_client.tls_insecure_set(True)
    return initialise_client

def MQTT_Pub(pub_topic, msg, WaitForAck=True):
    Pubmsg = f"Confirm Order: {msg}"
    mid = client.publish(pub_topic, Pubmsg, qos=1)[1]
    if WaitForAck:
        if mid not in receiveMessanges:
            print("wait ack")
    # if status[1] == 15:
    #     client.disconnect()
    # print(f"result:{status}")
    # print(f"Send back the Order{status[1]} was already Confirm")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    MQTT_Pub(topic, "ack", True)

def on_disconnect(client, userdata, rc):
    print("dissconnect")

def on_publish(self, userdata, mid):
    print("ack")
    receiveMessanges.append(mid)

    


# ROS
def chatter_callback(message):
    #get_caller_id(): Get fully resolved name of local node
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", message.data)   
    MQTT_Pub(topic, message.data)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("phone_msg", String, chatter_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()










if __name__ == '__main__':
    host = "mrf7613cpe6j8.messaging.solace.cloud"
    port = 8883
    username = "solace-cloud-client"
    password = "rd9h3fudcut4j35fvu8938lq1rlab606"
    topic = "mqtt/sub"
    client = initialise_clients("client1", username, password)
    client.connect(host, port, 60)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.loop_start()
    listener()
