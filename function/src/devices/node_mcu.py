import math
from yandex.device import YandexIoTDevice
from yandex.capability import (capability, brightness, color_setting)

def getRGB(value):
    r =  value & 255
    g = (value >> 8) & 255
    b =   (value >> 16) & 255
    return r, g, b

class NodeMCU(YandexIoTDevice):
    def __init__(self, id, type):
        super().__init__(id, "NodeMCU", type)   

    @capability("devices.capabilities.on_off")
    def on_off(self, engine, params):
        value = params['value']
        topic = "/yandex-iot-core/{0}/commands".format(self.id)

        return self.result(params, engine.client.publish(topic, '1' if value else '0'))

    @color_setting(2000, 6700)
    def color_setting(self, engine, params):
        value = params['value']
        topic = "/yandex-iot-core/{0}/commands".format(self.id)
        
        r,g,b = getRGB(value)

        msg = "rgb={0}:{1}:{2}".format(r,g,b)

        return self.result(params, engine.client.publish(topic, msg))

    @brightness()
    def brightness(self, engine, params):
        value = math.floor(params['value'] / 100 * 255)
        topic = "/yandex-iot-core/{0}/commands".format(self.id)

        msg = "brightness={0}".format(value)

        return self.result(params, engine.client.publish(topic, msg))
