import asyncio
import os

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient, Detection
from viam.components.sensor import Sensor

# Set environment variables.
api_key = os.getenv('VIAM_API_KEY') or ''
api_key_id = os.getenv('VIAM_API_KEY_ID') or ''
address = os.getenv('VIAM_ADDRESS') or ''

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key=api_key,
      api_key_id=api_key_id
    )
    return await RobotClient.at_address(address, opts)


async def main():
    robot = await connect()

    print("Resources:")
    print(robot.resource_names)

    sensor = Sensor.from_robot(robot, name="sensor1")
    reading = await sensor.get_readings()
    print(f"The reading is {reading}")

    response = await sensor.do_command({"hello": "world"})
    print(f"The response is {response}")

    await robot.close()


async def main2():
    machine = await connect()
    print( "Resources:")
    print(machine.resource_names)
    # make sure that your detector name in the app matches "peopleDetector"
    peopleDetector = VisionClient.from_robot(machine, "peopleDetector")

    while True:
        detections = await peopleDetector.get_detections_from_camera("camera-565webcam")
        print(detections)
        found = False
        for d in detections:
            if d.confidence > 0.7 and d.class_name.lower() == "person":
                print("This is a person!")
                found = True
        if found:
            print("1 - person_detected")
        else:
            print("0 - no_person_detected")
        await asyncio.sleep(10)

    await asyncio.sleep(5)
    await machine.close()


if __name__ == '__main__':
    asyncio.run(main())