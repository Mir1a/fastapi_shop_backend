import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        response = s3.upload_file(file_name, bucket, object_name)
        return response
    except Exception as e:
        print(e)
        return None


def download_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        response = s3.download_file(bucket, object_name, file_name)
        with open(file_name, 'rb') as file:
            return file.read()
    except Exception as e:
        print(e)
        return None
