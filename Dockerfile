#FROM python:3-alpine
FROM keppel.eu-de-1.cloud.sap/ccloud-dockerhub-mirror/library/python:3-alpine
#FROM python:3-slim

# https://cryptography.io/en/latest/installation.html#alpine
ADD . exporter
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo make ca-certificates && \
    apk upgrade && \ 
    pip install --upgrade --no-cache-dir pip && \
    pip install --no-cache-dir -r  exporter/requirements.txt && \
    apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo make 


WORKDIR exporter/