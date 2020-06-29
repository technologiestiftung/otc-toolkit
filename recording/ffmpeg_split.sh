#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
# espects as argument the folder where the recordings are stored


function main() {
    cd "$1"
    last_recordings=$(ls ./*.mp4)
    for entry in $last_recordings; do
        NAME=$(echo "$entry" | cut -d'.' -f1) # get name of mp4-file without ending
        echo "$entry - should be the mp4 filename"
        echo "$NAME - should be foldername"

        mkdir "$NAME"
        mv "$entry" "$NAME"
        mv "${NAME}_tracker.json" "$NAME"
        mv "${NAME}_counter.json" "$NAME"
        cd "$NAME"
        ffmpeg -i "$entry" "${NAME}_%03d.png"
        cd ..
    done

}

main "$1"
