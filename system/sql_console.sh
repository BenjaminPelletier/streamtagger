#!/bin/bash

docker container exec -it streamtagger_db sh cockroach.sh sql --insecure
