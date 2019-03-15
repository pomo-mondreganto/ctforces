FROM python:3.7-alpine

MAINTAINER nikrom2012@me.com

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache gcc musl-dev postgresql-dev zlib-dev jpeg-dev && \
    apk add --no-cache graphviz-dev

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -r /requirements.txt
ADD ./ctforces_backend /app

RUN adduser -S celery
USER celery

WORKDIR /app
CMD ["/usr/local/bin/celery", "-A", "ctforces_backend", "worker", "--concurrency", "20", "-E", "-l", "info", "--statedb=/celery/celery.state"]
