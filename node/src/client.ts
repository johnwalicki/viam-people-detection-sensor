import { setMaxIdleHTTPParsers } from "http";

const VIAM = require('@viamrobotics/sdk');
const wrtc = require('node-datachannel/polyfill');
const connectNode = require('@connectrpc/connect-node');

// @ts-expect-error
globalThis.VIAM = {
  GRPC_TRANSPORT_FACTORY: (opts: any) =>
    connectNode.createGrpcTransport({ httpVersion: '2', ...opts }),
};
for (const key in wrtc) {
  (global as any)[key] = (wrtc as any)[key];
}

async function connect() {
  const host = process.env.HOST;
  const apiKeyId = process.env.API_KEY_ID;
  const apiKeySecret = process.env.API_KEY;
  if (!host) {
    throw new Error('must set HOST env var');
  }
  if (!apiKeyId) {
    throw new Error('must set API_KEY_ID env var');
  }
  if (!apiKeySecret) {
    throw new Error('must set API_KEY_SECRET env var');
  }

  const client = await VIAM.createRobotClient({
    host,
    credentials: {
      type: 'api-key',
      authEntity: apiKeyId,
      payload: apiKeySecret, 
    },
    signalingAddress: 'https://app.viam.com:443',
    iceServers: [{ urls: 'stun:global.stun.twilio.com:3478' }],
  });

  console.log(await client.resourceNames());
  
  const sensor = new VIAM.SensorClient(client,"sensor1");

  // Return the reading from a Sensor
  const reading = await sensor.getReadings();
  console.log(await sensor.getReadings());
  console.log("The reading is person_detected: "+reading.person_detected);

  // Create a gRPC-web client for a Vision service.
  const peopleDetector = new VIAM.VisionClient(client,"peopleDetector");
  // Get Detections from the Vision / mlmodel
  const detections = await peopleDetector.getDetectionsFromCamera("camera-565webcam");
  console.log(detections);

  // Loop and report if a person is detected
  while( true ) {
    const detections = await peopleDetector.getDetectionsFromCamera("camera-565webcam");
    let found = false;
    for (let d of detections) {
      if (d.confidence > 0.7 && d.className === "Person") {
        console.log("This is a person!");
        found = true;
      } else {
        console.log("No person has been detected.");
        found = false;
      }
    }
    await sleep(1000);
  }  
}

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));

connect().catch((e) => {
  console.error('error connecting to machine', e);
});
