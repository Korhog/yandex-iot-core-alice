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

    
    def execute(self, engine, device, state):
        result = self.func(device, engine, state)
 
        return result['success'], {
            'type': self.type,
            'state': {
                'instance': result['instance'],
                'action_result': {
                    'status': "DONE" if result['success'] else "UNKNOWN_ERROR"
                }
            }
        }   


    def get_capability_name(self):
        return "__" + self.type.replace(".", "_")


    def get_default(self):
        return  {
            'instance': "on",
            'value': False
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

    def get_default(self):
        return  {
            'instance': "hsv",
            'value': {
                'h': 125,
                's': 25,
                'v': 100
            }
        } 

class brightness(capability):
    def __init__(self, **kwargs):
        super().__init__("devices.capabilities.range", **kwargs)

        self.parameters = {
            'instance': "brightness",
            'unit': "unit.percent",
            'range': {
                'min': 0,
                'max': 100
            }
        }

    def get_default(self):
        return  {
            'instance': "brightness",
            'value': 100
        }