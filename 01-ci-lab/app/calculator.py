import json


def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def multiply(a, b):
    return a * b


def substract(a, b):
    return a - b


def power(a, b):
    return a**b


def lambda_handler(event, context):
    # Extract body depending on source (Function URL / API Gateway vs. Direct Console Test)
    if "body" in event:
        if isinstance(event["body"], str):
            body = json.loads(event["body"])
        else:
            body = event["body"]
    else:
        body = event

    # Extract required parameters from the body
    operation = body.get("operation")
    a = body.get("a")
    b = body.get("b")

    # Validate input presence
    if operation is None or a is None or b is None:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": "Missing required fields. Please provide 'operation', 'a', and 'b'."
                }
            ),
        }

    try:
        # Cast inputs to float/int to handle numeric string inputs smoothly
        a = float(a)
        b = float(b)

        if operation == "add":
            result = add(a, b)
        elif operation == "divide":
            result = divide(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        elif operation == "substract":
            result = substract(a, b)
        elif operation == "power":
            result = power(a, b)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": f"Unsupported operation: {operation}"}
                ),
            }

        return {"statusCode": 200, "body": json.dumps({"result": result})}

    except ValueError as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal error: {str(e)}"}),
        }
