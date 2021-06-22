# Define gloval args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.8"
ARG DISTRO_VERSION="3.12"

# Stage 1 - bundle base image + runtime
# Grab a fresh copy of the image
FROM python:${RUNTIME_VERSION}-buster AS build-image
# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG RUNTIME_VERSION
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}
# Install the runtime interface client
RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}

# Stage 2 - Add app related dependencies
FROM build-image as build-image2
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
COPY requirements.txt .
RUN pip install -r requirements.txt --target ${FUNCTION_DIR}


# Stage 3 - final runtime image
# Grab a fresh copy of the Python image
FROM build-image
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
COPY --from=build-image2 ${FUNCTION_DIR} ${FUNCTION_DIR}
# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
# Copy handler function
COPY app/* ${FUNCTION_DIR}
COPY entry.sh /
RUN chmod +x /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.handler" ]
