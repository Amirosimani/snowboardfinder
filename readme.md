# Snow Authority

# The Source Code

folder structure

----
## Lambda Functions

* Web Scraper
* Machine Learning

#### Web Scraper
This project containerises a web scraper that can query the good ride website and then scrape and save all the snowboard reviews and ratings.

The src code for the web scraper is found in the `lambda-scraper`; app.py contains the lambda function handler and modules scraper and aws_s3 are helper modules for scraping and persisting to S3 respectively.

#### Machine Learning

### Building the container

The Dockerfile contains the instructions to build this image. This guide shows the steps you need to take for the webs scraper as an example. However, same steps apply to other lambda functions.

You can run the command to create the image lambda/web-scraper version latest

	docker build -t lambda/web-scraper:latest .

#### Running the container locally

The image can be run locally before you deploy to deploy to AWS Lambda. Providing you already have AWS credentials setup in `~/.aws/credentials` you can simply run the command.

	docker run -p 9000:8080 -v ~/.aws/:/root/.aws/ lambda/web-scraper:latest


The -v flag mounts your local AWS credentials into the docker container allowing it access to your AWS account and S3 bucket.

To confirm the container is working as it should locally, you can run a similar command to

	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"bucket":"snowboard-finder", "folder_path":"raw/", "gender":"mens"}'


This command intends to query the website, scrape the ratings for both mens and womens boards and then persist them to a bucket called 'snowboard-finder' within a 'folder' called 'raw'.

#### Deploying to Lambda

AWS Lambda can now take an image to run as a serverless function. At the time of writing this feature is limited to certain regions so you will need to carefully select the region. For extra help, AWS have published a guide to working with containers in Lambda https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html.

You will also need to create an Elastic Container Registry within AWS - a place to store your Docker images so they can be used by Lambda. For extra help, AWS have published a guide to working with ECR https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html.

```bash
# Authenticate the Docker CLI to your Amazon ECR registry.
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT ID>.dkr.ecr.us-east-1.amazonaws.com

# Create a repository in Amazon ECR 
aws ecr create-repository --repository-name snowboard-ml --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE


#Tag the image to match  repository name, and deploy the image to Amazon ECR
docker tag lambda/web-scraper <ACCOUNT ID>.dkr.ecr.us-east-1.amazonaws.com/snowboard-web-scraper:latest
docker push <ACCOUNT ID>.dkr.ecr.us-east-1.amazonaws.com/snowboard-web-scraper:latest

```

testing on AWS for both scraper and ml

```json
{
  "gender": "mens",
  "bucket": "snowboard-finder",
  "folder_path": "raw/"
}

```

sample test for S3 object change

```json
{
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-west-2",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "<BUCKET NAME>",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::<BUCKET NAME>"
        },
        "object": {
          "key": "<KEY>",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}

```

link: https://main.d1dbeq6kwnylr9.amplifyapp.com/

web scraper: https://github.com/rchauhan9/image-scraper-lambda-container
bucket: 
---
## Web

Using react
source: https://medium.com/crobyer/search-filter-with-react-js-88986c644ed5


----
TODO:
[ ] scraper: multi-threaded scraping
[ ] web: clean up/format names: drop -snowboard-review, remove extra -
[ ] similarity percentiles over all boards
