FROM python:3.6-alpine

RUN adduser -D player

WORKDIR /home/player

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY player ./
COPY favicon.ico ./

COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R player:player ./
USER player

EXPOSE 5000
VOLUME ["/home/player/data"]
ENTRYPOINT ["./boot.sh"]
