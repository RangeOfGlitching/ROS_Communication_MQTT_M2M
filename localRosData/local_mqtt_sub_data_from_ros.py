#!/usr/bin/env python3
#coding:utf-8
import sys
import json
import paho.mqtt.client as mqtt


from traceback import print_tb
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from geometry_msgs.msg import Vector3

mqtt_config = {"host": "192.168.100.157", "port": 1883, "topic": "data/pub"}
data ={}
# Ros
def callBack_imu(IMU):

    gyro_x=str(IMU.linear_acceleration.x)
    gyro_y=str(IMU.linear_acceleration.y)
    gyro_z=str(IMU.linear_acceleration.z)

    accel_x=str(IMU.angular_velocity.x)
    accel_y=str(IMU.angular_velocity.y)
    accel_z=str(IMU.angular_velocity.z)

    dataImuUpdate = {"gyro_x": gyro_x, "gyro_y": gyro_y,"gyro_z":gyro_z, "accel_x": accel_x, "accel_y": accel_y, "accel_z": accel_z}
    data.update(dataImuUpdate)

    # print ('gyro_x:'+gyro_x+'\n'+'gyro_y:'+gyro_y+'\n'+'gyro_z:'+gyro_z +'\n')
    # print ('accel_x:'+accel_x+'\n'+'accel_y:'+accel_y+'\n'+'accel_z:'+accel_z +'\n')


def callBack_gps(GPS):
    lat=str(GPS.latitude)
    lon=str(GPS.longitude)
    dataGpsUpdate = {"lat": GPS.latitude, "lon": GPS.longitude}
    data.update(dataGpsUpdate)
    toJson(data)
    # print ('lat:'+lat+'\n'+'lon:'+lon+'\n')
def callBack_rng(RNG):
    dataRngUpdate = {"range": RNG.range}
    data.update(dataRngUpdate)
    dataJsonFormate = json.dumps(data)
    # print ('range:'+range+'\n')
    

def toJson(data):
    dataJsonFormate = json.dumps(data)
    print (dataJsonFormate)
    mqtt_Pub(message=dataJsonFormate)

# MQTT
def initialise_clients(clientname):
    # callback assignment
    initialise_client = mqtt.Client(clientname, False) 
    initialise_client.topic_ack = []
    return initialise_client


# publish a message
def mqtt_Pub(message, topics = mqtt_config["topic"], waitForAck=False):
    mid = client.publish(topics, message, 0)[1]
    # print(f"just published {message} to topic")
    if waitForAck:
        while mid not in client.topic_ack:
            print("wait for ack")
            time.sleep(0.25)
        client.topic_ack.remove(mid)


def on_publish(self, userdata, mid):
    client.topic_ack.append(mid)

def on_connect(self, userdata, flags, rc):
    print("Connected with result code " + str(rc))

 
if __name__ == '__main__':
    # Mqtt
    client = initialise_clients("client1")
    client.on_publish = on_publish
    client.on_connect = on_connect
    client.connect(mqtt_config["host"], mqtt_config["port"], 60)
    client.loop_start()

    # Ros
    nodeName = 'save_data_py'
    rospy.init_node(nodeName)
    # topicName = 'data_topic'
    subscriber1 = rospy.Subscriber('/mavros/imu/data_raw',Imu,callBack_imu)  #從topic獲取string再呼叫callback
    subscriber2 = rospy.Subscriber('/mavros/global_position/global',NavSatFix,callBack_gps)  #從topic獲取string再呼叫callback
    subscriber3 = rospy.Subscriber('/mavros/rangefinder/rangefinder',Range,callBack_rng)  #從topic獲取string再呼叫callback
    rospy.spin()
