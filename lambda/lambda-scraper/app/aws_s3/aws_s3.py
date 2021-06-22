import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format='%(asctime)s %(levelname)s %(process)d --- %(name)s %(funcName)20s() : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


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
