from yandex.device import YandexIoTDevice
from yandex.tools import YandexIoTDeviceSerializer

class EngineIoT:
    def __init__(self):
        self.__devices = dict()

    def handle(self, event, context):
        pass

    def register_device(self, device: YandexIoTDevice):
        self.__devices[device.id] = device

    def get_devices(self, event):
        devices = list()
        for device_id in self.__devices:
            devices.append(YandexIoTDeviceSerializer.serialize(self.__devices[device_id]))

        return devices