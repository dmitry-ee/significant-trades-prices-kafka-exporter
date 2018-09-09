#!/bin/bash

container_name="stpke"

docker rmi $(docker images | grep ${container_name} | awk '{ print $1 }')
docker run --rm \
  --name=${container_name} \
  --network=host \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e "LOG_LEVEL=INFO" \
  -e "STPKE_KAFKA_URL=localhost:9092" \
  -e "STPKE_MONGO_URL=localhost:27017" \
  -e "STPKE_DEFAULT_DB=whale-trades" \
  -e "STPKE_SLEEP_MS=120000" \
  dmi7ry/${container_name}:latest
