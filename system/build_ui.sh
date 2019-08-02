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
  echo Unsupported architecture $(uname -m)
  exit 1
esac

echo ${base_image_name}

eval "echo \"$(cat Dockerfile_template)\"" > Dockerfile

docker image build -f Dockerfile -t ${image_name} ../ui
