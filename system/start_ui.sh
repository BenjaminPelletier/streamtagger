#!/bin/bash

case $(uname -m) in
armv7l)
  image_name="streamtagger/ui:rpiv7"
  ;;
x86_64)
  image_name="streamtagger/ui"
  ;;
*)
  echo Unsupported architecture $(uname -m)
  exit 1
esac

if [[ $(docker container ls) == *"streamtagger_ui"* ]]; then
  echo Stopping and removing old ui container...
  docker container kill streamtagger_ui
  docker container rm streamtagger_ui
fi

docker run \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=10 \
  --name streamtagger_ui \
  --restart always \
  --network=streamtagger \
  -v "${PWD}/storage/media:/var/media" \
  -e ST_DB_CONNECTIONSTRING="host=streamtagger_db port=5432 user=streamtagger password=mysecretpassword" \
  -e PYTHONUNBUFFERED=TRUE \
  -p 5000:5000 -d ${image_name}
