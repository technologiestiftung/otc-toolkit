#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# this script expects as the first argument the path to the outputfolder
# where the recordings are stored
# as second argument the path where the archives should be moved
#
function main (){
  for f in $(find "$1" -mindepth 1 -maxdepth 1 -type d ); do
    echo "archiving folder: $f"
    zip -r -q -T -j "$f" "$f"
    echo "moving archive ''$f.zip' to '$2'"
    cp "$f.zip" "$2"
    rm "$f.zip"
    echo "removing folder: $f"
    rm -rf "$f"
    echo "---"
    echo ""
  done
}

main "$1" "$2"
