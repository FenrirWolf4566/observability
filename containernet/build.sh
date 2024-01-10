#!/bin/bash

docker build -t pinger:ubuntu1804 -f Dockerfile.pinger .
docker build -t receiver:ubuntu1804 -f Dockerfile.receiver .
python3 containernet_example.py

# Do on terminal for a complete cleaning !
## Clear mininet cache
#> mn -c
## Clear docker (if wanted)
#> sudo docker system prune
#> sudo docker rmi -f $(sudo docker images)



