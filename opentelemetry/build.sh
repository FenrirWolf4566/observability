#!/bin/bash

docker build -t zipkin:ubuntu -f ./zipkin/Dockerfile.zipkin .
docker build -t server:ubuntu -f ./server/Dockerfile.server .

python3 containernet_opentelemetry.py

# Do on terminal for a complete cleaning !
## Clear mininet cache
#> mn -c
## Clear docker (if wanted)
#> sudo docker system prune
#> sudo docker rmi -f $(sudo docker images)