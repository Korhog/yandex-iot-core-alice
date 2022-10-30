from yandex.core import EngineIoT
from devices.node_mcu import NodeMCU

engine = EngineIoT()
engine.register_device(NodeMCU("device-iot-node-mcu-01", "devices.types.other"))

event = dict()
print(engine.get_devices(event))