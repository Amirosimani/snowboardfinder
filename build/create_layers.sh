docker run --rm -v $(pwd):/. -w . lambci/lambda:build-python3.8 \
pip install pandas==1.1.5 -t python

