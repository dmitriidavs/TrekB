FROM python:3.9.15-alpine3.16

WORKDIR /app

COPY modules modules
COPY .env .
COPY app.py .
COPY requirements.txt .

RUN apk update && apk upgrade
RUN apk add --no-cache sqlite
RUN pip install -U pip install -r requirements.txt

RUN mkdir storage
RUN sqlite3 storage/users.db < modules/database/ddl.sql