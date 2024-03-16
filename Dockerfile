FROM python:3.12.2-bookworm

COPY fetch.py /opt/fetch/fetch
COPY requirements.txt /opt/fetch/requirements.txt

RUN ["chmod", "+x", "/opt/fetch/fetch"]

RUN pip3 install --no-cache-dir -r /opt/fetch/requirements.txt

WORKDIR /opt/fetch

RUN /bin/bash
