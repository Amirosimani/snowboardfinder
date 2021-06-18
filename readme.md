# Snow Authority

# The Source Code

folder structure

## Lambda functions

### Web Scraper
This project containerises a web scraper that can query the good ride website and then scrape and save all the snowboard reviews and ratings.

The src code for the web scraper is found in the `lambda-scra[er`; app.py contains the lambda function handler and modules scraper and aws_s3 are helper modules for scraping and persisting to S3 respectively.

#### Building the container

The Dockerfile contains the instructions to build this image. You can run the command to create the image lambda/web-scraper version latest

	docker build -t lambda/web-scraper:latest .

#### running the container locally

The image can be run locally before you deploy to deploy to AWS Lambda. Providing you already have AWS credentials setup in `~/.aws/credentials` you can simply run the command.

	docker run -p 9000:8080 -v ~/.aws/:/root/.aws/ lambda/web-scraper:latest


The -v flag mounts your local AWS credentials into the docker container allowing it access to your AWS account and S3 bucket.

To confirm the container is working as it should locally, you can run a similar command to

	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"query":"labrador", "count":3
	, "bucket":"my-dogs", "folder_path":"local/"}'


This command intends to query google images for 'labrador', scrape the first 3 images returned and then persist them to a bucket called 'my-dogs' within a 'folder' called 'local'. A successful result should return something like this...

"Successfully loaded 3 images to bucket my-dogs. Folder path local/ and file names ['4ddebbca9a.jpeg', 'eafde83cd9.jpeg
', 'b61b601eea.jpeg']."
The image names are based on a hash of their data so the names are likely to differ. You can also verify the result by checking your S3 bucket on AWS.


-----



link: https://main.dewjwq19opv7d.amplifyapp.com/



web scraper: https://github.com/rchauhan9/image-scraper-lambda-container
bucket: 

----
TODO:
[ ] calculate simialrity statistics i.e you can compare recommendations with all k-similar boards
