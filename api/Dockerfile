FROM python:3

WORKDIR /backend-api

ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt

RUN pip install pip --upgrade
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]