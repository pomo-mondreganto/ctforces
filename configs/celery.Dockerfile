FROM ubuntu:latest

MAINTAINER nikrom2012@me.com

RUN apt-get update
RUN apt-get install -y python3-dev python3-pip graphviz libgraphviz-dev pkg-config

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -U pip
RUN pip3 install -Ur /requirements.txt

WORKDIR /app
RUN useradd celery
USER celery

CMD ["/usr/local/bin/celery", "-A", "ctforces_backend", "worker", "--concurrency", "20", "-E", "-l", "info", "--statedb=/celery/celery.state"]