const aws = require("aws-sdk");

const s3 = new aws.S3({ apiVersion: "2006-03-01" });

// Function to convert JSON to CSV

function randomIntFromInterval(min, max) {
  // min and max included
  return Math.random() * (max - min) + min;
}

exports.handler = async (event) => {
  console.log("Event: ", event);
  let responseMessage = "market-prices!";

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 401,
      body: JSON.stringify({ message: "Invalid or missing token" }),
    };
  }

  const market_prices = randomIntFromInterval(0.1, 0.25).toFixed(2);
  // console.log(rndInt);
  const data = { market_prices: market_prices };
  const response = {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: JSON.stringify(data),
    }),
  };

  return response;
};
