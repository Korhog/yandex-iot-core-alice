from mqtt.client import MQTT
from yandex.device import YandexIoTDevice
from yandex.tools import YandexIoTDeviceSerializer

class Engine:
    def __init__(self):
        self.__devices = dict()  
        self.client = MQTT()
        self.client.connect()


    def register_device(self, device: YandexIoTDevice):
        self.__devices[device.id] = device


    def handle(self, event, context):
        request_type = event['request_type']
        if request_type == "discovery":
            return self.__handle_discovery(event, context)
        
        if request_type == "action":
            return self.__handle_action(event, context)

        if request_type == "query":
            return self.__handle_query(event, context)


    def __handle_discovery(self, event, context):  
        devices = list()
        for device_id in self.__devices:
            devices.append(YandexIoTDeviceSerializer.serialize(self.__devices[device_id]))

        return {
            'request_id': self.__get_request_id(event),
            'payload': {
                'user_id': "f475df023c0e408d8cc84bc79be90017",
                'devices': devices
            }
        } 

    
    def __handle_action(self, event, context):
        results = list()

        # execute actions
        for event_device in self.__get_payload_devices(event):
            if event_device['id'] in self.__devices:
                device = self.__devices[event_device['id']]
                capabilities = list()

                for event_capability in self.__get_payload_devices_capabilites(event_device):
                    result = self.__execute_capability(device, event_capability)     
                    capabilities.append(result)

                results.append({
                    'id': device.id,
                    'capabilities': capabilities
                })        

        return {                
            'request_id': self.__get_request_id(event),
            'payload': {
                'devices': results
            }
        }


    def __handle_query(self, event, context):
        pass


    @staticmethod
    def __get_request_id(event):
        return event['headers']['request_id']


    @staticmethod
    def __get_payload_devices(event):
        return event['payload']['devices']


    @staticmethod
    def __get_payload_devices_capabilites(device):
        return device['capabilities']


    def __execute_capability(self, device, event_capability):
        capability, func = YandexIoTDeviceSerializer.get_capability(device, event_capability['type'])
        return capability.build_responce(func(device, self, event_capability['state']))
  