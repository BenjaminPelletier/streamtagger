#!/bin/bash

if [[ $(docker container ls) == *"streamtagger_ui"* ]]; then
  echo Stopping and removing old ui container...
  docker container kill streamtagger_ui
  docker container rm streamtagger_ui
fi

docker pull streamtagger/ui

docker run \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=10 \
  --name streamtagger_ui \
  --restart always \
  --network=streamtagger \
  -v "${PWD}/storage/media:/var/media" \
  -e ST_DB_CONNECTIONSTRING="host=streamtagger_db port=26257 dbname=streamtagger user=root password=" \
  -p 5000:5000 -d streamtagger/ui
