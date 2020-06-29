#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# espects as argument the folder where the recordings are stored
function main() {
  #Start recording
  #echo "recording starting now"
  cd "$1"
  echo "moved to $1"

  FILENAME="$(date '+%Y-%m-%d-%H-%M-%S-%6N')"
  echo "creating file $FILENAME"
  ffmpeg -use_wallclock_as_timestamps 1 -f mjpeg -i "http://localhost:8080/webcam/stream" -t 00:00:10 -c:v copy -y "${FILENAME}.mp4"

}

main "$1"
