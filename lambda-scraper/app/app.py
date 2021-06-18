import scraper
import aws_s3 as s3s


def handler(event, context):
    scr = scraper.GearScraper()

    for gender in ['mens', 'womens']:
        board_ratings = scr.parse(gender)

        key = event['folder_path'] + gender + '.json'
        s3s.upload_object(board_ratings, event['bucket'], key)
    scr.close_connection()
    # return "Successfully loaded"
