#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'


# This script wants as arguments
# $1    first argument is the path
#       to the folder containing the docker-compose.yml
# $2    second argument is the folder
#       where the recordings get stored
# $3    Is the path where the record.sh is stored
#
function main() {

  cd "$3"

  ./start_odc.sh "$1"

  sleep 60

  python3.7 ./init_odc.py

  sleep 10

  python3.7 ./start_odc_recording.py

  sleep 10

  ./ffmpeg_recording.sh "$2"

  sleep 30

  python3.7 ./stop_odc_recording.py

  sleep 5

  python3.7 ./download_tracker_data.py "$2"

  sleep 5

  ./ffmpeg_split.sh "$2"

  sleep 60

  ./stop_odc.sh "$1"

}
main "$1" "$2" "$3"
