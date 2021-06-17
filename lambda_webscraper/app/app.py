
import scraper
import aws_s3 as s3s


def handler(event, context):
    scr = scraper.Scraper()

    scr.scraper()
    # scr.close_connection()
    # return "Successfully loaded {} images to bucket {}. Folder path {} and file names {}.".format(event['count'],
                                                                                                  event['bucket'],
                                                                                                  event['folder_path'],
                                                                                                  files)