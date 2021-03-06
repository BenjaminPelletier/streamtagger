#!/bin/bash

case $(uname -m) in
armv7l)
  image_name="arm32v7/postgres"
  ;;
x86_64)
  image_name="postgres"
  ;;
*)
  echo Unsupported architecture $(uname -m)
  exit 1
esac

if [[ $(docker network ls) != *"streamtagger"* ]]; then
  echo Creating docker network 'streamtagger'...
  docker network create streamtagger
fi

if [[ $(docker container ls) == *"streamtagger_db"* ]]; then
  echo Stopping and removing old db container...
  docker container kill streamtagger_db
  docker container rm streamtagger_db
fi

mkdir -p storage/db

echo Starting new streamtagger_db container
docker run \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=10 \
  --name streamtagger_db \
  --restart always \
  --network=streamtagger \
  -e POSTGRES_USER=streamtagger \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v ${PWD}/storage/db:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d ${image_name}
