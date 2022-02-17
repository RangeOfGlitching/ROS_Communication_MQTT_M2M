# ROS_Communication_MQTT_M2M

![alt text](https://github.com/tony19990828/ROS_Communication_MQTT_M2M/blob/main/schematic.png?raw=true)

internet -- use cloud mqtt broker to pub/sub data to ros node
   remeber change your host ip, userName, pssword (what I use is solace broker)

localRosData -- use local mqtt broker to pub/sub data to ros node
   remeber change your host ip (The machine that mqtt broker located)
   linux: ifconfig -> wlan0 - init - 192.168.xx.x
  
localTest-- use local mqtt broker to pub/sub data(for test)
   remeber change your host ip (The machine that mqtt broker located)
   linux: ifconfig -> wlan0 - init - 192.168.xx.x
