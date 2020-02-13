FROM python:3.7.4-alpine

#RUN adduser --disabled-password --gecos '' kisseklyv_user

RUN adduser -D kisseklyv_user

WORKDIR /home/kisseklyv_user

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY kisseklyv kisseklyv
COPY migrations migrations
COPY run.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R kisseklyv_user:kisseklyv_user ./
USER kisseklyv_user

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]