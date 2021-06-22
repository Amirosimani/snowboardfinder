import similarity
import aws_s3 as s3s
import boto3


def handler(event, context):
    sim = similarity.Similarity()
    key = event['folder_path'] + event['gender'] + '.json'

    # get scraped file from S3
    scraped_json = s3s.download_object(event['bucket'], key)
    print("1/3 snowboard reviews are loaded...")
    # calculate most similar boards
    df = sim.calculate_similarity(scraped_json)
    print("2/3 similarity scores calculated...")
    tmp_file = f"/tmp/{event['gender']}.csv"
    df.to_csv(tmp_file, index=False)

    key = 'sim/' + event['gender'] + '.csv'
    s3s.upload_csv(tmp_file, event['bucket'], key)

    return f"Successfully calculated top most similar boards and saved it to {event['bucket']}/{key}"
