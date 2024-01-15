#!/bin/bash

docker build -t tracer:ubuntu -f ./tracer/Dockerfile.tracer .
docker build -t server:ubuntu -f ./server/Dockerfile.server .
python3 containernet_opentelemetry.py

# Do on terminal for a complete cleaning !
## Clear mininet cache
#> mn -c
## Clear docker (if wanted)
#> sudo docker system prune
#> sudo docker rmi -f $(sudo docker images)
