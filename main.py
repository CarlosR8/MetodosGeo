################################################################################################
####################################### CLIENTE MQTT ###########################################
################################################################################################

from paho.mqtt import client as mqtt_client
import random, json, time

#Local
#BROKER = 'localhost'
#PORT = 1883
#0TOPIC = "/test"
# generate client ID with pub prefix randomly
#CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
#USERNAME = 'admin'
#PASSWORD = 'public'
#FLAG_CONNECTED = 0

#Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "metodos_ubicacion"
TOPIC_ALERT = "metodos_ubicacion"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0

def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):
    #print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
        publish(client,TOPIC_ALERT,"Hola")

    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    #client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

#Enviar mensajes
def publish(client,TOPIC,msg):
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)
    time.sleep(2)


client = connect_mqtt()
def run():
    while True:
        client.loop_start()
        time.sleep(1)
        if FLAG_CONNECTED:
            print("Wait for message...")
        else:
            client.loop_stop()


if __name__ == '__main__':
    run()