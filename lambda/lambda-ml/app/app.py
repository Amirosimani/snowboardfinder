import os
import boto3
import urllib.parse
import similarity
import aws_s3 as s3s

print('Loading function')

s3 = boto3.client('s3')


def handler(event, context):
    # Get the object from the event and show its content type
    try:
        key = event['folder_path'] + event['gender'] + '.json'
        bucket = event['bucket']
        gender = event['gender']
    except KeyError as e:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        base = os.path.basename(key)
        gender = os.path.splitext(base)[0]

    sim = similarity.Similarity()
    # get scraped file from S3
    scraped_json = s3s.download_object(bucket, key)
    print("1/3 snowboard reviews are loaded...")
    # calculate most similar boards
    df = sim.calculate_similarity(scraped_json)
    print("2/3 similarity scores calculated...")
    tmp_file = f"/tmp/{gender}.csv"
    df.to_csv(tmp_file, index=False)

    upload_key = 'sim/' + gender + '.csv'
    s3s.upload_csv(tmp_file, bucket, upload_key)

    return f"Successfully calculated top most similar boards and saved it to {bucket}/{upload_key}"
