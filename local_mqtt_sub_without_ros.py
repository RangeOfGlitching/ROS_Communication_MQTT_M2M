import ssl

import paho.mqtt.client as mqtt


def on_connect(self, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(self, userdata, msg):
    print(f"msg.topic {msg.payload.decode('utf-8')}")


def initialise_clients(cname):
    # callback assignment
    initialise_client = mqtt.Client(cname, True)  # don't use clean session
    return initialise_client


host = "192.168.50.180"
port = 1883
topic = "mqtt/pub"

client = initialise_clients("python_sub")

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
