#!/bin/bash

docker network create myapp_network
docker-compose up -d

cd tests || exit
docker-compose up -d
cd code || exit

pytest -lsv -n4 --selenoid_vnc
