#!/usr/bin/env python
#coding:utf-8
# license removed for brevity
import ssl
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt

def ros_pub(data):
    global publisher, rate

    publisher.publish(data)     #將date字串發布到topic
    rate.sleep();
    print(f"publish data {data}")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    print(f"got {msg.payload.decode('utf-8')}")
    ros_pub(msg.payload.decode('utf-8'))


def initialise_clients(cname, user, Password):
    # callback assignment
    initialise_client = mqtt.Client(cname, True)  # don't use clean session
    initialise_client.username_pw_set(user, Password)

    initialise_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                              tls_version=ssl.PROTOCOL_TLS,
                              ciphers=None)
    initialise_client.tls_insecure_set(True)
    return initialise_client


host = "mr2xg4fgthgmv.messaging.solace.cloud"
port = 8883
username = "solace-cloud-client"
password = "mos9bagc51fv70u1ejk7l6rt28"
topic = "mqtt/pub"

Mqtt_Node = 'publisher_py'
rospy.init_node(Mqtt_Node)
# initialize Ros node
topicName = 'phone_msg'
publisher = rospy.Publisher(topicName,String,queue_size=10)
rate = rospy.Rate(10)

client = initialise_clients("python_sub", username, password)

client.on_connect = on_connect

client.on_message = on_message

client.connect(host, port, 60)

client.loop_forever()

# mqtt connect code list
# 0: Connection successful
# 1: Connection refused – incorrect protocol version
# 2: Connection refused – invalid client identifier
# 3: Connection refused – server unavailable
# 4: Connection refused – bad username or password
# 5: Connection refused – not authorised
# 6-255: Currently unused.

