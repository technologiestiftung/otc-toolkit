#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
# This script expects the path to the docker-compose setup
# as first argument
# docker-compose restart assumes that the docker environment was already created
PLATFORM=docker

print_usage() {
  printf "\n\nUsage:------------------------------\n"
  printf "Usage: %s -p <docker|tx2> /absolut/path/to/docker-compose/or/opendatacam/folder\n" "${0}"
  printf "       If -p flag is not specified it will use '%s'\n" $PLATFORM
  printf "       valid options are docker or tx2\n"
  printf "       If -h flag is specified it will print the help and exit\n\n"
}

while getopts 'hp:' flag; do
  case "${flag}" in
    p) PLATFORM="$OPTARG" ;;
    h) print_usage
       exit 0 ;;
  esac
done
shift $(($OPTIND - 1))

function main() {
  if [[ "$PLATFORM" != "docker" && "$PLATFORM" != "tx2" ]]; then
    print_usage;
    exit 1;
  fi

  if [[ "$PLATFORM" == "docker" ]]; then 
    echo "running with docker"
    cd "$1"
    docker-compose restart
  elif [[ "$PLATFORM" == "tx2" ]]; then
    echo "running with pm2 on bare metal"
    pm2 restart /home/otc-admin/otc/otc-toolkit/ecosystem.config.js 
  else
   print_usage;
   exit 1;
  fi
}

main "$1"
