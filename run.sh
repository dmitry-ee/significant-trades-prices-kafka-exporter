#!/bin/bash

export LOG_LEVEL=WARN
export STPKE_KAFKA_URL="localhost:9092"
export STPKE_MONGO_URL="localhost:27017"
export STPKE_DEFAULT_DB="whale-trades"
export STPKE_SLEEP_MS=120000
set -e
python3 -m src
