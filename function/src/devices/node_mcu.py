import math
from yandex.device import YandexIoTDevice
from yandex.capability import (on_off, brightness, color_setting)

def getRGB(value):
    if value <= 6700:
        # temperature logic
        return (255,255,255)


    h = hex(value)[2:]
    if len(h) == 5:
        h = '0' + h

    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

class NodeMCU(YandexIoTDevice):
    def __init__(self, id, type):
        super().__init__(id, "NodeMCU", type)   

    @on_off()
    def on_off(self, engine, params):
        value = params['value']
        return self.result(params, engine.client.publish(self.__topic__(), '1' if value else '0'))

    @color_setting(temperature_k=(2000, 6700), scenes=["alice"])
    def color_setting(self, engine, params):
        instance = params['instance']
        value = params['value']   
        msg = ""

        if instance == "rgb":        
            r,g,b = getRGB(value)
            msg = "rgb={0}:{1}:{2}".format(r,g,b)

        if instance == "scene":        
            msg = "scene={0}".format(value)
        
        if instance == "temperature_k":        
            msg = "rgb=255:255:255"   

        return self.result(params, engine.client.publish(self.__topic__(), msg))

    @brightness()
    def brightness(self, engine, params):
        value = math.floor(params['value'] / 100 * 255)
        msg = "brightness={0}".format(value)
        return self.result(params, engine.client.publish(self.__topic__(), msg))
