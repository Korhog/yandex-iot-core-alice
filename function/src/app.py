from yandex.engine import Engine
from devices.node_mcu import NodeMCU


engine = Engine()
engine.register_device(NodeMCU("device-iot-node-mcu-01", "devices.types.other"))

event = {"headers": {"authorization": "Bearer y0_AgAAAAAA8nz8AAiFvQAAAADSo0Edv-rvXvkwTJiCoV0MTQ2Wo1IkzZU", "request_id": "d0ab6173-2c6f-44f2-a659-2e29542b183c"}, "request_type": "action", "payload": {"devices": [{"id": "device-iot-node-mcu-01", "capabilities": [{"type": "devices.capabilities.on_off", "state": {"instance": "on", "value": False}}]}]}}
print(engine.handle(event, None))