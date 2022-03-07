FROM alpine:3.15

RUN mkdir /flask_app
COPY . /flask_app/
WORKDIR /flask_app

RUN apk add --update python3 py3-pip \
    && pip3 install -r requirements.txt

EXPOSE 5000

CMD ["./app.py"]