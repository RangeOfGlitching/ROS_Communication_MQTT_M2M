#!/usr/bin/env python
# license removed for brevity
# lis
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import time
import numpy as np
from paho.mqtt.client import ssl
import sys
  
  



def initialise_clients(clientname, user, Password):
    # callback assignment
    initialise_client = mqtt.Client(clientname, False)  # don't use clean session
    initialise_client.username_pw_set(user, Password)
    # initialise_client.tls_set(cert_reqs=ssl.CERT_NONE)

    initialise_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                              tls_version=ssl.PROTOCOL_TLS,
                              ciphers=None)
    initialise_client.tls_insecure_set(True)
    # if mqttclient_log:  # enable mqqt client logging
    #     initialise_client.on_log = on_log
    initialise_client.on_connect = on_connect  # attach function to callback
    initialise_client.on_publish = on_publish
    # initialise_client.on_message = on_message  # attach function to callback
    # initialise_client.on_subscribe = on_subscribe
    # flags set
    initialise_client.topic_ack = []
    # initialise_client.run_flag = False
    # initialise_client.running_loop = False
    # initialise_client.subscribe_flag = False
    # initialise_client.bad_connection_flag = False
    # initialise_client.connected_flag = False
    # initialise_client.disconnect_flag = False
    return initialise_client

def MQTT_Pub(pub_topic, msg, WaitForAck=True):
    Pubmsg = f"Confirm Order: {msg}"
    mid = client.publish(pub_topic, Pubmsg, qos=1)[1]
    if WaitForAck:
        if mid not in client.topic_ack:
            print("wait ack")
        else:
            client.topic_ack.remove(mid)

    # if status[1] == 15:
    #     client.disconnect()
    # print(f"result:{status}")
    # print(f"Send back the Order{status[1]} was already Confirm")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    print("dissconnect")

def on_publish(self, userdata, mid):
    print("ack")
    client.topic_ack.append(mid)

    


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
    host = "mr2xg4fgthgmv.messaging.solace.cloud"
    port = 8883
    username = "solace-cloud-client"
    password = "mos9bagc51fv70u1ejk7l6rt28"
    topic = "mqtt/sub"
    client = initialise_clients("client1", username, password)
    # client.on_connect = on_connect
    # client.on_disconnect = on_disconnect
    # client.on_publish = on_publish
    client.connect(host, port, 60)
    client.loop_start()
    MQTT_Pub(topic, "ack", True)
    listener()
