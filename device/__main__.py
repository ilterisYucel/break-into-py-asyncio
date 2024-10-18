import asyncio
import logging

from inovat_commonlib.modules.modbus_client import ModbusClient
from inovat_commonlib.modules.redis_client import RedisClient
from inovat_commonlib.services.device import (
    BaseModbusTCPDevice,
    DeviceFactory,
)
from kink import inject

from device.initialize import bootstrap
from device.schemas import SDeviceServiceConfig


@inject
async def process(
    service_config: SDeviceServiceConfig,
    modbus_client: ModbusClient,
    redis_client: RedisClient,
    logger: logging.Logger,
):
    # device_config: SModbusTCPDeviceConfig = SModbusTCPDeviceConfig(
    #     identifier=service_config.identifier,
    #     model=service_config.model,
    #     interval=service_config.interval,
    #     modbus_order=service_config.modbus_order,
    #     modbus_slave=service_config.modbus_slave,
    # )
    device: BaseModbusTCPDevice = DeviceFactory(
        config=service_config,
        modbus_client=modbus_client,
        redis_client=redis_client,
        logger=logger,
    ).build()
    await device.initialize()
    await device.process()


async def main():
    await bootstrap()
    await process()


asyncio.run(main())
