const aws = require("aws-sdk");

const s3 = new aws.S3({ apiVersion: "2006-03-01" });

const batteries = [
  { index: 0, serial: "66354", battery_token: "12321321qsd" },
  { index: 1, serial: "23313", battery_token: "2323121fab" },
  { index: 2, serial: "12333", battery_token: "adsb12312" },
];

// return data from batteries array
const get_battery_data = () => {
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
  return data;
};

const check_serial_and_token_exist = (serial, token, batteries_info) => {
  for (i = 0; i < batteries.length; i++) {
    if (
      serial === batteries_info[i].serial &&
      token.slice(7) === batteries_info[i].battery_token
    ) {
      return true;
    }
  }
  return false;
};

exports.handler = async (event) => {
  // check header has an authorization token and check if queryStringParameters exusts
  if (
    !event.headers.authorization ||
    !event.queryStringParameters ||
    !event.queryStringParameters["serial"]
  ) {
    // return status code 401 if not exist
    return {
      statusCode: 401,
      body: JSON.stringify({ message: "Invalid or missing token" }),
    };
  }
  const token = event.headers.authorization;
  const serial = event.queryStringParameters["serial"];
  // check serial number and token exist in batteries array

  if (!token || !token.startsWith("Bearer ")) {
    return {
      statusCode: 401,
      body: JSON.stringify({ message: "Invalid or missing token" }),
    };
  }

  let match = check_serial_and_token_exist(serial, token, batteries);

  if (match) {
    // if method is GET, return data
    if (event.httpMethod === "GET") {
      const data = get_battery_data();
      return {
        statusCode: 200,
        body: JSON.stringify(data),
      };
    }
    // if method is POST, return success
    if (event.httpMethod === "POST") {
      return {
        statusCode: 200,
        body: JSON.stringify({ message: "success" }),
      };
    }
  }
  // return status code 400 if not exist

  return {
    statusCode: 400,
    body: JSON.stringify({ message: "failed" }),
  };
};
