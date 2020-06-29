#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
# This script expexts the path to the docker-compose setup
# as first argument

function main() {
  cd "$1"
  docker-compose stop
}

main "$1"
