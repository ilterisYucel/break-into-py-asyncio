from typing import Annotated

from inovat_commonlib.core.domain import SMessageBusConfig
from inovat_commonlib.services.device import (
    SModbusTCPDeviceConfig,
)
from pydantic import Field, IPvAnyAddress, field_serializer, field_validator


class SDeviceServiceConfig(SModbusTCPDeviceConfig):
    # identifier: Annotated[
    #     str,
    #     Field(
    #         default_factory=uuid.uuid4,
    #         description="Device identifier for indoor usage.",
    #     ),
    # ]
    # model: Annotated[str, Field(description="Device model for service creation.")]
    # host: Annotated[IPvAnyAddress, Field(description="Modbus client host for service.")]
    # port: Annotated[
    #     int, Field(default=502, description="Modbus client port for service.")
    # ]
    # order: Annotated[
    #     EModbusTCPDeviceOrder,
    #     Field(default="ABCD", description="Byte and word order for register read."),
    # ]
    # slave: Annotated[
    #     int,
    #     Field(gt=0, lt=256, description="Byte and word order for register read."),
    # ]
    # interval: Annotated[
    #     float, Field(default=0.1, description="Request interval to send device")
    # ]
    message_bus: Annotated[
        SMessageBusConfig,
        Field(description="Message Bus config for internal communication"),
    ]

    @field_validator("host")
    @classmethod
    def validate_host(cls, host: IPvAnyAddress):
        return str(host)

    @field_serializer("host")
    @classmethod
    def serialize_host(cls, host: IPvAnyAddress):
        return str(host)

    @field_validator("model", mode="before")
    @classmethod
    def validate_device_model(cls, device_model: str):
        return device_model.upper()

    @field_serializer("model")
    @classmethod
    def serialize_device_model(cls, device_model: str):
        return device_model.upper()
