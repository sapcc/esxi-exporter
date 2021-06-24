FROM keppel.eu-de-1.cloud.sap/ccloud-dockerhub-mirror/library/alpine:latest

# https://cryptography.io/en/latest/installation.html#alpine
RUN apk --update add --no-cache python3 openssl bash git gcc musl-dev python3-dev libffi-dev openssl-dev cargo make ca-certificates py3-pip && \
    apk upgrade
RUN git config --global http.sslVerify false
RUN git clone https://github.com/sapcc/esxi-exporter
RUN pip3 install --upgrade pip

ADD . esxi-exporter/
RUN pip3 install --upgrade -r esxi-exporter/requirements.txt

WORKDIR esxi-exporter/
