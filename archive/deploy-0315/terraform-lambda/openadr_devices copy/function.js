const aws = require("aws-sdk");

const s3 = new aws.S3({ apiVersion: "2006-03-01" });

const batteries = [
  { index: 0, battery_sn: 66354, battery_token: "12321321qsd" },
  { index: 1, battery_sn: 23313, battery_token: "2323121fab" },
  { index: 2, battery_sn: 12333, battery_token: "adsb12312" },
];

exports.handler = async (event) => {
  const token = event.headers.authorization;
  var responseMessage = "Battery api";
  const payload = JSON.parse(event.body);
  let match = false;
  if (event.httpMethod !== "POST") {
    return {
      statusCode: 401,
      body: JSON.stringify({ message: "Invalid or missing token" }),
    };
  }

  if (!token || !token.startsWith("Bearer ")) {
    return {
      statusCode: 401,
      body: JSON.stringify({ message: "Invalid or missing token" }),
    };
  }

  for (let i = 0; i < batteries.length; i++) {
    const battery = batteries[i];
    if (
      battery.battery_sn === payload.battery_sn &&
      token.slice(7) === battery.battery_token
      // battery.battery_token === payload.battery_token
    ) {
      match = true;
      break;
    }
  }

  const bucket = "openadr-batteries-definite-puma";
  const key = "batteries.csv";

  if (match) {
    message = {};

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "success" }),
    };
  } else {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: "fail" }),
    };
  }
};
