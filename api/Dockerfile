FROM python:3

LABEL maintainer="Liang Sun <sunly917@gmail.com>"

WORKDIR /backend-api

ENV FLASK_APP server.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt

RUN pip install pip --upgrade
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]