const aws = require("aws-sdk");

const s3 = new aws.S3({ apiVersion: "2006-03-01" });

const VENS_info = {
  ven0: {
    ven_name: "ven0",
    ven_id: "ven0",
    registration_id: "reg_id_ven234",
  },
  ven1: {
    ven_name: "ven1",
    ven_id: "ven1",
    registration_id: "reg_id_ven123",
  },
  ven2: {
    ven_name: "ven2",
    ven_id: "ven2",
    registration_id: "reg_id_ven567",
  },
  ven3: {
    ven_name: "ven3",
    ven_id: "ven3",
    registration_id: "reg_id_ven567",
  },
  ven4: {
    ven_name: "ven4",
    ven_id: "ven4",
    registration_id: "reg_id_ven567",
  },
  ven5: {
    ven_name: "ven5",
    ven_id: "ven5",
    registration_id: "reg_id_ven567",
  },
  ven6: {
    ven_name: "ven6",
    ven_id: "ven6",
    registration_id: "reg_id_ven567",
  },
  ven7: {
    ven_name: "ven7",
    ven_id: "ven7",
    registration_id: "reg_id_ven567",
  },
  ven8: {
    ven_name: "ven8",
    ven_id: "ven8",
    registration_id: "reg_id_ven567",
  },
  ven9: {
    ven_name: "ven9",
    ven_id: "ven9",
    registration_id: "reg_id_ven567",
  },
};

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

  const bucket = "openadr-device-boss-civet";
  const key = "openadr_devices.json";
  const params = {
    Bucket: bucket,
    Key: key,
  };

  if (event.queryStringParameters && event.queryStringParameters["NAME"]) {
    var ven_name = event.queryStringParameters["NAME"];
    // check if ven_name exists in VENS_info
    if (!VENS_info[ven_name]) {
      return {
        statusCode: 400,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: "failed",
        }),
      };
    }
    // if ven_name exists, return ven_name, ven_id and registration_id
    responseMessage = {
      [ven_name]: {
        ven_name: ven_name,
        ven_id: VENS_info[ven_name].ven_id,
        registration_id: VENS_info[ven_name].registration_id,
      },
    };
    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: responseMessage,
      }),
    };
  }

  if (event.httpMethod === "POST") {
    const jsonData = JSON.parse(event.body);

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
