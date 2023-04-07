from yandex.attribute import attribute
from yandex.capability import capability

class YandexIoTDeviceSerializer:
    @staticmethod
    def serialize(device):
        desc = {            
            'id': device.id,
            'name': device.name,
            'type': device.type
        }        

        capabilities = list()
        for capability in YandexIoTDeviceSerializer.get_capabilities(device):       
            capabilities.append({
                'type': capability.type,
                'retrievable': capability.retrievable,
                'reportable': capability.reportable,
                'parameters': capability.parameters
            })

        desc['capabilities'] = capabilities
        return desc

    
    @staticmethod
    def get_capability(device, type):
        methods = {funcname: func for funcname, func in device.__class__.__dict__.items() if hasattr(func, '__dict__')}.items()
        for funcname, func in methods:
            if YandexIoTDeviceSerializer.__has_attributes(func):
                for attr in YandexIoTDeviceSerializer.__get_attributes(func):
                    if isinstance(attr, capability) and attr.type == type:
                        return attr

        return None

    
    @staticmethod
    def get_capabilities(device):
        capabilities = list()
        methods = {funcname: func for funcname, func in device.__class__.__dict__.items() if hasattr(func, '__dict__')}.items()
        for funcname,func in methods:
            if YandexIoTDeviceSerializer.__has_attributes(func):
                for attr in YandexIoTDeviceSerializer.__get_attributes(func):
                    if isinstance(attr, capability):
                        capabilities.append(attr)

        return capabilities    


    @staticmethod
    def __has_attributes(method):
        if method.__dict__.__contains__(attribute.attributes_member_name):
            attributeList = method.__dict__[attribute.attributes_member_name]
            return (isinstance(attributeList, list) and (len(attributeList) != 0))
        else:
            return False


    @staticmethod
    def __get_attributes(method):
        if method.__dict__.__contains__(attribute.attributes_member_name):
            attributeList = method.__dict__[attribute.attributes_member_name]
            if isinstance(attributeList, list):
                return attributeList
        return list()