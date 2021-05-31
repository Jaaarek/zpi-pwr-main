FROM ubuntu

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos  --uid $USER_ID --gid $GROUP_ID user
USER user


FROM python:3.6-buster

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update && \
    apt-get -y install gcc mono-mcs libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get -y install cmake protobuf-compiler

RUN pip3 install face-recognition

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENV FLASK_DEBUG=1

ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=16000"]

