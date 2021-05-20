FROM python:3.6-buster

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get -y install gcc mono-mcs libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_DEBUG=1

ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=11000"]
