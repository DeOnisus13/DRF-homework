FROM python:3.11-slim

WORKDIR /drf-app

COPY /requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt --no-cache-dir

COPY . .
