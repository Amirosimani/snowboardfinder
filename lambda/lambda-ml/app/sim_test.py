import os
import boto3
import urllib.parse
import pandas as pd
from  similarity import similarity
import aws_s3.aws_s3 as s3s

print('Loading function')

s3 = boto3.client('s3')


if __name__ == '__main__':
    bucket='snowboard-finder'
    key='raw/mens.json'

    sim = similarity.Similarity()
    # get scraped file from S3
    scraped_json = s3s.download_object(bucket, key)
    print("1/3 snowboard reviews are loaded...")

    df = pd.json_normalize(scraped_json)
    print(df.head())
    print(df.columns)
    # print(df.shape)
    # # calculate most similar boards
    df = sim.calculate_similarity(scraped_json)
    # print("2/3 similarity scores calculated...")
    # tmp_file = f"/tmp/{gender}.csv"
    # df.to_csv(tmp_file, index=False)
    #
    # upload_key = 'sim/' + gender + '.csv'
    # s3s.upload_csv(tmp_file, bucket, upload_key)
    #
    # return f"Successfully calculated top most similar boards and saved it to {bucket}/{upload_key}"
