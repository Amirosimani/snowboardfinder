import scraper
import aws_s3 as s3s


def handler(event, context):
    scr = scraper.GearScraper()

    board_ratings = scr.parse(event['gender'])

    key = event['folder_path'] + event['gender'] + '.json'
    s3s.upload_object(board_ratings, event['bucket'], key)
    scr.close_connection()
    # return f"Successfully scraped {event['gender']} and loaded snowboard ratings to {event['bucket']}{event['folder_path']}"
