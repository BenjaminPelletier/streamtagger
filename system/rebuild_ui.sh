#!/bin/bash

docker container kill streamtagger_ui
docker container rm streamtagger_ui
echo 'ID of old image:'
docker inspect -f "{{ .Id }}" streamtagger/ui
docker image build -f Dockerfile -t streamtagger/ui ../ui
echo 'ID of new image:'
docker inspect -f "{{ .Id }}" streamtagger/ui
./start_ui.sh
echo 'ID of final image:'
docker inspect -f "{{ .Id }}" streamtagger/ui
docker container logs --follow streamtagger_ui
