exports.handler = async (event) => {
  console.log("Event: ", event);
  let responseMessage = "Hello, World!";

  if (event.queryStringParameters && event.queryStringParameters["VEN_NAME"]) {
    var ven_name = event.queryStringParameters["VEN_NAME"];
    responseMessage = {
      [ven_name]: {
        ven_name: ven_name,
        ven_id: "ven_id_ven123",
        registration_id: "reg_id_ven123",
      },
    };
  }

  if (event.httpMethod === "POST") {
    const body = JSON.parse(event.body);
    responseMessage = body;
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
