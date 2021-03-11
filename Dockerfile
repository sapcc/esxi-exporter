#FROM python:3-alpine
FROM keppel.eu-de-1.cloud.sap/ccloud-dockerhub-mirror/library/python:3-alpine

# https://cryptography.io/en/latest/installation.html#alpine
# Merged with run apk add from old exporter because nacl failed to build
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo ca-certificates build-base libxslt libffi-dev libxml2-dev libxslt-dev

ADD . exporter

RUN pip install --upgrade pip
RUN pip install --upgrade -r  exporter/requirements.txt

RUN apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo build-base libxml2-dev libxslt-dev

WORKDIR exporter/
