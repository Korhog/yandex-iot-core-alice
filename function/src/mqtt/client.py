import ssl
import paho.mqtt.client as mqtt
from os import environ as env

class MQTT:
    def __init__(self):  
        self.mqttc = mqtt.Client()

        self.mqttc.username_pw_set(username=env['MQTT_USER'], password=env['MQTT_PASS'])
        self.mqttc.tls_set("mqtt/rootCA.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
        self.mqttc.tls_insecure_set(True)

    def connect(self): 
        self.mqttc.connect(env['MQTT_URL'], int(env['MQTT_PORT']))

    def publish(self, topic, message):
        tries = 5
        while True:
            responce = self.mqttc.publish(topic, message, 1)
            if responce.rc == mqtt.MQTT_ERR_SUCCESS:
                break

            tries -= 1
            if tries == 0:
                return False
                
        return True