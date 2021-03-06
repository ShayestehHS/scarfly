FROM python:3.9-alpine3.13
LABEL MAINTAINER="ShayestehHS"

WORKDIR /app
ADD ./backend/requirements.txt /app/backend/

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update postgresql-client

## install Pillow dependencies
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

COPY backend/requirements.txt /requirements.txt

RUN apk add --update --virtual .tmp-deps \
        build-base libffi-dev openssl-dev gcc postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt

COPY scripts /scripts
COPY ./backend /app

WORKDIR /app
EXPOSE 8000

RUN apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R a+rwx **/migrations/ && \
    chmod -R 777 /py/lib/python3.9/site-packages/admin_honeypot/migrations/ && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]