#!/bin/bash

./build_ui.sh
./start_ui.sh

docker container logs --follow streamtagger_ui
