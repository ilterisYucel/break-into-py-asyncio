import uuid
from typing import Annotated

from inovat_commonlib.modbus_devices.enums import ModbusTCPDeviceOrder
from pydantic import BaseModel, Field, IPvAnyAddress, field_serializer, field_validator


class SDeviceServiceMessageBusConfig(BaseModel):
    host: Annotated[
        IPvAnyAddress, Field(description="Message bus client host for service.")
    ]
    port: Annotated[
        int, Field(default=6379, description="Message bus client port for service.")
    ]
    username: Annotated[str, Field(description="Username for message bus client")]
    password: Annotated[str, Field(description="Password for message bus client")]

    @field_validator("host")
    @classmethod
    def validate_host(cls, host: IPvAnyAddress):
        return str(host)

    @field_serializer("host")
    @classmethod
    def serialize_host(cls, host: IPvAnyAddress):
        return str(host)


class SDeviceServiceConfig(BaseModel):
    identifier: Annotated[
        str,
        Field(
            default_factory=uuid.uuid4(),
            description="Device identifier for indoor usage.",
        ),
    ]
    device_model: Annotated[
        str, Field(description="Device model for service creation.")
    ]
    host: Annotated[IPvAnyAddress, Field(description="Modbus client host for service.")]
    port: Annotated[
        int, Field(default=502, description="Modbus client port for service.")
    ]
    order: Annotated[
        ModbusTCPDeviceOrder,
        Field(default="ABCD", description="Byte and word order for register read."),
    ]
    slave: Annotated[
        int,
        Field(gt=0, lt=256, description="Byte and word order for register read."),
    ]
    message_bus: Annotated[
        SDeviceServiceMessageBusConfig,
        Field(description="Message bus config for service."),
    ]

    @field_validator("host")
    @classmethod
    def validate_host(cls, host: IPvAnyAddress):
        return str(host)

    @field_serializer("host")
    @classmethod
    def serialize_host(cls, host: IPvAnyAddress):
        return str(host)
