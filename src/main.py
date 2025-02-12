import asyncio

from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence

from typing_extensions import Self

from viam.components.sensor import Sensor
from viam.logging import getLogger
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes
from viam.services.vision import VisionClient, Detection

LOGGER = getLogger(__name__)


class peopleSensorJW(Sensor):
    # Subclass the Viam Sensor component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("walicki", "sensor"), "peopleSensorJW")

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        if "confidence" in config.attributes.fields:
            if not config.attributes.fields["confidence"].HasField("number_value"):
                raise Exception("confidence must be a float.")
            confidence = config.attributes.fields["confidence"].number_value
            if confidence == 0:
                raise Exception("confidence cannot be 0.")
        return []


    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        if "confidence" in config.attributes.fields:
            confidence = config.attributes.fields["confidence"].number_value
        else:
            confidence = 0.5
        self.confidence = confidence

        if "camera_source" in config.attributes.fields:
            camera_source = config.attributes.fields["camera_source"].string_value
        else:
            camera_source = "camera-565webcam"
        self.camera_source = camera_source

        if "vision_model" in config.attributes.fields:
            vision_model = config.attributes.fields["vision_model"].string_value
        else:
            vision_model = "peopleDetector"
        self.vision_model = vision_model
        # The vision name will be used to instantiate the VisionClient passed as a dependency
        self.vision_service = dependencies[VisionClient.get_resource_name(self.vision_model)]


    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, SensorReading]:
        detections = await self.vision_service.get_detections_from_camera(self.camera_source)
        isPerson = 0
        for d in detections:
            if d.confidence > self.confidence and d.class_name.lower() == "person":
                isPerson = 1

        return {"person_detected": isPerson}


    async def close(self):
        # This is a completely optional function to include. This will be called when the resource is removed from the config or the module
        # is shutting down.
        LOGGER.info(f"{self.name} is closed.")


async def main():
    """This function creates and starts a new module, after adding all desired resource models.
    Resource creators must be registered to the resource registry before the module adds the resource model.
    """
    Registry.register_resource_creator(Sensor.API, peopleSensorJW.MODEL, ResourceCreatorRegistration(peopleSensorJW.new, peopleSensorJW.validate_config))

    module = Module.from_args()
    module.add_model_from_registry(Sensor.API, peopleSensorJW.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
