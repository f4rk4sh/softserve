FROM ubuntu:20.04

RUN mkdir /flask_app
COPY . /flask_app/
WORKDIR /flask_app

RUN apt-get update && apt-get upgrade -y
RUN apt install -y python3.8
RUN apt install -y python3-pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ./app.py