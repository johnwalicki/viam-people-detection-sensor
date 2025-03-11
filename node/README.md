# Viam TypeScript SDK / node.js implementation of Viam People Detection Sensor

This example demonstrates how to:

- Connect to a machine using Node.js
- Return the getReadings from a Sensor
- Create a gRPC-web client for a Vision service
- Get Detections from the Vision / mlmodel
- Loop and report if a person is detected

## Usage

You must have a `.env` file in this directory with the following connection info which can be easily found in the TypeScript code sample for your machine. Use the `authEntity` value from the Code Sample as the `API_KEY_ID` and the `payload` value as the `API_KEY`.

```bash
HOST="<HOST>"
API_KEY_ID="<API_KEY_ID>"
API_KEY="<API_KEY>"
```

## Installation

Building this example requires the Viam TypeScript SDK to be available in a peer directory of the viam-people-detection-sensor fork.

```bash
cd ../..
git clone https://github.com/viamrobotics/viam-typescript-sdk.git
```

Then you can build / run the peopleSensor example

```bash
cd viam-people-detection-sensor/node
npm install
npm start
```

Edit `src/client.ts` to change the machine / sensor / Vision / mlmodel logic being run.

## Example

```text
$ npm start

> @viamrobotics/sdk-node-peopleSensor-example@0.1.0 start
> tsx --env-file=.env src/client.ts

dialing via WebRTC...
gathered local ICE a=candidate:6 1 UDP 1686108927 71.172.60.186 58993 typ srflx raddr 0.0.0.0 rport 0
received remote ICE candidate:2878742611 1 udp 2130706431 127.0.0.1 47692 typ host
received remote ICE candidate:1823732278 1 udp 2130706431 192.168.1.150 53583 typ host
received remote ICE candidate:2036382968 1 udp 1694498815 71.172.60.186 60353 typ srflx raddr 0.0.0.0 rport 60353
connected via WebRTC
[
  ResourceName {
    namespace: 'rdk',
    type: 'component',
    subtype: 'sensor',
    name: 'sensor1',
    remotePath: [],
    localName: ''
  },
  ResourceName {
    namespace: 'rdk',
    type: 'service',
    subtype: 'mlmodel',
    name: 'peopleModel',
    remotePath: [],
    localName: ''
  },
  ResourceName {
    namespace: 'rdk',
    type: 'component',
    subtype: 'camera',
    name: 'peopleCam',
    remotePath: [],
    localName: ''
  },
  ResourceName {
    namespace: 'rdk',
    type: 'service',
    subtype: 'vision',
    name: 'peopleDetector',
    remotePath: [],
    localName: ''
  },
  ResourceName {
    namespace: 'rdk',
    type: 'component',
    subtype: 'board',
    name: 'board-rpi5-rack5',
    remotePath: [],
    localName: ''
  },
  ResourceName {
    namespace: 'rdk',
    type: 'component',
    subtype: 'camera',
    name: 'camera-565webcam',
    remotePath: [],
    localName: ''
  },
  ResourceName {
    namespace: 'rdk',
    type: 'service',
    subtype: 'motion',
    name: 'builtin',
    remotePath: [],
    localName: ''
  },
  ResourceName {
    namespace: 'rdk',
    type: 'service',
    subtype: 'data_manager',
    name: 'data_manager-rack5',
    remotePath: [],
    localName: ''
  }
]
{ person_detected: 1 }
The reading is person_detected: 1
[
  Detection {
    confidence: 0.83984375,
    className: 'Person',
    xMin: 384n,
    yMin: 181n,
    xMax: 638n,
    yMax: 476n
  }
]
This is a person!
This is a person!
This is a person!
This is a person!
No person has been detected.
No person has been detected.
This is a person!
This is a person!
```
