const aws = require("aws-sdk");

const s3 = new aws.S3({ apiVersion: "2006-03-01" });

const batteries = [
  { index: 0, serial: "66354", battery_token: "12321321qsd" },
  { index: 1, serial: "23313", battery_token: "2323121fab" },
  { index: 2, serial: "12333", battery_token: "adsb12312" },
];

exports.handler = async (event) => {
  const token = event.headers.authorization;

  let match = false;
  if (event.httpMethod !== "GET") {
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

  const serial = event.queryStringParameters["serial"];

  for (let i = 0; i < batteries.length; i++) {
    const battery = batteries[i];

    if (
      serial === battery.serial &&
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
    var data = {
      BackupBuffer: "10",
      BatteryCharging: true,
      BatteryDischarging: false,
      Consumption_Avg: 0,
      Consumption_W: 0,
      Fac: 60,
      FlowConsumptionBattery: false,
      FlowConsumptionGrid: false,
      FlowConsumptionProduction: false,
      FlowGridBattery: true,
      FlowProductionBattery: true,
      FlowProductionGrid: true,
      GridFeedIn_W: 196,
      IsSystemInstalled: 1,
      OperatingMode: "2",
      Pac_total_W: -1800,
      Production_W: 1792,
      RSOC: 52,
      RemainingCapacity_W: 5432,
      SystemStatus: "OnGrid",
      Timestamp: "2023-02-09 14:50:32",
      USOC: 49,
      Uac: 237,
      Ubat: 54,
    };
    return {
      statusCode: 200,
      body: JSON.stringify(data),
    };
  } else {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: "failed" }),
    };
  }
};
