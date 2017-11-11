FROM python:3.6.3

MAINTAINER Corey Burmeister "burmeister.corey@gmail.com"

RUN mkdir -p /var/www/flask-bones
WORKDIR /var/www/flask-bones

ADD requirements.txt /var/www/flask-bones/
RUN pip install -r requirements.txt

ADD . /var/www/flask-bones
