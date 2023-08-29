FROM python:3.11-slim

WORKDIR /app

COPY ./system /app
COPY ./system/requirements.txt /app

RUN pip3 install -r ./requirements.txt --no-cache-dir