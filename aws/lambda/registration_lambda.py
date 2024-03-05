import boto3
import json

# Calling in the S3 bucket client to access specified S3 bucket:

# Storing the S3 client in a varible named s3
s3 = boto3.client("s3", region_name="us-east-1")


# Creaing a DynamoDB client to write info from Rekonition to DyanmoDB:

# Storing the DynamoDB client in a variable named dynamodb
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

# Storing the name of the table created in the AWS DynamoDB as dynamo_table_name
dynamo_table_name = dynamodb.Table("Facial-Indexing-DB")

# Creating a Rekognition client to extract certain features from images (such as: gender, age, face print, etc):
# Storing the rekognition client in a varible named rekognition
rekognition = boto3.client("rekognition", region_name="us-east-1")


def lambda_handler(event, context):
    print(event)

    # Storing the S3 bucket in a variable called s3_bucket_name
    s3_bucket_name = event["Records"][0]["s3"]["bucket"]["name"]

    # Storing the object_key from a object in a S3 bucket in a variable named object_key
    object_key = event["Records"][0]["s3"]["object"]["key"]

    try:
        response = index_image(s3_bucket_name, object_key)
        print(response)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            face_id = response["FaceRecords"][0]["Face"]["FaceId"]
            name = object_key.split(".")[0].split("_")
            first_name = name[0]
            last_name = name[1]
            gender = response["FaceRecords"][0]["FaceDetail"]["Gender"]
            age_range = response["FaceRecords"][0]["FaceDetail"]["AgeRange"]
            register(face_id, first_name, last_name, age_range, gender)
        return response

    except Exception as e:
        print(e)
        print(f"Error processing image {object_key} from bucket {s3_bucket_name}")
        raise e


# Creating a function to index each newly acquired image to later be stored in DynamoDB
def index_image(bucket, key):
    """
    This function is used to index the face and provide a series of arrays that determine
    specific traits from a submitted image

    bucket (str): The S3 bucket where the object is stored
    key (str): the speific object key that will be indexed

    Returns:
    An array of the image provided
    """
    response = rekognition.index_faces(
        # The ID of an existing collection to which you want to add the faces that are detected in the input images.
        CollectionId="initial_pictures",
        # Determining the image to be used from the S3 bucket
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        # The maximum number of faces to index. The value of MaxFaces must be greater than or equal to 1
        MaxFaces=1,
        # An array of facial attributes you want to be returned
        DetectionAttributes=["AGE_RANGE", "GENDER"],
    )
    return response


# Creating a function to register the new image with face print, first name, last name, age range, and gender
def register(face_id, first_name, last_name, age_range, gender):
    """
    This function will be used to craete a new record in the DynamoDB with the folloing fields:
    RekognitionFacePrintIndex, First_Name, Last_Name, Age_Range, and Gender

    face_id (str): The Rekognition face id given to the processed picture
    first_name (str): The first name determined by the name given in the S3 bucket object key
    last_name (str): The last name determined by the name given in the S3 bucket object key
    age_range (str): The age range determined by the Rekognition
    gender (str): The gender determined by the Rekognition

    Returns:
    A new record is stored in the specifed DynamoDB table
    """
    dynamo_table_name.put_item(
        Item={
            # Storing Face ID created by Rekognition as the RekognitionFacePrintIndex field
            "RekognitionFacePrintIndex": str(face_id),
            # Storing the part of the object from the S3 bucket as the first name
            "First_Name": str(first_name),
            # Storing the part of the object from the S3 bucket as the last name
            "Last_Name": str(last_name),
            # Storing the part age range determined by Rekognition as the Age_Range field
            "Age_Range": str(age_range),
            # Storing the gender determined by Rekognition as the Gender field
            "Gender": str(gender),
        }
    )
