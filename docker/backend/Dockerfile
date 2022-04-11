FROM python:3.9-alpine3.13
LABEL MAINTAINER="ShayestehHS"

WORKDIR /app
ADD ./backend/requirements.txt /app/backend/


RUN pip install --upgrade pip

RUN pip install gunicorn

## install Pillow
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install Pillow==9.0.1

RUN pip install -r backend/requirements.txt

ADD ./docker /app/docker
ADD ./backend /app/backend