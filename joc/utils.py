import boto3
from django.conf import settings
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

def upload_to_s3(file, file_name):
    file_content = file.read()
    try:
        s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_name, Body=file_content, ContentType=file.file.content_type)
        return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
    except (NoCredentialsError, PartialCredentialsError) as e:
        return f"Credential error: {str(e)}"
    except ClientError as e:
        return f"Client error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
