class YandexIoTDevice:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

    def result(self, params, success):
        return {
            'instance': params['instance'],
            'success': success
        }
    
    def __topic__(self):
        return "/yandex-iot-core/{0}/commands".format(self.id)
