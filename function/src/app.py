from yandex.engine import Engine
from devices.node_mcu import NodeMCU


engine = Engine()
engine.register_device(NodeMCU("device-iot-node-mcu-01", "devices.types.other"))

event = {"headers":{"authorization":"##########","request_id":"814ecc30-27ba-45a9-961a-aca67d9d6864"},"request_type":"action","payload":{"devices":[{"id":"device-iot-node-mcu-01","capabilities":[{"type":"devices.capabilities.on_off","state":{"instance":"on","value": True}}]}]}}
print(engine.handle(event, None))