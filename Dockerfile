FROM python:2.7.15-alpine

COPY . /

RUN apk add py-pip && pip install boto3
