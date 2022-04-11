FROM python:3.9-alpine3.13
LABEL MAINTAINER="ShayestehHS"

WORKDIR /app
ADD ./backend/requirements.txt /app/backend/

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update postgresql-client

RUN pip install --upgrade pip

RUN pip install gunicorn

## install Pillow
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install Pillow==9.0.1

RUN apk add --update --virtual .tmp-deps \
        build-base libffi-dev openssl-dev gcc postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt

RUN apk del .tmp-deps

ADD ./docker /app/docker
ADD ./backend /app/backend