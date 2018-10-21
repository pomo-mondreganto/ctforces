FROM ubuntu:latest

MAINTAINER nikrom2012@me.com

RUN apt-get update
RUN apt-get install -y python3 python3-pip graphviz libgraphviz-dev pkg-config

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -U pip
RUN pip3 install -Ur /requirements.txt
RUN pip3 install gunicorn

ADD ./configs/django.start.sh /entrypoint.sh
ADD ./configs/db.check.py /db.check.py
RUN chmod +x /entrypoint.sh

CMD ["./entrypoint.sh"]