FROM python:3.7-alpine

MAINTAINER nikrom2012@me.com

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache gcc musl-dev postgresql-dev zlib-dev jpeg-dev && \
    apk add --no-cache graphviz-dev

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -r /requirements.txt
ADD ./ctforces_backend /app

ADD ./configs/django.start.sh /entrypoint.sh
ADD ./configs/db.check.py /db.check.py
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
