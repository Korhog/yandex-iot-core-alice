from yandex.device import YandexIoTDevice
from yandex.capability import (capability, color_setting)

class NodeMCU(YandexIoTDevice):
    def __init__(self, id, type):
        super().__init__(id, "NodeMCU", type)   

    @capability("devices.capabilities.on_off")
    def on_off(self, engine, params):
        value = params['value']
        topic = "/krhg/{0}/commands".format(self.id)

        engine.client.publish
        if engine.client.publish(topic, '1' if value else '0'):
            return {
                'instance': params['instance'],
                'success': True
            }
        
        return {
            'instance': params['instance'],
            'success': False
        }

    