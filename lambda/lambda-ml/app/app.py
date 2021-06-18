# import scraper
import aws_s3 as s3s


def handler(event, context):

    key = event['folder_path'] + event['gender'] + '.json'
    s3s.download_object(event['bucket'], key)

    # return f"Successfully scraped {event['gender']} and loaded snowboard ratings to {event['bucket']}{event['folder_path']}"
