import boto3
import json

# Calling in the S3 bucket client to access specified S3 bucket:
s3 = boto3.client("s3") # Storing the S3 client in a varible named s3


# Creaing a DynamoDB client to write info from Rekonition to DyanmoDB:
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # Storing the DynamoDB client in a variable named dynamodb
dynamo_table_name = dynamodb.Table('Facial-Indexing-DB') # Storing the name of the table created in the AWS DynamoDB as dynamo_table_name
# dynamo_table_name = dynamodb.Table(dynamo_table_name)

# Creating a Rekognition client to extract certain features from images (such as: gender, age, face print, etc):
rekognition = boto3.client('rekognition') # Storing the rekognition client in a varible named rekognition

# Creating collection id which is mandatory for Rekognition (if needed):
# collection_id = rekognition.create_collection(CollectionId='initial_pictures')
    

def lambda_handler(event, context):
    print(event)
    
    # Storing the S3 bucket in a variable called s3_bucket_name
    s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
    
    # Storing the object_key from a object in a S3 bucket in a variable named object_key
    object_key = event['Records'][0]['s3']['object']['key']

    try:
        response = index_image(s3_bucket_name, object_key)
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            face_id = response['FaceRecords'][0]['Face']['FaceId']
            name = object_key
            gender = response['FaceRecords'][0]['FaceDetail']['Gender']
            age_range = response['FaceRecords'][0]['FaceDetail']['AgeRange']
            register(face_id, name, age_range, gender)
        return response
    
    except Exception as e:
        print(e)
        print(f'Error processing image {object_key} from bucket {s3_bucket_name}')
        raise e

# Creating a function to index each newly acquired image to later be stored in DynamoDB
def index_image(bucket, key):
        response = rekognition.index_faces(
            CollectionId = 'initial_pictures',                        # The ID of an existing collection to which you want to add the faces that are detected in the input images.
            Image = {'S3Object': {'Bucket': bucket, 'Name': key}}, # Determining the image to be used from the S3 bucket
            MaxFaces = 1,                                          # The maximum number of faces to index. The value of MaxFaces must be greater than or equal to 1
            DetectionAttributes = ['AGE_RANGE', 'GENDER']          # An array of facial attributes you want to be returned.
        )
        return response

# Creating a function to register the new image with face print, first name, last name, and gender
def register(face_id, name, age_range, gender):
        dynamo_table_name.put_item(
            Item={
                'RekognitionFacePrintIndex': str(face_id), # Storing Face ID created by Rekognition as the RekognitionFacePrintIndex field
                'Name': str(name),                         # Storing the object key from the S3 bucket as the name field
                'Age Range': str(age_range),               # Storing the age_range determined by Rekognition as the Age Range field
                'Gender': str(gender)                      # Storing the gender determined by Rekognition as the Age Range field
            }
        )


# {
#    "FaceModelVersion": "string",
#    "FaceRecords": [ 
#       { 
#          "Face": { 
#             "BoundingBox": { 
#                "Height": number,
#                "Left": number,
#                "Top": number,
#                "Width": number
#             },
#             "Confidence": number,
#             "ExternalImageId": "string",
#             "FaceId": "string",
#             "ImageId": "string",
#             "IndexFacesModelVersion": "string",
#             "UserId": "string"
#          },
#          "FaceDetail": { 
#             "AgeRange": { 
#                "High": number,
#                "Low": number
#             },
#             "Beard": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "BoundingBox": { 
#                "Height": number,
#                "Left": number,
#                "Top": number,
#                "Width": number
#             },
#             "Confidence": number,
#             "Emotions": [ 
#                { 
#                   "Confidence": number,
#                   "Type": "string"
#                }
#             ],
#             "EyeDirection": { 
#                "Confidence": number,
#                "Pitch": number,
#                "Yaw": number
#             },
#             "Eyeglasses": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "EyesOpen": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "FaceOccluded": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Gender": { 
#                "Confidence": number,
#                "Value": "string"
#             },
#             "Landmarks": [ 
#                { 
#                   "Type": "string",
#                   "X": number,
#                   "Y": number
#                }
#             ],
#             "MouthOpen": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Mustache": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Pose": { 
#                "Pitch": number,
#                "Roll": number,
#                "Yaw": number
#             },
#             "Quality": { 
#                "Brightness": number,
#                "Sharpness": number
#             },
#             "Smile": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Sunglasses": { 
#                "Confidence": number,
#                "Value": boolean
#             }
#          }
#       }
#    ],
#    "OrientationCorrection": "string",
#    "UnindexedFaces": [ 
#       { 
#          "FaceDetail": { 
#             "AgeRange": { 
#                "High": number,
#                "Low": number
#             },
#             "Beard": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "BoundingBox": { 
#                "Height": number,
#                "Left": number,
#                "Top": number,
#                "Width": number
#             },
#             "Confidence": number,
#             "Emotions": [ 
#                { 
#                   "Confidence": number,
#                   "Type": "string"
#                }
#             ],
#             "EyeDirection": { 
#                "Confidence": number,
#                "Pitch": number,
#                "Yaw": number
#             },
#             "Eyeglasses": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "EyesOpen": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "FaceOccluded": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Gender": { 
#                "Confidence": number,
#                "Value": "string"
#             },
#             "Landmarks": [ 
#                { 
#                   "Type": "string",
#                   "X": number,
#                   "Y": number
#                }
#             ],
#             "MouthOpen": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Mustache": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Pose": { 
#                "Pitch": number,
#                "Roll": number,
#                "Yaw": number
#             },
#             "Quality": { 
#                "Brightness": number,
#                "Sharpness": number
#             },
#             "Smile": { 
#                "Confidence": number,
#                "Value": boolean
#             },
#             "Sunglasses": { 
#                "Confidence": number,
#                "Value": boolean
#             }
#          },
#          "Reasons": [ "string" ]
#       }
#    ]
# }