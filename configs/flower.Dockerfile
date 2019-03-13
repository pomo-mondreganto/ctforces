FROM python:3.7

MAINTAINER nikrom2012@me.com

RUN apt-get update && apt-get install -y python3-dev python3-pip graphviz libgraphviz-dev pkg-config

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -r /requirements.txt
ADD ./ctforces_backend /app

ADD ./configs/flower.start.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN useradd celery
USER celery

CMD ["/entrypoint.sh"]
