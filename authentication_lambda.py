import boto3
import json

# Calling in the S3 bucket client to access specified S3 bucket:
# Storing the S3 client in a varible named s3
s3 = boto3.client("s3")

# specifiying the name of the bucket that captured images will be stored
bucket_name = "authentication-bucket"


# Creaing a DynamoDB client to write info from Rekonition to DyanmoDB:
# Storing the DynamoDB client in a variable named dynamodb
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

# Storing the name of the table created in the DynamoDB as dynamo_table_name
dynamo_table_name = dynamodb.Table("Facial-Indexing-DB")

# Creating a Rekognition client so that it can compared images captured in the specified S3 bucket and DynamoDB:
# Storing the rekognition client in a varible named rekognition
rekognition = boto3.client("rekognition", region_name="us-east-1")


def lambda_handler(event, context):
    print(event)

    # Obtaining the object key from the triggered event (in this case S3 bucket).
    object_key = event["Records"][0]["s3"]["object"]["key"]

    # Storing the newly captured image in the S3 bucket in this variable
    image = s3.get_object(Bucket=bucket_name, Key=object_key)["Body"].read()

    # Checking DynamoDB to see if there are any mathces
    response = rekognition.search_faces_by_image(
        CollectionId="initial_pictures", Image={"Bytes": image}
    )

    for match in response["FaceMatches"]:
        # Printing the Face Id and Confidence Level
        print(match["Face"]["FaceId"], match["Face"]["Confidence"])

        # Extracting the FaceId from Dynamodb and specifying it as the face variable
        face = dynamo_table_name.get_item(
            Key={"RekognitionFacePrintIndex": match["Face"]["FaceId"]}
        )

        if "item" in face:
            print("Person Found: ", face["item"])
            return build_response(
                200,
                {
                    "Message": "Success",
                    "First_Name": face["item"]["first_name"],
                    "Last_Name": face["item"]["last_name"],
                },
            )
    print("Person could not be recognized")
    return build_response(403, {"Message": "Person not found"})


def build_response(status_code, body=None):
    """
    This function is used to return a response. Depending on the status_code inputted and
    the body of the function, it will return the resonse in json format

    status_code (int): The status code which is appropriate for the outcome of the lambda handler
    body (dict (Key (str): Value (str)): Specifies what message is the be read

    Returns:
    A json response
    """
    response = {
        "status_code": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    if body is not None:
        response["body"] = json.dump(body)
    return response
