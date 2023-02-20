const aws = require("aws-sdk");

const s3 = new aws.S3({ apiVersion: "2006-03-01" });

// Function to convert JSON to CSV
function convertToCsv(data) {
  const headers = Object.keys(data);
  const values = Object.values(data);
  const rows = [headers.join(",")];
  rows.push(values.join(","));
  return rows.join("\n");
}

exports.handler = async (event) => {
  console.log("Event: ", event);
  let responseMessage = "Hello, World!";
  const bucket = "test-adjusted-elk";
  const key = "hello.json";
  const params = {
    Bucket: bucket,
    Key: key,
  };

  if (event.queryStringParameters && event.queryStringParameters["NAME"]) {
    var ven_name = event.queryStringParameters["NAME"];

    responseMessage = {
      [ven_name]: {
        ven_name: ven_name,
        ven_id: "ven_id_ven123",
        registration_id: "reg_id_ven123",
      },
    };
  }

  if (event.httpMethod === "POST") {
    const jsonData = JSON.parse(event.body);
    const bucket = "test-adjusted-elk";

    const timestamp = new Date().toISOString().replace(/:/g, "-");
    const filename = `data-${timestamp}.csv`;
    const csvData = convertToCsv(jsonData);
    // Save CSV file to S3 bucket
    const s3Params = {
      Bucket: bucket,
      Key: filename,
      Body: csvData,
      ContentType: "text/csv",
    };
    try {
      await s3.putObject(s3Params).promise();
      responseMessage = "save to s3 success";
    } catch (err) {
      responseMessage = err;
    }
  }

  const response = {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: responseMessage,
    }),
  };

  return response;
};
