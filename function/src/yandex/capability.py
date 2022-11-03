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
        if result['success']:
            self.__save(device, state)
 
        return {
            'type': self.type,
            'state': {
                'instance': result['instance'],
                'action_result': {
                    'status': "DONE" if result['success'] else "UNKNOWN_ERROR"
                }
            }
        }


    def load(self, device):
        valiable_name = self.__get_capability_name()
        if (device.__dict__.__contains__(valiable_name)):
            return device.__dict__[valiable_name]
        else:
            state = self.__set_default()
            device.__setattr__(valiable_name, state)   
            return state     


    def __save(self, device, state):
        valiable_name = self.__get_capability_name()
        if (device.__dict__.__contains__(valiable_name)):
            device.__dict__[valiable_name] = state
        else:
            device.__setattr__(valiable_name, state)   


    def __get_capability_name(self):
        return "__" + self.type.replace(".", "_")


    def __set_default(self):
        pass


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