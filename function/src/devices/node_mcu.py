from yandex.device import YandexIoTDevice
from yandex.capability import capability

class NodeMCU(YandexIoTDevice):
    def __init__(self, id, type):
        super().__init__(id, "NodeMCU", type)   

    @capability("devices.capabilities.on_off")
    def on_off(self):
        pass 