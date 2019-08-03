#!/bin/bash

case $(uname -m) in
armv7l)
  base_image_name="arm32v7/python:3.7-buster"
  image_name="streamtagger/ui:rpiv7"
  ;;
x86_64)
  base_image_name="python:3.7-buster"
  image_name="streamtagger/ui"
  ;;
*)
  echo Unsupported architecture "$(uname -m)"
  exit 1
esac

if [[ $(docker container ls) == *"${image_name}"* ]]; then
  echo Stopping and removing old ui container...
  docker container kill streamtagger_ui
  docker container rm streamtagger_ui
fi

if [[ $(docker image ls) == *"${image_name}"* ]]; then
  echo 'ID of old image:'
  docker inspect -f "{{ .Id }}" ${image_name}
fi

eval "echo \"$(cat Dockerfile_template)\"" > Dockerfile

docker image build -f Dockerfile -t ${image_name} ../ui

echo 'ID of new image:'
docker inspect -f "{{ .Id }}" ${image_name}
