import similarity_functions
import aws_s3 as s3s


def handler(event, context):
    sim = similarity_functions.Similarity()
    key = event['folder_path'] + event['gender'] + '.json'

    # get scraped file from S3
    scraped_json = s3s.download_object(event['bucket'], key)
    # calculate most similar boards
    df = sim.calculate_similarity(scraped_json)

    return f"Successfully calculated top most similar boards"
