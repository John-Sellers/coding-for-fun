import boto3
import json

# Calling in the S3 bucket client to access specified S3 bucket:

# Storing the S3 client in a varible named s3
s3 = boto3.client('s3', region_name='us-east-1')


# Creaing a DynamoDB client to write info from Rekonition to DyanmoDB:

# Storing the DynamoDB client in a variable named dynamodb
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Storing the name of the table created in the AWS DynamoDB as dynamo_table_name
dynamo_table_name = dynamodb.Table('Facial-Indexing-DB')

# Creating a Rekognition client to extract certain features from images (such as: gender, age, face print, etc):
# Storing the rekognition client in a varible named rekognition
rekognition = boto3.client('rekognition', region_name='us-east-1')

def lambda_handler(event, context):
    # Storing the S3 bucket in a variable called s3_bucket_name
    s3_bucket_name = event['Records'][0]['s3']['bucket']['name']

    # Storing the object_key from a object in a S3 bucket in a variable named object_key
    object_key = event['Records'][0]['s3']['object']['key']

    # Storing the object from the S3 bucket into the image variable as a binary object
    image = s3.get_object(Bucket=s3_bucket_name, Key=object_key)['Body'].read()

    # Comparing the image captured in the image variable with the images stored in the
    # collection (initial_images). Then using Amazon Rekognition to compare image with
    # all images stored in the collection
    response = rekognition.search_faces_by_image(
        CollectionId="initial_pictures",
        Image = {'Bytes':image},
        MaxFaces = 1,
    )

    for match in response['FaceMatches']:
        face = dynamo_table_name.get_item(
            Key={'RekognitionFacePrintIndex': match['Face']['FaceId']}
        )

        if 'Item' in face:
            first_name = face['Item']['First_Name']
            last_name = face['Item']['Last_Name']
            response_data = {
                'first_name': first_name,
                'last_name': last_name
            }
            print('Person Found: ', face['Item']['First_Name'], ' ', face['Item']['Last_Name'])
            return {
                'statusCode': 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                    },
                'body': json.dumps(response_data)
            }
        else:
            print('Person could no be recognized!')
            return {
                'statusCode': 404,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                    },
                'body': 'Person could not be recognized!'
            }