#!/bin/bash

if [[ $(docker network ls) != *"streamtagger"* ]]; then
  echo Creating docker network 'streamtagger'...
  docker network create streamtagger
fi

if [[ $(docker container ls) == *"streamtagger_db"* ]]; then
  echo Stopping and removing old db container...
  docker container kill streamtagger_db
  docker container rm streamtagger_db
fi

echo Starting new streamtagger_db container
docker run \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=10 \
  --name streamtagger_db \
  --restart always \
  --network=streamtagger \
  -v ${PWD}/storage/db:/cockroach/cockroach-data \
  -p 26257:26257 \
  -p 8888:8080 -d cockroachdb/cockroach:v19.1.3 \
  start --insecure
