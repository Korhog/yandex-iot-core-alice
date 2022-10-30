from yandex.attribute import attribute

class capability(attribute):   
    def __init__(self, type, **kwargs):
        super().__init__()
        self.type = type
        self.retrievable = True
        self.reportable = False
        self.parameters = { "split":False }

    def get_type(self):
        return self.type

    def build_responce(self, result):
        return {
            'type': self.type,
            'state': {
                'instance': result['instance'],
                'action_result': {
                    'status': "DONE" if result['success'] else "UNKNOWN_ERROR"
                }
            }
        }

class color_setting(capability):
    def __init__(self, min, max, **kwargs):
        super().__init__("devices.capabilities.color_setting", **kwargs)

        self.parameters = {
            'color_model':"hsv",
            'temperature_k': {
                'max': max,
                'min': min
            }
        }