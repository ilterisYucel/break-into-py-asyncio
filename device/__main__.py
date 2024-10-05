import logging

from inovat_commonlib.loop_manager import UVLoopManager
from inovat_commonlib.modbus_client import ModbusClient
from inovat_commonlib.modbus_devices import (
    BaseModbusTCPDevice,
    DeviceFactory,
    SModbusTCPDeviceConfig,
)
from inovat_commonlib.redis_client import RedisClient
from kink import di, inject

from device.initialize import bootstrap
from device.schemas import SDeviceServiceConfig

_loop_manager = di["loop_manager"]


@inject
async def process(
    service_config: SDeviceServiceConfig,
    modbus_client: ModbusClient,
    redis_client: RedisClient,
    loop_manager: UVLoopManager,
    logger: logging.Logger,
):
    device_config: SModbusTCPDeviceConfig = SModbusTCPDeviceConfig(
        identifier=service_config.identifier,
        device_model=service_config.device_model,
        modbus_order=service_config.order,
        modbus_slave=service_config.slave,
    )
    device: BaseModbusTCPDevice = DeviceFactory(config=device_config).build()
    print(device)


async def main():
    await bootstrap()
