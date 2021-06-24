# Define global args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.8"
ARG DISTRO_VERSION="3.12"


# Stage 1 - bundle base image + runtime
# Grab a fresh copy of the image and install GCC
FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine
# Install GCC (Alpine uses musl but we compile and link dependencies with GCC)


# Stage 2 - build function and dependencies
FROM python-alpine AS build-image
# Include global args in this stage of the build
ARG FUNCTION_DIR
ARG RUNTIME_VERSION
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}
RUN apk update \
    && apk add gcc python3-dev
COPY requirements.txt .
RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}


# Stage 4 - final runtime image
# Grab a fresh copy of the Python image
FROM python-alpine
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
RUN  apk add chromium chromium-chromedriver
COPY src/* ${FUNCTION_DIR}
CMD [ "python", "./scraper.py"  ]