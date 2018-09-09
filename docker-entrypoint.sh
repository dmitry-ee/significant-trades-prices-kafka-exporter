#!/bin/bash

RED='\033[0;31m'  # Red color
NC='\033[0m'      # No Color

echo -e "\nHELLO THERE! THIS IS SIGNIFICANT TRADE PRICES KAFKA EXPORTER"
echo -e "Project ${RED}https://github.com/dmitry-ee/significant-trades-prices-kafka-exporter${NC}"
echo -e "Liked? Donate: ${RED}ETH:0xfc4c960baaae1a91e7ebcdab2056c35e9d4df4ac${NC}\n"

if [ ! -z "$VERBOSE" ]; then
  printenv
  set -ex
fi

if [[ "$1" == "run" ]]; then
  exec python -m src
fi

exec "$@"
