from yandex.engine import Engine
from devices.node_mcu import NodeMCU

engine = Engine()

# add new iot smart device 
engine.register_device(NodeMCU("device-iot-node-mcu-01", "devices.types.other"))

def handler(event, context):    
    return engine.handle(event, context)
