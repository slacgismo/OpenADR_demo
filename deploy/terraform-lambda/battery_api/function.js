const aws = require("aws-sdk");

const dynamodb = new aws.DynamoDB();

const random_value = (min, max, decimal) => {
  const randomFloat = (Math.random() * (max - min) + min).toFixed(decimal);
  return randomFloat;
};

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
    RSOC: random_value(20, 98, 0),
    RemainingCapacity_W: 5432,
    SystemStatus: "OnGrid",
    Timestamp: "2023-02-09 14:50:32",
    USOC: random_value(10, 95, 0),
    Uac: 237,
    Ubat: 54,
  };
  return data;
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
  const authHeader = event.headers.Authorization || event.headers.authorization;
  const serial = event.queryStringParameters["serial"];
  const match = authHeader.match(/^Bearer (.+)$/);
  if (!match) {
    return {
      statusCode: 401,
      body: 'Invalid authorization header format. Format should be "Bearer <token>".',
    };
  }
  const token = match[1];
  const params = {
    TableName: "battery-table",
    Key: {
      serial: { S: serial },
    },
  };
  const result = await dynamodb.getItem(params).promise();
  if (result.Item && result.Item.token && result.Item.token.S === token) {
    const data = get_battery_data();
    return {
      statusCode: 200,
      body: JSON.stringify(data),
    };
  }

  return {
    statusCode: 400,
    body: JSON.stringify({ message: "failed" }),
  };
};
