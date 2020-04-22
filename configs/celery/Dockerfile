FROM python:3.7

MAINTAINER pomo_mondreganto

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq-dev libgraphviz-dev

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -r /requirements.txt
ADD ./ctforces_backend /app

ADD ./configs/celery/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nobody

CMD ["/entrypoint.sh"]
