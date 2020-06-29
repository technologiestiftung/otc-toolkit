#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
# This script expexts the path to the docker-compose setup
# as first argument
# docker-compose start assumes that the docker environment was already created

function main() {
  cd "$1"
  docker-compose start
}

main "$1"
