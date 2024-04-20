# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster as base

# Install necessary system packages, including gcc
RUN apt-get update \
    && apt-get install -y pkg-config default-libmysqlclient-dev gcc git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
EXPOSE 5000

# Set entrypoint script as executable
RUN chmod +x entrypoint.sh

# Use a minimal production image
FROM base as production

ENTRYPOINT ["./entrypoint.sh"]

