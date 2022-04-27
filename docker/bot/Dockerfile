FROM python:3.8-slim AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv

RUN mkdir -p /telegram_bot /storage

COPY ../../telegram_bot/requirements.txt /telegram_bot
RUN pip3 install -r /telegram_bot/requirements.txt

ADD ../../telegram_bot /telegram_bot
WORKDIR /telegram_bot

COPY ../../telegram_bot/main.py /telegram_bot/main.py
CMD ["python3" ,"/telegram_bot/main.py"]
