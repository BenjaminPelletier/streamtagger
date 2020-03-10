#!/bin/bash

echo This script is starting the adminer database web UI.
echo After allowing adminer to start, visit http://localhost:8080 in a browser.

docker run --network=streamtagger --link streamtagger_db -p 8080:8080 adminer
