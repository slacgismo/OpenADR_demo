const aws = require("aws-sdk");

// const s3 = new aws.S3({ apiVersion: "2006-03-01" });

// Function to convert JSON to CSV

exports.handler = async (event) => {
  // console.log("Event: ", event);
  let responseMessage = "participated vens!";

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 401,
      body: JSON.stringify({ message: "Invalid or missing token" }),
    };
  }
  const payload = JSON.parse(event.body);

  const response = {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: JSON.stringify(payload),
    }),
  };

  return response;
};
