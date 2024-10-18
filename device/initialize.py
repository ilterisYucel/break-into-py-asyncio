import logging
import os
from typing import Dict, TypeVar

import yaml
from inovat_commonlib.modules.modbus_client import (
    ModbusClient,
    SModbusClientConfig,
)
from inovat_commonlib.modules.redis_client import RedisClient
from kink import di

from .schemas import SDeviceServiceConfig

__all__ = [
    "bootstrap",
]

ServiceConfigValues = TypeVar("ServiceConfigValues")

_INVALID_CONFIGURATION_FILE = """Invalid configuration file for device service.
Please check DEVICE_SERVICE_CONFIG_PATH environment variable.
"""

_INVALID_CONFIGURATION_CONTENT = """Invalid configuration file for device service.
Please check DEVICE_SERVICE_CONFIG_PATH environment variable.
"""

_CONFIGURATION_PROCESS = """Configuration process is failed.
"""
_VALID_ENV_KEY = [
    "DEVICE_SERVICE_CONFIG_PATH",
    "DEVICE_SERVICE_IDENTIFIER",
    "DEVICE_SERVICE_MODEL",
    "DEVICE_SERVICE_HOST",
    "DEVICE_SERVICE_PORT",
    "DEVICE_SERVICE_MODBUS_ORDER",
    "DEVICE_SERVICE_MODBUS_SLAVE",
    "DEVICE_SERVICE_INTERVAL",
    "DEVICE_SERVICE_MESSAGE_BUS_HOST",
    "DEVICE_SERVICE_MESSAGE_BUST_PORT",
    "DEVICE_SERVICE_MESSAGE_BUS_USERNAME",
    "DEVICE_SERVICE_MESSAGE_BUS_PASSWORD",
]


def create_config_schema(
    env_key_prefix: str,
) -> SDeviceServiceConfig | Dict[str, ServiceConfigValues] | None:
    config_path = os.getenv(f"{env_key_prefix}_CONFIG_PATH", "./configuration.yaml")
    config_content: str | dict
    try:
        with open(config_path, "r") as f:
            config_content = f.read()
    except (FileNotFoundError, TypeError):
        logging.getLogger(__name__).critical(_INVALID_CONFIGURATION_FILE)
        return None
    try:
        config_content = yaml.safe_load(config_content)
        config_content = SDeviceServiceConfig(**config_content["service"])
    except (yaml.YAMLError, TypeError):
        logging.getLogger(__name__).critical(_INVALID_CONFIGURATION_CONTENT)
        return None
    return merge_config(
        config_content=config_content,
        env_key_prefix=env_key_prefix,
        env_keys=_VALID_ENV_KEY,
    )


def merge_config(
    config_content: SDeviceServiceConfig, env_key_prefix: str, env_keys: list[str]
):
    try:
        for key in env_keys:
            key_without_prefix = key.split(env_key_prefix)[1]
            key_breadcrumb = key_without_prefix.split("_")[1:]
            if hasattr(config_content, ".".join(key_breadcrumb)):
                setattr(config_content, ".".join(key_breadcrumb), os.getenv(key))
        return config_content
    except Exception as e:
        logging.getLogger(__name__).critical(str(e))
        logging.getLogger(__name__).critical(_CONFIGURATION_PROCESS)


async def bootstrap():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    di["logger"] = logger

    config_schema: SDeviceServiceConfig = create_config_schema("DEVICE_SERVICE")
    di["service_config"] = config_schema

    redis_client = RedisClient(config=config_schema.message_bus)
    di["redis_client"] = redis_client

    modbus_client_config = SModbusClientConfig(
        host=config_schema.host, port=config_schema.port
    )
    modbus_client = ModbusClient(modbus_client_config, logger=logger)
    di["modbus_client"] = modbus_client
