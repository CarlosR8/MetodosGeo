from geopy.distance import geodesic
from paho.mqtt import client as mqtt_client
import random, json, time
import geocoder
import time

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
    #   print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
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

client = connect_mqtt()
# Obtener las coordenadas actuales
g = geocoder.ip('me')

#   Definir coordenadas
latitude_a = g.latlng[0]
longitude_a = g.latlng[1]

#   Distancia a recorrer en metros
distance_m = 20

#   Crear la nueva ubicacion
original_point = (latitude_a, longitude_a)
destination = geodesic(meters=distance_m).destination(original_point, 180)

latitude_b = destination.latitude
longitude_b = destination.longitude

'''Coordenadas de los puntos A y B
point_a = (latitude_a, longitude_a)  # Coordenadas del punto A
point_b = (latitude_b, longitude_b)  # Coordenadas del punto B'''

#   Definir ruta de incremento de 1 metro
increment = 1

#   Definir distancia minima para generar alerta
alert_distance = 5

# Calcular la distancia entre los puntos A y B
total_distance = geodesic((latitude_a, longitude_a), (latitude_b, longitude_b)).meters


# Calcular los incrementos de latitud y longitud
lat_increment = (latitude_b - latitude_a) * increment / total_distance
lon_increment = (longitude_b - longitude_a) * increment / total_distance

# Simular el movimiento entre los puntos A y B
current_latitude = latitude_a
current_longitude = longitude_a

def publish(client,TOPIC,msg):
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)


for i in range(int(total_distance/increment)):
    current_latitude += lat_increment
    current_longitude += lon_increment

    # Calcular la distancia actual a la ruta directa
    distance_to_route = geodesic((current_latitude, current_longitude), (latitude_a, longitude_a)).meters

    # Verificar si se excede la distancia permitida
    if distance_to_route > alert_distance:
        print("Se excedio a ruta")
        #publish(client,TOPIC, msg)

    print(f"Coordenadas actuales: {current_latitude}, {current_longitude}")
    time.sleep(2)