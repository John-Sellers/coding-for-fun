import boto3
import json

# Calling in the S3 bucket client to access specified S3 bucket:
s3 = boto3.client("s3")  # Storing the S3 client in a varible named s3
bucket_name = "authentication-bucket"


# Creaing a DynamoDB client to write info from Rekonition to DyanmoDB:
dynamodb = boto3.resource(
    "dynamodb", region_name="us-east-1"
)  # Storing the DynamoDB client in a variable named dynamodb
dynamo_table_name = dynamodb.Table(
    "Facial-Indexing-DB"
)  # Storing the name of the table created in the AWS DynamoDB as dynamo_table_name

# Creating a Rekognition client to extract certain features from images (such as: gender, age, face print, etc):
rekognition = boto3.client(
    "rekognition"
)  # Storing the rekognition client in a varible named rekognition

# Creating collection id which is mandatory for Rekognition (if needed):
# collection_id = rekognition.create_collection(CollectionId='initial_pictures')


def lambda_handler(event, context):
    print(event)
    object_key = event["queryStringParameters"]["object_key"]
    image_bytes = s3.get_object(Bucket=bucket_name, Key=object_key)["Body"].read()
    response = rekognition.search_faces_by_image(
        collection_id="initial_pictures", Image={"Bytes": image_bytes}
    )

    for match in response["FaceMatches"]:
        print(match["Face"]["FaceId"], match["Face"]["Confidence"])

        face = dynamo_table_name.get_item(
            Key={"RekognitionFacePrintIndex": match["Face"]["FaceId"]}
        )

        if "item" in face:
            print("Person Found: ", face["item"])
            return build_response(
                200,
                {
                    "Message": "Success",
                    "first_name": face["item"]["first_name"],
                    "last_name": face["item"]["last_name"],
                },
            )
    print("Person could not be recognized")
    return build_response(403, {"Message": "Person not found"})


def build_response(status_code, body=None):
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
