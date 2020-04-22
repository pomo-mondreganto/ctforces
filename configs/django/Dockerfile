FROM python:3.7

MAINTAINER pomo_mondreganto

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq-dev libgraphviz-dev

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -r /requirements.txt
ADD ./ctforces_backend /app

ADD ./configs/django/entrypoint.sh /entrypoint.sh
ADD ./configs/db.check.py /db.check.py
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
