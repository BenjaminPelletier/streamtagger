# docker image build -f Dockerfile -t streamtagger/ui ../ui

FROM python:3.7-buster

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get -y install libtag1-dev python3-dev && \
    pip install flask gunicorn jinja2 psycopg2 pytaglib

COPY . .

CMD gunicorn streamtagger:app -b 0.0.0.0:5000 --access-logfile -

EXPOSE 5000
