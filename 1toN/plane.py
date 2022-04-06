import paho.mqtt.client as mqtt


def on_connect(self, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topicBroadcast)


def on_message(self, userdata, msg):
    msg = msg.payload.decode('utf-8')
    print(f"msg.topic {msg}")
    command = f"Receive commend  {msg} from client2"
    publish(topicAck, command)


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


def initialise_clients(clientName):
    # callback assignment
    initialise_client = mqtt.Client(clientName, False)
    initialise_client.topic_ack = []
    return initialise_client


host = "192.168.50.149"
port = 1883
username = "client2"
topicBroadcast = "mqtt/startUp3to1"
topicAck = "mqtt/topicAck3to1"

client = initialise_clients(username)

client.on_connect = on_connect

client.on_message = on_message

client.connect(host, port, 60)

client.loop_forever()
