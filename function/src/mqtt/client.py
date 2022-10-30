import ssl
import mqtt.config as cfg
import paho.mqtt.client as mqtt

class MQTT:
    def __init__(self):  
        self.mqttc = mqtt.Client()

        self.mqttc.username_pw_set(username=cfg.brpker_user,password=cfg.proker_pass)
        self.mqttc.tls_set("function/src/mqtt/rootCA.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
        self.mqttc.tls_insecure_set(True)

    def connect(self): 
        self.mqttc.connect(cfg.broker_url, cfg.broker_port)

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