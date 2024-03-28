# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# Install necessary system packages, including gcc
RUN apt-get update \
    && apt-get install -y pkg-config default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV FLASK_APP=app.py
EXPOSE 5000

CMD [ "python3", "app.py"]

