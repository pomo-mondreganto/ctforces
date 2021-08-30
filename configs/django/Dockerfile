FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /app
ADD ./backend/requirements.txt .
RUN pip install -r requirements.txt
ADD ./backend .

ADD ./configs/django/entrypoint.sh /entrypoint.sh
ADD ./configs/db.check.py /db.check.py
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
