FROM apache/airflow:2.3.4-python3.9

USER root

RUN apt update

USER airflow

WORKDIR /opt/airflow

COPY requirements.txt /opt/airflow

RUN pip install -U pip install -r requirements.txt
