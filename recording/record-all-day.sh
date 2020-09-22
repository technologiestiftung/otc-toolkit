#!/usr/bin/env bash
set -eo pipefail
IFS=$'\n\t'

#
# The export below should be set in the crontab 
# 
# export PLATFORM=tx2
#
# This script wants as arguments
#
# $1    first argument is the path
#       to the folder containing the docker-compose.yml
# $2    Is the path where the record-all-day.sh is stored
#
#

function main() {
  TIMESTAMP="$(date '+%Y-%m-%d-%H-%M-%S-%6N')"
  echo "Timestamp: $TIMESTAMP"
  echo "running on: $PLATFORM"
  cd "$2"

  /usr/bin/python3.7 ./stop_odc_recording.py
  
  sleep 10

  ./stop_odc.sh -p "$PLATFORM" "$1"
  
  sleep 10

  ./restart_odc.sh -p "$PLATFORM" "$1"

  sleep 60

  /usr/bin/python3.7 ./init_odc.py

  sleep 10

  /usr/bin/python3.7 ./start_odc_recording.py

}
main "$1" "$2" 
