FROM python:3.9.15-alpine3.16

WORKDIR /home

ENV ARCH_TYPE="Lite"
ENV BOT_ADDRESS="@<your_tg_bot_name>"
ENV API_KEY="<your_api_key>"

COPY *.py ./
COPY requirements.txt ./

RUN apk update && apk upgrade
RUN pip install -U pip install -r requirements.txt

ENTRYPOINT ["python", "bot_run.py"]
