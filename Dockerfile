FROM keppel.eu-de-1.cloud.sap/ccloud-dockerhub-mirror/library/python:3-alpine

RUN apk --update add openssl ca-certificates build-base libxslt libffi-dev openssl-dev libxml2-dev libxslt-dev

ADD . exporter

RUN pip install --upgrade pip
RUN pip install --upgrade -r  exporter/requirements.txt

RUN apk del build-base libffi-dev openssl-dev libxml2-dev libxslt-dev

WORKDIR exporter/
