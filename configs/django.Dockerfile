FROM ubuntu:latest

MAINTAINER nikrom2012@me.com

RUN apt-get update
RUN apt-get install -y python3 python3-pip graphviz libgraphviz-dev pkg-config

ADD ./ctforces_backend/requirements.txt /
RUN pip3 install -U pip
RUN pip3 install -Ur /requirements.txt
RUN pip3 install gunicorn

ADD ./ctforces_backend /app

WORKDIR /app

RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput -v 3

CMD ["gunicorn", "--access-logfile", "/logs/access.log", "--error-logfile", "/logs/error.log", "--workers", "3", "--timeout", "120", "--bind", "unix:/socks/ctforces.sock", "ctforces_backend.wsgi:application"]
