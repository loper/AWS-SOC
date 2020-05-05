FROM python:3.8-alpine

RUN adduser -D soc

RUN apk add bash vim

WORKDIR /home/soc
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip boto3
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY src ./
COPY boot.sh ./
COPY prod-config.py ./config.py
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R soc:soc ./

USER soc

VOLUME ["/data"]
EXPOSE 5000
ENV DATA_DIR /data
ENTRYPOINT ["./boot.sh"]
