import json
import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format='%(asctime)s %(levelname)s %(process)d --- %(name)s %(funcName)20s() : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def download_object(bucket: str, key: str):
    s3_client = boto3.client('s3')
    try:
        s3_response_object = s3_client.get_object(Bucket=bucket, Key=key)
        object_content = s3_response_object['Body'].read().decode('utf-8')
        json_content = json.loads(object_content)
        return json_content
    except ClientError as e:
        logging.error(e)


def upload_object(object: bytes, bucket: str, key: str) -> bool:
    """
    Upload an image file to an S3 bucket

    object: The file in bytes to upload to s3
    bucket: Bucket to upload to
    key: The key to save the object as

    Returns:
        True if file was uploaded, else False
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Body=object, Bucket=bucket, Key=key)
        logging.info(f"Successfully uploaded object to '{bucket}' as '{key}'.")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_csv(local_path, bucket, key) -> bool:
    """

    Args:
        local_path:
        bucket:
        key:

    Returns:

    """
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.upload_file(local_path, bucket, key)
        logging.info(f"Successfully uploaded object to '{bucket}' as '{key}'.")
    except ClientError as e:
        logging.error(e)
        return False
    return True
