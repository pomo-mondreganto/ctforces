FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /app
ADD ./backend/requirements.txt .
RUN pip install -r requirements.txt
ADD ./backend .

ADD ./configs/celery/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nobody

CMD ["/entrypoint.sh"]
