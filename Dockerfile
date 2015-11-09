FROM python:2.7.9

RUN mkdir -p /var/www/flask-bones
WORKDIR /var/www/flask-bones
ADD requirements.txt /var/www/flask-bones/
RUN pip install -r requirements.txt
ADD . /var/www/flask-bones
